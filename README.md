# 🤖🎓 AI-Coachen

> **En intelligent AI-coach för personlig utveckling och universitets AI-implementering**

AI-Coachen är en egenutvecklad intelligent coach som kombinerar personlig utveckling med expertis inom AI-implementering på universitet. Systemet fungerar som både din personliga mentor och strategiska rådgivare för AI-transformation inom akademisk miljö.

![AI-Coachen Demo](docs/demo-screenshot.png)

## ✨ Huvudfunktioner

### 🧠 Personlig Coaching
- **Målsättning & Progress Tracking**: Sätt och följ upp personliga utvecklingsmål
- **Reflektion & Självutvärdering**: Strukturerade reflektionssessions med mood/energy tracking  
- **Personaliserade Råd**: AI-genererade råd baserat på dina mönster och framsteg
- **Coaching Prompts**: Intelligenta frågor för att driva din utveckling framåt

### 🎓 Universitets AI-Implementering
- **Strategisk Planering**: Komplett roadmap för AI-adoption på ditt universitet
- **Projekthantering**: Hantera AI-projekt genom alla implementeringsfaser
- **Stakeholder Management**: Specifika strategier för olika grupper (fakultet, forskare, IT, administration)
- **Risk Assessment**: Identifiera och hantera implementationsutmaningar
- **Change Management**: Verktyg för att driva organisationsförändring

### 🔄 Hybrid Coaching
- **Integrerad Approach**: Kombinerar personlig utveckling med AI-expertis
- **Ledarskapscoaching**: Utveckla färdigheter för att leda AI-transformation
- **Balans & Välmående**: Hantera stress och motstånd vid stora förändringar

## 🚀 Snabbstart

### Automatisk Installation (Rekommenderas)

**Windows:**
```bash
# Dubbelklicka på start_coach.bat eller kör:
start_coach.bat
```

**Linux/Mac:**
```bash
chmod +x start_coach.sh
./start_coach.sh
```

### Manuell Installation

```bash
# 1. Klona repository
git clone https://github.com/mikaelrosendahl/AI-Coachen.git
cd AI-Coachen

# 2. Skapa virtual environment
python -m venv venv

# 3. Aktivera virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Installera dependencies
pip install -r requirements.txt

# 5. Kopiera environment template
cp .env.example .env

# 6. Lägg till din OpenAI API-nyckel i .env
# OPENAI_API_KEY=your_api_key_here

# 7. Testa systemet (valfritt - kräver ej API-nyckel)
python demo_ai_coach.py

# 8. Starta applikationen
streamlit run main.py
```

## 📖 Användning

1. **Välj Coaching-läge**: Personlig, Universitets, eller Hybrid
2. **Starta Session**: Börja din coaching-session
3. **Utforska Funktioner**: 
   - 💬 Chat med AI-coachen
   - 🎯 Sätt och spåra mål
   - 📝 Reflektera och utvecklas
   - 🏗️ Hantera AI-projekt
   - ⚠️ Lös implementationsutmaningar

## 🎯 Användningsfall

### Scenario 1: Personlig AI-utveckling
- Lära sig AI/ML för karriärutveckling
- Strukturerad utvecklingsplan med progress tracking
- Motivationsstöd och reflektion

### Scenario 2: Universitets AI-transformation  
- Implementera AI-verktyg för forskning och undervisning
- Stakeholder-analys och change management
- Systematisk roadmap för AI-adoption

### Scenario 3: Hybrid ledarskap
- Leda AI-implementering medan du utvecklar egna AI-kunskaper
- Balansera personlig utveckling med organisatoriska krav
- Integrerad approach för både personlig och professionell framgång

## 🏗️ Arkitektur

