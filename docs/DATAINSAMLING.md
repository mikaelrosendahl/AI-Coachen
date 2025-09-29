# Datainsamling och träningsdata

Detta dokument beskriver hur man samlar in, förbereder och hanterar data för att träna AI-Coachen.

## Innehållsförteckning

1. [Översikt av datainsamling](#översikt-av-datainsamling)
2. [Automatisk datainsamling](#automatisk-datainsamling)
3. [Manuell datakuratering](#manuell-datakuratering)
4. [Dataformat och struktur](#dataformat-och-struktur)
5. [Kvalitetskontroll](#kvalitetskontroll)
6. [Dataexport och förberedelse](#dataexport-och-förberedelse)
7. [Etiska överväganden](#etiska-överväganden)

## Översikt av datainsamling

### Datatyper som samlas in

1. **Användarinteraktioner**
   - Frågor och förfrågningar från användare
   - AI-genererade svar
   - Användarfeedback och betyg
   - Sessionsinformation

2. **Kontextuell data**
   - Coaching-läge (personal/university)
   - Tidsstämpel
   - Session-ID för spårning
   - Användarpreferenser

3. **Kvalitetsindikationer**
   - Användarbetyg (1-5 stjärnor)
   - Textfeedback
   - Interaktionslängd
   - Uppföljningsfrågor

## Automatisk datainsamling

### Implementering av logging-system

```python
# utils/data_collector.py
import sqlite3
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import hashlib

class DataCollector:
    def __init__(self, db_path="training_data.db"):
        self.db_path = db_path
        self.setup_database()
        self.setup_logging()
    
    def setup_database(self):
        """Skapa databastabeller för datainsamling"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Huvudtabell för interaktioner
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                mode TEXT NOT NULL,
                user_input TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                response_time_ms INTEGER,
                tokens_used INTEGER,
                cost_usd REAL,
                user_hash TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Feedback-tabell
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_id INTEGER,
                rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                feedback_text TEXT,
                helpful BOOLEAN,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (interaction_id) REFERENCES interactions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_interaction(self, 
                       session_id: str,
                       mode: str,
                       user_input: str,
                       ai_response: str,
                       response_time_ms: int = None,
                       tokens_used: int = None,
                       cost_usd: float = None) -> int:
        """Logga en interaktion till databasen"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interactions 
            (session_id, timestamp, mode, user_input, ai_response, 
             response_time_ms, tokens_used, cost_usd)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            datetime.now().isoformat(),
            mode,
            user_input,
            ai_response,
            response_time_ms,
            tokens_used,
            cost_usd
        ))
        
        interaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return interaction_id
```

## Manuell datakuratering

### Verktyg för datagranskning

```python
# utils/data_curator.py
import streamlit as st
import sqlite3
import pandas as pd

class DataCurator:
    def __init__(self, db_path="training_data.db"):
        self.db_path = db_path
    
    def show_curation_interface(self):
        """Streamlit-interface för manuell datakuratering"""
        st.title("🔍 Datakuratering för AI-Coach")
        
        # Hämta data för granskning
        data = self.get_uncurated_data()
        
        if not data:
            st.info("Ingen data att granska just nu.")
            return
        
        # Granska interaktioner
        st.subheader("Granska interaktioner")
        
        for i, row in enumerate(data):
            with st.expander(f"Interaktion {i + 1}"):
                st.write("**Användarfråga:**")
                st.write(row['user_input'])
                
                st.write("**AI-svar:**")
                st.write(row['ai_response'])
                
                # Kurateringsverktyg
                quality = st.selectbox(
                    "Kvalitet:",
                    ["Välj...", "Utmärkt", "Bra", "OK", "Dålig"],
                    key=f"quality_{row['id']}"
                )
                
                include_in_training = st.checkbox(
                    "Inkludera i träning",
                    key=f"include_{row['id']}"
                )
```

## Dataformat och struktur

### OpenAI Fine-tuning format

```json
{
  "messages": [
    {
      "role": "system",
      "content": "Du är en AI-coach som hjälper med personlig utveckling."
    },
    {
      "role": "user", 
      "content": "Jag har svårt att hålla motivation för mina mål."
    },
    {
      "role": "assistant",
      "content": "Jag förstår att det kan vara utmanande. Låt oss utforska vad som driver dig."
    }
  ]
}
```

### Lokal träning format

```json
{
  "conversation_id": "conv_001",
  "turns": [
    {
      "speaker": "user",
      "text": "Jag känner mig fast i min karriär",
      "timestamp": "2025-09-29T10:00:00Z"
    },
    {
      "speaker": "coach",
      "text": "Berätta mer om vad som får dig att känna så.",
      "timestamp": "2025-09-29T10:00:30Z"
    }
  ]
}
```

## Kvalitetskontroll

### Automatisk kvalitetsbedömning

```python
class QualityController:
    def evaluate_interaction(self, user_input: str, ai_response: str):
        """Utvärdera kvaliteten på en interaktion"""
        scores = {
            'length_check': self.check_response_length(ai_response),
            'coherence_check': self.check_coherence(ai_response),
            'relevance_check': self.check_relevance(user_input, ai_response)
        }
        
        overall_score = sum(scores.values()) / len(scores)
        return overall_score, scores
    
    def check_response_length(self, response):
        """Kontrollera svarslängd"""
        if 20 <= len(response) <= 1000:
            return 1.0
        elif len(response) < 20:
            return 0.3
        else:
            return 0.7
```

## Dataexport och förberedelse

### Export för olika träningsmetoder

```python
class DataExporter:
    def export_for_openai_finetuning(self, output_file="training_data.jsonl"):
        """Exportera data för OpenAI fine-tuning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT mode, user_input, ai_response
            FROM interactions i
            LEFT JOIN feedback f ON i.id = f.interaction_id
            WHERE f.rating >= 3 OR f.rating IS NULL
        '''
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        training_examples = []
        for mode, user_input, ai_response in results:
            example = {
                "messages": [
                    {"role": "system", "content": self._get_system_prompt(mode)},
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": ai_response}
                ]
            }
            training_examples.append(example)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for example in training_examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        return len(training_examples)
```

## Etiska överväganden

### Dataskydd och integritet

1. **Anonymisering**
   - Använd hash-funktioner för användaridentifiering
   - Ta bort eller maskera personlig information
   - Lagra inte IP-adresser eller teknisk identifiering

2. **Samtycke**
   - Informera användare om datainsamling
   - Ge möjlighet att välja bort
   - Respektera GDPR och andra dataskyddsregler

3. **Datalagring**
   - Begränsa lagringstid
   - Säker datalagring med kryptering
   - Regelbunden rensning av gamla data

### Implementering av etiska riktlinjer

```python
class EthicsCompliance:
    def __init__(self):
        self.pii_patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',  # Datum
            r'\b\d{10,}\b',  # Telefonnummer
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        ]
    
    def anonymize_text(self, text):
        """Ta bort eller maskera personlig information"""
        anonymized = text
        for pattern in self.pii_patterns:
            anonymized = re.sub(pattern, '[ANONYMIZED]', anonymized)
        return anonymized
```

Detta dokument ger en komplett guide för datainsamling och förberedelse av träningsdata för AI-Coachen.