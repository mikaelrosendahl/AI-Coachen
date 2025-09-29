# Modellträning för AI-Coachen

Detta dokument beskriver olika metoder för att träna och anpassa AI-modellen för att förbättra AI-Coachens prestanda och specialisering.

## Innehållsförteckning

1. [Översikt](#översikt)
2. [Fine-tuning med OpenAI](#fine-tuning-med-openai)
3. [Lokal modellträning](#lokal-modellträning)
4. [RAG (Retrieval-Augmented Generation)](#rag-retrieval-augmented-generation)
5. [Datainsamling och förberedelse](#datainsamling-och-förberedelse)
6. [Implementationsguide](#implementationsguide)
7. [Kostnadsjämförelse](#kostnadsjämförelse)
8. [Rekommendationer](#rekommendationer)

## Översikt

AI-Coachen kan förbättras genom olika tränings- och anpassningsmetoder. Varje metod har sina fördelar och är lämplig för olika användningsfall:

- **Fine-tuning**: Snabbt sätt att anpassa OpenAI:s modeller
- **Lokal träning**: Full kontroll och kostnadsbesparing på lång sikt
- **RAG**: Förbättrar svar med extern kunskapsbas

## Fine-tuning med OpenAI

### Beskrivning
Fine-tuning anpassar en befintlig OpenAI-modell för specifika användningsfall genom att träna den på dina egna data.

### Fördelar
- ✅ Behåller kraftfulla basmodellens kapacitet
- ✅ Relativt enkelt att implementera
- ✅ Mindre datamängd krävs (minst 10 exempel, rekommenderat 50-100)
- ✅ Snabbare träning (minuter till timmar)
- ✅ Automatisk optimering av hyperparametrar

### Nackdelar
- ❌ Kontinuerliga API-kostnader
- ❌ Begränsad kontroll över modellens interna logik
- ❌ Beroende av OpenAI:s tjänster

### Kostnader
- **Träning**: $0.008 per 1K tokens
- **Användning**: $0.012 per 1K input tokens, $0.016 per 1K output tokens (gpt-3.5-turbo)

### Implementationsprocess

#### 1. Dataförberedelse
```python
# Exempel på dataformat för fine-tuning
training_data = [
    {
        "messages": [
            {"role": "system", "content": "Du är en AI-coach som hjälper användare med personlig utveckling."},
            {"role": "user", "content": "Jag har svårt att hålla mig motiverad med mina mål."},
            {"role": "assistant", "content": "Jag förstår att motivation kan vara utmanande. Låt oss utforska vad som driver dig. Vad är det viktigaste målet för dig just nu, och varför är det betydelsefullt?"}
        ]
    }
]
```

#### 2. Datavalidering
```python
import json

def validate_training_data(data):
    """Validera träningsdata enligt OpenAI:s format"""
    for example in data:
        assert "messages" in example
        for message in example["messages"]:
            assert "role" in message and message["role"] in ["system", "user", "assistant"]
            assert "content" in message
    return True
```

#### 3. Uppladdning och träning
```python
from openai import OpenAI

client = OpenAI()

# Ladda upp träningsfil
response = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Starta fine-tuning
fine_tune_job = client.fine_tuning.jobs.create(
    training_file=response.id,
    model="gpt-3.5-turbo"
)
```

## Lokal modellträning

### Beskrivning
Träning av egen modell med open-source verktyg som Transformers, LoRA eller full parameter fine-tuning.

### Fördelar
- ✅ Full kontroll över modellen
- ✅ Inga löpande API-kostnader efter träning
- ✅ Kan köras helt lokalt (datasäkerhet)
- ✅ Anpassningsbar för specifika domäner
- ✅ Skalbar för stora datamängder

### Nackdelar
- ❌ Kräver betydligt mer träningsdata (tusentals exempel)
- ❌ Beräkningsintensivt (GPU-krav)
- ❌ Längre utvecklings- och träningstid
- ❌ Kräver djupare ML-kunskap

### Rekommenderade modeller
- **Llama 2/3**: Meta's open-source modeller
- **Mistral**: Effektiva och kraftfulla modeller
- **CodeLlama**: Specialiserad för kod och tekniska ämnen

### Implementationsprocess

#### 1. Miljöuppsättning
```python
# requirements_training.txt
torch>=2.0.0
transformers>=4.30.0
datasets>=2.12.0
peft>=0.4.0  # För LoRA fine-tuning
accelerate>=0.20.0
```

#### 2. LoRA Fine-tuning (rekommenderad metod)
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

# Ladda basmodell
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Konfigurera LoRA
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["c_attn"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

# Applicera LoRA
model = get_peft_model(model, lora_config)
```

## RAG (Retrieval-Augmented Generation)

### Beskrivning
RAG förbättrar AI:n genom att kombinera en språkmodell med en kunskapsbas som söks igenom dynamiskt.

### Fördelar
- ✅ Behåller kraftfull basmodell
- ✅ Lätt att uppdatera kunskaper utan omträning
- ✅ Kostnadseffektivt
- ✅ Bättre kontroll över informationskällor
- ✅ Transparent - kan visa källor

### Nackdelar
- ❌ Kräver bra söksystem
- ❌ Kvaliteten beror på kunskapsbas
- ❌ Kan bli långsam vid stora kunskapsbaser

### Implementationsprocess

#### 1. Kunskapsbasuppsättning
```python
import chromadb
from sentence_transformers import SentenceTransformer

# Initiera embedding-modell
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Skapa vektordatabas
client = chromadb.Client()
collection = client.create_collection("coaching_knowledge")

# Lägg till dokument
documents = [
    "Motivation är nyckeln till framgång. Sätt tydliga, mätbara mål.",
    "Aktiv lyssning innebär att fokusera helt på vad personen säger.",
    # ... fler coaching-dokument
]

for i, doc in enumerate(documents):
    embedding = embedding_model.encode(doc)
    collection.add(
        embeddings=[embedding.tolist()],
        documents=[doc],
        ids=[f"doc_{i}"]
    )
```

#### 2. RAG-implementering
```python
def rag_query(question, collection, model, k=3):
    # Sök relevanta dokument
    query_embedding = embedding_model.encode(question)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )
    
    # Bygg kontext
    context = "\n".join(results['documents'][0])
    
    # Skapa prompt med kontext
    prompt = f"""
    Baserat på följande information:
    {context}
    
    Användarfråga: {question}
    
    Ge ett hjälpsamt coaching-svar:
    """
    
    return ai_coach.generate_response(prompt)
```

## Datainsamling och förberedelse

### Datatyper för träning

#### 1. Coaching-sessioner
```python
# Struktur för coaching-data
coaching_session = {
    "session_id": "sess_001",
    "timestamp": "2025-09-29T10:00:00Z",
    "mode": "personal",  # eller "university"
    "conversation": [
        {
            "role": "user",
            "content": "Jag känner mig fast i min karriär",
            "timestamp": "2025-09-29T10:00:00Z"
        },
        {
            "role": "assistant", 
            "content": "Berätta mer om vad som får dig att känna så. Vad är det specifikt som känns 'fast'?",
            "timestamp": "2025-09-29T10:00:30Z",
            "feedback": {
                "rating": 4,
                "helpful": true
            }
        }
    ]
}
```

#### 2. Datainsamling från systemet
```python
# Utöka AICoach-klassen för datainsamling
class AICoach:
    def __init__(self):
        self.training_data = []
    
    def log_interaction(self, user_input, response, feedback=None):
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": response,
            "feedback": feedback
        }
        self.training_data.append(interaction)
        
        # Spara till fil
        with open("training_data.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(interaction, ensure_ascii=False) + "\n")
```

### Datafiltrering och kvalitetskontroll

```python
def filter_quality_data(interactions, min_rating=3):
    """Filtrera bort dåliga exempel baserat på användarfeedback"""
    quality_data = []
    
    for interaction in interactions:
        if (interaction.get("feedback", {}).get("rating", 0) >= min_rating and
            len(interaction["user_input"]) > 10 and
            len(interaction["ai_response"]) > 20):
            quality_data.append(interaction)
    
    return quality_data

def format_for_openai(interactions):
    """Formatera data för OpenAI fine-tuning"""
    training_examples = []
    
    for interaction in interactions:
        example = {
            "messages": [
                {"role": "system", "content": "Du är en AI-coach som hjälper med personlig utveckling och universitets-AI-implementation."},
                {"role": "user", "content": interaction["user_input"]},
                {"role": "assistant", "content": interaction["ai_response"]}
            ]
        }
        training_examples.append(example)
    
    return training_examples
```

## Kostnadsjämförelse

### Fine-tuning (OpenAI)
- **Initial träning**: ~$50-200 (beroende på datastorlek)
- **Månadsvis användning**: $100-500 (1000 sessioner/månad)
- **Total kostnad år 1**: ~$1,500-6,200

### Lokal träning
- **Initial setup**: $2,000-5,000 (GPU-hårdvara)
- **Träningskostnad**: $100-500 (el och tid)
- **Löpande kostnader**: ~$50/månad (el)
- **Total kostnad år 1**: ~$2,700-6,100

### RAG
- **Initial setup**: $0-100 (vektordatabas)
- **Månadsvis användning**: $50-200 (API-kostnader)
- **Total kostnad år 1**: ~$600-2,500

## Rekommendationer

### För prototyping och små volymer
**Använd Fine-tuning med OpenAI**
- Snabbt att komma igång
- Låg initial investering
- Bra för validering av koncept

### För mediumstora projekt
**Använd RAG-approach**
- Balans mellan kostnad och prestanda
- Flexibel kunskapshantering
- Lätt att underhålla

### För stora volymer eller säkerhetskritiska system
**Använd lokal träning**
- Full kontroll
- Kostnadseffektivt på lång sikt
- Bästa datasäkerhet

## Nästa steg

1. **Börja med datainsamling**: Implementera logging i befintligt system
2. **Testa RAG**: Enklast att implementera först
3. **Utvärdera prestanda**: Mät förbättring mot baseline
4. **Skala upp**: Välj lämplig metod baserat på resultat

## Referenser

- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)