```
AI-Coachen/
├── core/                   # Kärnfunktionalitet
│   ├── ai_coach.py        # Huvudcoach-modell (GPT-4 integration)
│   ├── personal_coach.py  # Personlig coaching logik
│   └── university_coach.py # Universitets-coaching logik
├── data/                   # SQLite databas (skapas automatiskt)
├── ui/                     # Streamlit interface komponenter
├── utils/                  # Utilities och konfiguration
├── logs/                   # Systemloggar (skapas automatiskt)
├── main.py                 # Huvudapplikation
├── demo_ai_coach.py       # Demo utan API-krav
└── test_ai_coach.py       # Test suite
```

## 🔧 Tekniska Krav

- **Python**: 3.8+ 
- **RAM**: 4GB minimum
- **Internet**: För OpenAI API-anrop
- **Browser**: Modern webbläsare för Streamlit UI
- **API**: OpenAI API-nyckel (för AI-funktioner)

## 📦 Dependencies

- `openai>=1.3.0` - OpenAI GPT-4 API
- `streamlit>=1.28.0` - Webbapplikations-framework
- `pandas>=2.0.0` - Dataanalys
- `numpy>=1.24.0` - Numeriska beräkningar
- `pydantic>=2.0.0` - Datavalidering
- `python-dotenv>=1.0.0` - Environment variables
- `tiktoken>=0.5.0` - Token counting för OpenAI

## 🔒 Säkerhet och Integritet

- **Lokal Data**: All personlig data lagras lokalt i SQLite
- **API-säkerhet**: Nycklar lagras säkert i `.env` fil
- **Privacy**: Inga känsliga data delas utöver nödvändiga API-anrop
- **Export**: Fullständig dataexport möjlig när som helst

## 🧪 Demo och Test

### Kör Demo (Ingen API-nyckel krävs)
```bash
python demo_ai_coach.py
```
Visar alla funktioner med mock-data och exempel.

### Kör Test Suite
```bash
python test_ai_coach.py  
```
Testar alla moduler (vissa tester kräver API-nyckel).

## 🧠 Modellträning och Anpassning

AI-Coachen kan förbättras och anpassas genom olika träningsmetoder för att bättre passa dina specifika behov:

### 🎯 Tillgängliga Träningsmetoder

1. **🔧 Fine-tuning (OpenAI)**
   - Snabbt sätt att anpassa GPT-4 för coaching
   - Kräver 50-100 kvalitetsexempel
   - Kostnad: ~$50-200 för träning

2. **🏠 Lokal Modellträning**
   - Full kontroll med LoRA fine-tuning
   - Inga löpande API-kostnader
   - Kräver GPU och mer data

3. **📚 RAG (Kunskapsförstärkning)**
   - Förbättrar svar med egen kunskapsbas
   - Lätt att uppdatera och underhålla
   - Mest kostnadseffektiv

### 🚀 Kom igång med träning

```bash
# 1. Samla träningsdata från dina sessioner
python utils/export_training_data.py

# 2. Välj träningsmetod:

# För Fine-tuning:
python utils/fine_tune_openai.py --data training_data.jsonl

# För lokal träning:
python utils/train_local_model.py --method lora

# För RAG-implementation:
python utils/setup_rag.py --knowledge_base your_docs/
```

### 📊 Datainsamling

- Automatisk logging av alla coaching-sessioner
- Användarfeedback och kvalitetsbedömning
- Export i standardformat för träning
- Etiska riktlinjer och dataskydd

### 📖 Träningsdokumentation

- [**MODELLTRÄNING.md**](docs/MODELLTRANING.md) - Komplett guide för alla träningsmetoder
- [**IMPLEMENTATION_GUIDE.md**](docs/IMPLEMENTATION_GUIDE.md) - Steg-för-steg implementering
- [**DATAINSAMLING.md**](docs/DATAINSAMLING.md) - Datainsamling och kvalitetskontroll

## 📚 Dokumentation

- [**ANVÄNDARGUIDE.md**](ANVÄNDARGUIDE.md) - Komplett användarmanual
- [**API-dokumentation**](docs/api.md) - För utvecklare
- [**Deployment Guide**](docs/deployment.md) - Produktionssättning

## 🤝 Bidra

Vi välkomnar bidrag! För att bidra:

