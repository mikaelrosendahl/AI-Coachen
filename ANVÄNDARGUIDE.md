# 🤖🎓 AI-Coachen - Komplett Användarguide

## Överblick

AI-Coachen är en egenutvecklad intelligent coach som kombinerar personlig utveckling med expertis inom AI-implementering på universitet. Den fungerar som både din personliga mentor och strategisk rådgivare för AI-transformation inom akademisk miljö.

## 🎯 Huvudfunktioner

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

## 🚀 Installation och Setup

### Snabb Start (Windows)
1. Dubbelklicka på `start_coach.bat`
2. Följ instruktionerna för att sätta upp environment
3. Lägg till din OpenAI API-nyckel i `.env` filen
4. Applikationen startar automatiskt i din webbläsare

### Manuell Installation
```bash
# 1. Klona eller ladda ner projektet
git clone [repository-url]
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

# 6. Redigera .env och lägg till din OpenAI API-nyckel
# OPENAI_API_KEY=your_api_key_here

# 7. Testa systemet (valfritt)
python demo_ai_coach.py

# 8. Starta applikationen
streamlit run main.py
```

## 📖 Användarguide

### Första Användning

1. **Välj Coaching-läge**:
   - **Personlig Coach**: Fokus på personlig utveckling
   - **Universitets AI-Coach**: AI-implementering på universitet
   - **Hybrid**: Kombinerar båda (rekommenderas)

2. **Starta Session**: Klicka "Starta Coaching-Session" för att börja

3. **Utforska Funktioner**: Använd flikarna för att navigera mellan olika funktioner

### Personlig Coaching

#### Sätta Mål
1. Gå till fliken "🎯 Mål" 
2. Klicka "➕ Skapa Nytt Mål"
3. Fyll i målinformation:
   - Titel och beskrivning
   - Måltyp (Karriär, Hälsa, Lärande, etc.)
   - Slutdatum (valfritt)
   - Framgångskriterier
4. Klicka "Skapa Mål"

#### Uppdatera Framsteg
1. Se dina aktiva mål i "🎯 Mål" fliken
2. Använd progress-slidern för att uppdatera framsteg
3. Lägg till kommentarer och milstolpar
4. Systemet spårar automatiskt din utveckling

#### Reflektioner
1. Gå till "📝 Reflektion" fliken
2. Välj en reflektionsfråga eller skriv egen
3. Svara genomtänkt på frågan
4. Betygsätt ditt humör och energinivå (1-10)
5. Lägg till insikter du fått
6. Spara reflektionen

### Universitets AI-Coaching

#### Sätta Universitetsprofil
1. Första gången du använder universitets-funktioner
2. Fyll i information om ditt universitet:
   - Namn och storlek
   - Forskningsfokus
   - Nuvarande AI-mognad (1-10)
   - Budget och utmaningar

#### Skapa AI-Projekt
1. Gå till "🏗️ Projekt" fliken
2. Klicka "➕ Skapa Nytt AI-Projekt"
3. Definiera projekt:
   - Titel och beskrivning
   - AI Use Case (forskningsaccelleration, automatiserad rättning, etc.)
   - Involverade stakeholders
   - Slutdatum
4. Projekt skapas i "Assessment" fas

#### Hantera Projektframsteg
1. Se aktiva projekt i "🏗️ Projekt" fliken
2. Klicka "Nästa Fas" för att avancera projekt genom:
   - Assessment → Strategy → Pilot → Deployment → Scaling → Optimization
3. Lägg till kommentarer för varje fasövergång

#### Utmaningshantering
1. Gå till "⚠️ Utmaningar" fliken
2. Rapportera implementationsutmaningar:
   - Tekniska, organisatoriska, finansiella, eller etiska
   - Allvarlighetsgrad (1-10)
   - Påverkade stakeholders
3. Föreslå och diskutera lösningar
4. Spåra utmaningarnas status

### Chat-Funktionen

#### Intelligent Konversation
1. Använd "💬 Chat" fliken för direkt coaching
2. Skriv dina frågor eller concerns
3. AI-coachen svarar baserat på valt läge:
   - Personliga coaching-frågor
   - Strategiska AI-implementerings-frågor  
   - Hybrid coaching för båda områden

#### Föreslagna Prompts
- Systemet föreslår relevanta frågor baserat på:
  - Dina aktiva mål och framsteg
  - Pågående AI-projekt
  - Identifierade utmaningar
- Klicka på förslag för att snabbt starta konversationer

