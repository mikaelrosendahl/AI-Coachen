# Implementation Guide: Modellträning för AI-Coachen

Detta dokument innehåller steg-för-steg implementationsguider för de olika träningsmetoderna.

## Innehållsförteckning

1. [Snabbstart: RAG Implementation](#snabbstart-rag-implementation)
2. [Fine-tuning Implementation](#fine-tuning-implementation)
3. [Lokal träning med LoRA](#lokal-träning-med-lora)
4. [Datainsamlingssystem](#datainsamlingssystem)
5. [Utvärdering och testning](#utvärdering-och-testning)

## Snabbstart: RAG Implementation

### Steg 1: Installera beroenden

```bash
pip install chromadb sentence-transformers langchain
```

### Steg 2: Skapa RAG-modul

```python
# utils/rag_system.py
import chromadb
from sentence_transformers import SentenceTransformer
import json
from typing import List, Dict
import os

class RAGSystem:
    def __init__(self, collection_name="ai_coach_knowledge"):
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(collection_name)
    
    def add_knowledge(self, documents: List[str], metadata: List[Dict] = None):
        """Lägg till dokument till kunskapsbasen"""
        if metadata is None:
            metadata = [{"source": f"doc_{i}"} for i in range(len(documents))]
        
        # Generera embeddings
        embeddings = self.embedding_model.encode(documents)
        
        # Lägg till i collection
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadata,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
        
        print(f"Lade till {len(documents)} dokument till kunskapsbasen")
    
    def search_relevant_context(self, query: str, n_results: int = 3) -> List[str]:
        """Sök relevanta dokument för en fråga"""
        query_embedding = self.embedding_model.encode([query])
        
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )
        
        return results['documents'][0] if results['documents'] else []
    
    def enhance_prompt(self, user_query: str, system_prompt: str) -> str:
        """Förbättra prompt med relevant kontext"""
        relevant_docs = self.search_relevant_context(user_query)
        
        if relevant_docs:
            context = "\n".join([f"- {doc}" for doc in relevant_docs])
            enhanced_prompt = f"""{system_prompt}

Relevant bakgrundsinformation:
{context}

Använd denna information för att ge mer träffsäkra och hjälpsamma svar."""
        else:
            enhanced_prompt = system_prompt
        
        return enhanced_prompt

# Exempel på kunskapsdata för coaching
COACHING_KNOWLEDGE = [
    "SMART-mål är Specifika, Mätbara, Uppnåeliga, Relevanta och Tidsbundna. De hjälper till att skapa tydliga och uppnåeliga målsättningar.",
    "Aktiv lyssning innebär att ge full uppmärksamhet, ställa öppna frågor och reflektera tillbaka vad personen säger för att visa förståelse.",
    "Motivation kan vara inre (autonomi, kompetens, samhörighet) eller yttre (belöningar, bestraffningar). Inre motivation är oftast mer hållbar.",
    "Feedback bör vara specifik, konstruktiv och fokuserad på beteende snarare än person. Använd SBI-modellen: Situation, Beteende, Impact.",
    "Förändring sker i steg: Förberedelse, Handling, Upprätthållande. Var förberedd på motstånd och bakslag som naturliga delar av processen.",
    "Självreflektion är viktigt för personlig utveckling. Ställ frågor som 'Vad lärde jag mig?', 'Vad skulle jag göra annorlunda?'",
    "Stress kan hanteras genom tekniker som djupandning, mindfulness, fysisk aktivitet och tidshantering.",
    "AI-implementation i universitet kräver förändringsledning, utbildning av personal och gradvis införande av nya teknologier.",
    "Stakeholder-analys hjälper att identifiera nyckelpersoner och deras intressen i ett AI-projekt på universitet.",
    "Etiska överväganden för AI inkluderar transparens, rättvisa, ansvarsskyldighet och integritet."
]
```

### Steg 3: Integrera RAG i AI-Coach

```python
# core/ai_coach.py - lägg till RAG-support
from utils.rag_system import RAGSystem

class AICoach:
    def __init__(self):
        # ... befintlig kod ...
        self.rag_system = RAGSystem()
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialisera kunskapsbasen om den är tom"""
        try:
            # Kontrollera om kunskapsbasen redan har innehåll
            results = self.rag_system.collection.peek(limit=1)
            if not results['documents']:
                print("Initialiserar kunskapsbasen...")
                from utils.rag_system import COACHING_KNOWLEDGE
                self.rag_system.add_knowledge(COACHING_KNOWLEDGE)
        except Exception as e:
            print(f"Kunde inte initiera kunskapsbasen: {e}")
    
    def generate_response(self, user_input, mode="personal", use_rag=True):
        """Generera svar med valfri RAG-förstärkning"""
        try:
            # Skapa system prompt
            if mode == "personal":
                system_prompt = self._get_personal_coach_prompt()
            else:
                system_prompt = self._get_university_coach_prompt()
            
            # Förbättra med RAG om aktiverat
            if use_rag:
                system_prompt = self.rag_system.enhance_prompt(user_input, system_prompt)
            
            # ... resten av befintlig kod för API-anrop ...
            
        except Exception as e:
            print(f"Fel vid generering av svar: {e}")
            return "Ursäkta, jag stötte på ett problem. Kan du försöka igen?"
```

### Steg 4: Lägg till RAG-kontroller i UI

```python
# main.py - lägg till RAG-kontroller
def show_coaching_interface(mode):
    # ... befintlig kod ...
    
    # RAG-kontroller
    st.sidebar.subheader("🧠 Kunskapsförstärkning")
    use_rag = st.sidebar.checkbox("Använd RAG (Kunskapsbas)", value=True, 
                                  help="Förbättrar svar med relevant bakgrundsinformation")
    
    if st.sidebar.button("📚 Visa kunskapsbas"):
        show_knowledge_base()
    
    # ... resten av befintlig kod ...
    
    # Vid generering av svar
    if st.button("Skicka"):
        with st.spinner("Genererar svar..."):
            response = ai_coach.generate_response(user_input, mode, use_rag=use_rag)
            # ... hantera svar ...

def show_knowledge_base():
    """Visa innehållet i kunskapsbasen"""
    st.subheader("📚 Kunskapsbas")
    try:
        results = st.session_state.ai_coach.rag_system.collection.peek(limit=100)
        if results['documents']:
            for i, doc in enumerate(results['documents']):
                with st.expander(f"Dokument {i+1}"):
                    st.write(doc)
        else:
            st.info("Kunskapsbasen är tom. Lägg till dokument för att förbättra AI:ns svar.")
    except Exception as e:
        st.error(f"Kunde inte visa kunskapsbas: {e}")
```

## Fine-tuning Implementation

### Steg 1: Förbered träningsdata

```python
# utils/training_data_collector.py
import json
from datetime import datetime
from typing import List, Dict

class TrainingDataCollector:
    def __init__(self, output_file="training_data.jsonl"):
        self.output_file = output_file
        self.training_examples = []
    
    def collect_from_sessions(self, sessions_data: List[Dict]):
        """Samla träningsdata från coaching-sessioner"""
        for session in sessions_data:
            if session.get('rating', 0) >= 4:  # Endast bra sessioner
                example = {
                    "messages": [
                        {
                            "role": "system",
                            "content": self._get_system_prompt(session.get('mode', 'personal'))
                        },
                        {
                            "role": "user", 
                            "content": session['user_input']
                        },
                        {
                            "role": "assistant",
                            "content": session['ai_response']
                        }
                    ]
                }
                self.training_examples.append(example)
    
    def _get_system_prompt(self, mode):
        if mode == "personal":
            return "Du är en AI-coach som hjälper med personlig utveckling, målsättning och självreflektion."
        else:
            return "Du är en AI-expert som hjälper universitet att implementera AI-teknologi effektivt och etiskt."
    
    def save_training_data(self):
        """Spara träningsdata i JSONL-format"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for example in self.training_examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        print(f"Sparade {len(self.training_examples)} träningsexempel till {self.output_file}")
    
    def validate_data(self):
        """Validera träningsdata enligt OpenAI:s krav"""
        valid_examples = []
        
        for example in self.training_examples:
            if self._is_valid_example(example):
                valid_examples.append(example)
            else:
                print(f"Ogiltigt exempel: {example}")
        
        self.training_examples = valid_examples
        return len(valid_examples)
    
    def _is_valid_example(self, example):
        if "messages" not in example:
            return False
        
        for message in example["messages"]:
            if "role" not in message or message["role"] not in ["system", "user", "assistant"]:
                return False
            if "content" not in message or len(message["content"]) < 1:
                return False
        
        return True
```

### Steg 2: OpenAI Fine-tuning

```python
# utils/openai_finetuner.py
import openai
import json
import time
from typing import Optional

class OpenAIFineTuner:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def upload_training_file(self, file_path: str) -> str:
        """Ladda upp träningsfil till OpenAI"""
        try:
            with open(file_path, 'rb') as f:
                response = self.client.files.create(
                    file=f,
                    purpose="fine-tune"
                )
            print(f"Träningsfil uppladdad: {response.id}")
            return response.id
        except Exception as e:
            print(f"Fel vid uppladdning: {e}")
            return None
    
    def create_fine_tune_job(self, training_file_id: str, model: str = "gpt-3.5-turbo") -> Optional[str]:
        """Skapa fine-tuning jobb"""
        try:
            response = self.client.fine_tuning.jobs.create(
                training_file=training_file_id,
                model=model,
                hyperparameters={
                    "n_epochs": 3  # Anpassa efter behov
                }
            )
            print(f"Fine-tuning jobb skapat: {response.id}")
            return response.id
        except Exception as e:
            print(f"Fel vid skapande av fine-tuning jobb: {e}")
            return None
    
    def monitor_fine_tune_job(self, job_id: str):
        """Övervaka fine-tuning jobbets progress"""
        while True:
            try:
                response = self.client.fine_tuning.jobs.retrieve(job_id)
                status = response.status
                
                print(f"Status: {status}")
                
                if status == "succeeded":
                    print(f"Fine-tuning klar! Modell: {response.fine_tuned_model}")
                    return response.fine_tuned_model
                elif status == "failed":
                    print(f"Fine-tuning misslyckades: {response.error}")
                    return None
                
                time.sleep(30)  # Vänta 30 sekunder innan nästa kontroll
                
            except Exception as e:
                print(f"Fel vid övervakning: {e}")
                time.sleep(60)
    
    def test_fine_tuned_model(self, model_id: str, test_prompt: str):
        """Testa den fine-tunade modellen"""
        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "user", "content": test_prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Fel vid testning: {e}")
            return None
```

### Steg 3: Användning av fine-tunad modell

```python
# core/ai_coach.py - uppdatera för fine-tunad modell
class AICoach:
    def __init__(self, custom_model_id=None):
        # ... befintlig kod ...
        self.custom_model_id = custom_model_id or "gpt-4"
    
    def generate_response(self, user_input, mode="personal", use_custom_model=False):
        model_to_use = self.custom_model_id if use_custom_model else "gpt-4"
        
        # ... resten av koden med model_to_use istället för hårdkodad modell ...
```

## Lokal träning med LoRA

### Steg 1: Installera beroenden

```bash
pip install torch transformers datasets peft accelerate bitsandbytes
```

### Steg 2: LoRA Fine-tuning implementation

```python
# utils/local_trainer.py
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import Dataset
import json

class LoRATrainer:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Ladda modell med 4-bit quantization för minnesbesparing
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_4bit=True,
            device_map="auto"
        )
        
        # Förbered modell för LoRA
        self.model = prepare_model_for_kbit_training(self.model)
        
        # LoRA konfiguration
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["c_attn"],
            lora_dropout=0.1,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        self.model = get_peft_model(self.model, lora_config)
        
    def prepare_dataset(self, training_file):
        """Förbered dataset för träning"""
        with open(training_file, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f]
        
        # Konvertera till träningsformat
        texts = []
        for example in data:
            conversation = ""
            for message in example["messages"]:
                conversation += f"{message['role']}: {message['content']}\n"
            texts.append(conversation)
        
        # Tokenisera
        tokenized = self.tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
        
        return Dataset.from_dict(tokenized)
    
    def train(self, training_file, output_dir="./lora_model"):
        """Träna modellen med LoRA"""
        dataset = self.prepare_dataset(training_file)
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            warmup_steps=100,
            logging_steps=10,
            save_steps=500,
            evaluation_strategy="no",
            save_strategy="steps",
            fp16=True,
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator,
        )
        
        # Starta träning
        trainer.train()
        
        # Spara modell
        trainer.save_model()
        print(f"Modell sparad i {output_dir}")
        
    def load_trained_model(self, model_path):
        """Ladda tränad LoRA-modell"""
        from peft import PeftModel
        
        base_model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.model = PeftModel.from_pretrained(base_model, model_path)
        
    def generate_response(self, prompt, max_length=200):
        """Generera svar med tränad modell"""
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):]  # Ta bort prompt från svar
```

## Datainsamlingssystem

### Steg 1: Utökad AI-Coach med logging

```python
# core/ai_coach.py - lägg till datainsamling
import sqlite3
from datetime import datetime

class AICoach:
    def __init__(self):
        # ... befintlig kod ...
        self.init_training_database()
    
    def init_training_database(self):
        """Initialisera databas för träningsdata"""
        conn = sqlite3.connect('training_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                mode TEXT,
                user_input TEXT,
                ai_response TEXT,
                rating INTEGER,
                feedback TEXT,
                session_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_interaction(self, user_input, ai_response, mode, session_id, rating=None, feedback=None):
        """Logga interaktion för träningsdata"""
        conn = sqlite3.connect('training_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO training_interactions 
            (timestamp, mode, user_input, ai_response, rating, feedback, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            mode,
            user_input,
            ai_response,
            rating,
            feedback,
            session_id
        ))
        
        conn.commit()
        conn.close()
    
    def export_training_data(self, min_rating=3):
        """Exportera träningsdata till JSONL-format"""
        conn = sqlite3.connect('training_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mode, user_input, ai_response FROM training_interactions
            WHERE rating >= ? OR rating IS NULL
        ''', (min_rating,))
        
        results = cursor.fetchall()
        conn.close()
        
        training_examples = []
        for mode, user_input, ai_response in results:
            system_prompt = self._get_system_prompt_for_mode(mode)
            
            example = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": ai_response}
                ]
            }
            training_examples.append(example)
        
        # Spara till fil
        with open('exported_training_data.jsonl', 'w', encoding='utf-8') as f:
            for example in training_examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        return len(training_examples)
```

### Steg 2: Feedback-system i UI

```python
# main.py - lägg till feedback-system
def show_coaching_interface(mode):
    # ... befintlig kod ...
    
    # Efter att svar genererats
    if 'last_response' in st.session_state:
        st.subheader("📝 Feedback")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            rating = st.select_slider(
                "Hur hjälpsamt var svaret?",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: "⭐" * x
            )
        
        with col2:
            feedback_text = st.text_area(
                "Ytterligare kommentarer (valfritt):",
                placeholder="Vad var bra? Vad kunde förbättras?"
            )
        
        if st.button("Skicka feedback"):
            # Logga feedback
            ai_coach.log_interaction(
                user_input=st.session_state.get('last_input', ''),
                ai_response=st.session_state.get('last_response', ''),
                mode=mode,
                session_id=st.session_state.get('session_id', ''),
                rating=rating,
                feedback=feedback_text
            )
            st.success("Tack för din feedback! Detta hjälper oss förbättra AI-coachen.")
```

## Utvärdering och testning

### Steg 1: Evalueringsmetrik

```python
# utils/evaluation.py
import json
from typing import List, Dict
import statistics

class ModelEvaluator:
    def __init__(self, test_data_file):
        with open(test_data_file, 'r', encoding='utf-8') as f:
            self.test_data = [json.loads(line) for line in f]
    
    def evaluate_responses(self, model_function):
        """Utvärdera modellens svar mot testdata"""
        scores = []
        
        for example in self.test_data:
            user_input = None
            expected_response = None
            
            for message in example["messages"]:
                if message["role"] == "user":
                    user_input = message["content"]
                elif message["role"] == "assistant":
                    expected_response = message["content"]
            
            if user_input and expected_response:
                # Generera svar från modell
                generated_response = model_function(user_input)
                
                # Beräkna likhet (förenklad)
                similarity = self.calculate_similarity(expected_response, generated_response)
                scores.append(similarity)
        
        return {
            "average_score": statistics.mean(scores),
            "median_score": statistics.median(scores),
            "total_tests": len(scores)
        }
    
    def calculate_similarity(self, expected, generated):
        """Enkel likhetsberäkning (kan förbättras med BLEU, ROUGE etc.)"""
        expected_words = set(expected.lower().split())
        generated_words = set(generated.lower().split())
        
        if not expected_words:
            return 0
        
        intersection = expected_words.intersection(generated_words)
        return len(intersection) / len(expected_words)

# Användning
evaluator = ModelEvaluator("test_data.jsonl")
results = evaluator.evaluate_responses(lambda x: ai_coach.generate_response(x))
print(f"Genomsnittlig poäng: {results['average_score']:.2f}")
```

Detta täcker de viktigaste implementationsdetaljerna för alla tre träningsmetoderna. Vill du att jag fortsätter med någon specifik del eller har du frågor om implementationen?