1. Fork projektet
2. Skapa en feature branch (`git checkout -b feature/AmazingFeature`)  
3. Commita dina ändringar (`git commit -m 'Add some AmazingFeature'`)
4. Push till branch (`git push origin feature/AmazingFeature`)
5. Öppna en Pull Request

### Utvecklingsmiljö
```bash
# Installera development dependencies
pip install -r requirements-dev.txt

# Kör linting
flake8 core/ utils/

# Kör type checking  
mypy core/ utils/
```

## 📝 Licens

Detta projekt är licensierat under MIT License - se [LICENSE](LICENSE) filen för detaljer.

## 🌟 Acknowledgments

- OpenAI för GPT-4 API
- Streamlit community för fantastiskt framework
- Alla som bidrar till open source AI-utveckling

## 📞 Support

- **GitHub Issues**: För bug reports och feature requests
- **Dokumentation**: Se [ANVÄNDARGUIDE.md](ANVÄNDARGUIDE.md)
- **Demo**: Kör `python demo_ai_coach.py` för att testa funktioner

---

**Byggd med ❤️ för personlig utveckling och AI-transformation inom akademi**

🤖 *"Din intelligenta partner för både personlig tillväxt och organisatorisk AI-adoption"* 🎓
 
 # #   P r o d u c t i o n   L o g i n   T r o u b l e s h o o t i n g   -   L e s s o n s   L e a r n e d   ( O c t   1 9 ,   2 0 2 5 ) 
 
 # # #   P r o b l e m   S o l v e d 
 * * I s s u e * * :   A d m i n   l o g i n   f a i l e d   o n   p r o d u c t i o n   w i t h   ' L o g i n   f a i l e d '   m e s s a g e 
 * * R o o t   C a u s e * * :   P o s t g r e S Q L   i n e t   d a t a t y p e   c o u l d n ' t   a c c e p t   ' u n k n o w n '   a s   I P   a d d r e s s 
 * * S o l u t i o n * * :   C h a n g e d   I P   f a l l b a c k   f r o m   ' u n k n o w n '   t o   ' 1 2 7 . 0 . 0 . 1 '   i n   u i / a u t h _ c o m p o n e n t s . p y 
 
 # # #   K e y   L e s s o n s 
 1 .   * * A l w a y s   c h e c k   p r o d u c t i o n   l o g s   f i r s t * *   -   R e n d e r   l o g s   s h o w e d   t h e   r e a l   e r r o r 
 2 .   * * E n v i r o n m e n t   s e p a r a t i o n   i s   c r i t i c a l * *   -   L o c a l   S Q L i t e     P r o d u c t i o n   P o s t g r e S Q L     
 3 .   * * P o s t g r e S Q L   i s   s t r i c t e r   t h a n   S Q L i t e * *   -   V a l i d a t e s   d a t a   t y p e s   p r o p e r l y 
 4 .   * * R e n d e r   d e p l o y s   f r o m   m a i n   b r a n c h * *   -   M u s t   m e r g e   f e a t u r e   b r a n c h e s   p r o p e r l y 
 5 .   * * O n e   l i n e   c a n   f i x   e v e r y t h i n g * *   -   S i m p l e   c h a n g e   s o l v e d   e n t i r e   l o g i n   s y s t e m 
 
 # # #   T h e   F i x 
 ` p y t h o n 
 #   B E F O R E   ( b r o k e n ) 
 i p _ a d d r e s s = s t . s e s s i o n _ s t a t e . g e t ( ' c l i e n t _ i p ' ,   ' u n k n o w n ' ) 
 #   A F T E R   ( w o r k i n g ) 
 i p _ a d d r e s s = s t . s e s s i o n _ s t a t e . g e t ( ' c l i e n t _ i p ' ,   ' 1 2 7 . 0 . 0 . 1 ' ) 
 ` 
 
 * * R e s u l t * * :     A d m i n   l o g i n   n o w   w o r k s   o n   h t t p s : / / a i - c o a c h e n . o n r e n d e r . c o m / 
  
 