## 📊 Dashboard och Analys

### Progress Tracking
- **Personlig**: Se målframsteg, completion rates, mood/energy trends
- **Universitets**: Projektfaser, utmaningsstatus, AI-mognadsgrad
- **Hybrid**: Kombinerad vy av personlig utveckling och AI-implementering

### Rapporter och Insikter
- Automatiskt genererade råd baserat på dina mönster
- Personaliserade utvecklingsrekommendationer  
- Universitets-specifika implementeringsstrategier
- Stakeholder-anpassade kommunikationsplaner

## 🔧 Avancerade Funktioner

### Dataexport
```python
# Exportera personlig data
personal_data = session_state.personal_coach.export_data()

# Exportera universitets data  
university_data = session_state.university_coach.export_university_data()
```

### Custom Prompts
Systemet lär sig från dina interaktioner och anpassar coaching-prompts över tid.

### Integration Möjligheter
Arkitekturen stödjer integration med:
- LMS (Learning Management Systems)
- Universitets databaser
- Externa AI-verktyg och API:er
- Projekthanteringssystem

## 🛠️ Teknisk Information

### Systemkrav
- Python 3.8+
- 4GB RAM minimum
- Internetanslutning för AI-funktioner
- Modern webbläsare

### Arkitektur
```
AI-Coachen/
├── core/                   # Kärnfunktionalitet
│   ├── ai_coach.py        # Huvudcoach-modell  
│   ├── personal_coach.py  # Personlig coaching
│   └── university_coach.py # Universitets-coaching
├── data/                   # SQLite databas
├── ui/                     # Streamlit interface
├── utils/                  # Utilities och config
└── logs/                   # Systemloggar
```

### API-beroenden
- **OpenAI GPT-4**: För naturlig språkbehandling och coaching-svar
- **Streamlit**: Webbapplikations-framework
- **SQLite**: Lokal datalagring

## 🔒 Säkerhet och Integritet

### Datahantering
- All personlig data lagras lokalt i SQLite databas
- Inga känsliga data delas med externa tjänster utom OpenAI för AI-svar
- Användardata kan exporteras och raderas när som helst

### API-säkerhet
- API-nycklar lagras i lokal `.env` fil
- Ingen logging av API-nycklar eller användardata i klartext
- HTTPS används för alla externa API-anrop

## 🆘 Felsökning

### Vanliga Problem

**Problem**: "Import errors" när du startar
**Lösning**: Kontrollera att virtual environment är aktiverat och dependencies installerade

**Problem**: "OpenAI API error"
**Lösning**: Verifiera att OPENAI_API_KEY är korrekt satt i .env filen

**Problem**: Streamlit startar inte
**Lösning**: Kör `pip install streamlit` och försök igen

**Problem**: Database errors
**Lösning**: Radera `data/coach_data.db` för att återställa databasen

### Kontakt och Support

För teknisk support eller feature requests:
1. Kör `python demo_ai_coach.py` för att testa grundfunktioner
2. Kontrollera `logs/coach.log` för felmeddelanden
3. Skapa issue i GitHub repository (om tillgängligt)

## 🎯 Användningsfall och Exempel

### Scenario 1: Personlig AI-utveckling
- **Mål**: Lära sig AI/ML för karriärutveckling
- **Coaching**: Sätt SMART-mål, reflektion över lärande, motivationsstöd
- **Outcome**: Strukturerad utvecklingsplan med progress tracking

### Scenario 2: Universitets AI-transformation
- **Utmaning**: Implementera AI-verktyg för forskning och undervisning
- **Coaching**: Stakeholder-analys, change management, pilotprojekt
- **Outcome**: Systematisk roadmap för AI-adoption

### Scenario 3: Hybrid ledarskap
- **Kontext**: Du leder AI-implementering medan du utvecklar egna AI-kunskaper
- **Coaching**: Balansera personlig utveckling med organisatoriska krav
- **Outcome**: Integrerad approach för både personlig och professionell framgång

## 🚀 Nästa Steg

1. **Utforska Demo**: Kör `python demo_ai_coach.py` för att se alla funktioner
2. **Sätt ditt första mål**: Börja med personlig coaching
3. **Definiera AI-vision**: Om du arbetar på universitet, starta med strategisk planering
4. **Experimentera**: Testa olika coaching-lägen för att hitta vad som fungerar bäst
5. **Iterera**: Använd insikter från systemet för kontinuerlig förbättring

Lycka till med din AI-coaching resa! 🤖🎓✨