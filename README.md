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