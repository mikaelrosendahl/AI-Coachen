# 🚀 Deployment Guide: AI-Coachen på Render

Detta dokument beskriver hur du deployar AI-Coachen på Render molnplattform.

## Översikt

Render är en modern molnplattform som gör det enkelt att deploya webbapplikationer. AI-Coachen är konfigurerad för att fungera optimalt på Render med automatisk deployment från GitHub.

## 📋 Förutsättningar

1. **Render-konto**: Skapa gratis konto på [render.com](https://render.com)
2. **GitHub repository**: AI-Coachen måste finnas på GitHub
3. **OpenAI API-nyckel**: För AI-funktionalitet

## 🚀 Steg-för-steg Deployment

### Steg 1: Förbereda Repository

Säkerställ att följande filer finns i ditt repository:

```
AI-Coachen/
├── render.yaml              # Render konfiguration
├── start.sh                 # Startup script  
├── requirements.txt         # Python dependencies
├── .streamlit/config.toml   # Streamlit konfiguration
├── main.py                  # Huvudapplikation
└── ... (övriga filer)
```

### Steg 2: Skapa Web Service på Render

1. **Logga in på Render Dashboard**
   - Gå till [dashboard.render.com](https://dashboard.render.com)

2. **Skapa ny Web Service**
   - Klicka "New +" → "Web Service"
   - Välj "Build and deploy from a Git repository"

3. **Anslut GitHub Repository**
   - Välj ditt AI-Coachen repository
   - Klicka "Connect"

### Steg 3: Konfigurera Service

#### Grundläggande inställningar:
- **Name**: `ai-coachen` (eller ditt val)
- **Region**: Välj närmaste region
- **Branch**: `main`
- **Root Directory**: Lämna tomt (om AI-Coachen är i root)

#### Build & Deploy inställningar:
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
  ```

#### Alternativt - Använd render.yaml:
Om du har `render.yaml` i repository kommer Render automatiskt läsa konfigurationen därifrån.

### Steg 4: Konfigurera Environment Variables

I Render Dashboard under "Environment":

#### Obligatoriska variabler:
```
OPENAI_API_KEY = din_openai_api_nyckel
PYTHONUNBUFFERED = 1
```

#### Valfria variabler:
```
ENVIRONMENT = production
DEBUG = false
STREAMLIT_SERVER_HEADLESS = true
STREAMLIT_BROWSER_GATHER_USAGE_STATS = false
```

### Steg 5: Deploy

1. **Starta deployment**
   - Klicka "Create Web Service"
   - Render börjar bygga och deploya automatiskt

2. **Övervaka deployment**
   - Följ build-loggar i real-time
   - Deployment tar vanligtvis 3-5 minuter

3. **Testa applikationen**
   - När deployment är klar får du en URL (ex: `https://ai-coachen.online`)
   - Klicka på länken för att testa

## 🔧 Render-specifik Konfiguration

### render.yaml
```yaml
services:
  - type: web
    name: ai-coachen
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
    envVars:
      - key: PYTHONUNBUFFERED
        value: 1
      - key: OPENAI_API_KEY
        sync: false
    autoDeploy: true
```

### Streamlit Konfiguration (.streamlit/config.toml)
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false
fileWatcherType = "none"

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 💰 Kostnad och Begränsningar

### Free Plan (Gratis)
- **Tillgängligt**: 750 timmar/månad
- **RAM**: 512 MB
- **CPU**: Delad
- **Sovläge**: Efter 15 min inaktivitet
- **Kostnad**: $0

### Starter Plan ($7/månad)
- **RAM**: 512 MB  
- **CPU**: Delad
- **Ingen sovläge**: Alltid tillgänglig
- **Kostnad**: $7/månad

### Standard Plan ($25/månad)
- **RAM**: 2 GB
- **CPU**: 1 vCPU
- **Prestanda**: Bättre för flera användare
- **Kostnad**: $25/månad

## 🔄 Automatisk Deployment

### GitHub Integration
- **Auto-deploy**: Aktiverat via `render.yaml`
- **Trigger**: Vid push till `main` branch
- **Process**: Automatisk build och deployment

### Manual Deployment
```bash
# Uppdatera kod lokalt
git add .
git commit -m "Update AI-Coachen"
git push origin main

# Render deployar automatiskt
```

## 🛠️ Felsökning

### Vanliga problem och lösningar:

#### 1. Build Failed - Dependencies
```bash
# Lösning: Kontrollera requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

#### 2. App inte tillgänglig
- Kontrollera att `PORT` environment variable används
- Säkerställ att startkommandot är korrekt
- Kolla build-loggar för fel

#### 3. API-fel
```bash
# Kontrollera environment variables
echo $OPENAI_API_KEY  # Ska inte vara tom
```

#### 4. Prestanda problem på Free Plan
- Applikationen "sover" efter 15 min inaktivitet
- Första förfrågan efter sovläge tar längre tid
- Överväg uppgradering till Starter Plan

### Debug-kommandon
```bash
# Kolla miljövariabler (lägg till i main.py temporärt)
import os
st.write("Environment variables:")
st.write(f"PORT: {os.getenv('PORT')}")
st.write(f"RENDER: {os.getenv('RENDER')}")
st.write(f"OPENAI_API_KEY set: {bool(os.getenv('OPENAI_API_KEY'))}")
```

## 📊 Monitoring och Underhåll

### Render Dashboard
- **Metrics**: CPU, Memory, Request volume
- **Logs**: Real-time applikationsloggar  
- **Deploy History**: Tidigare deployments
- **Settings**: Konfigurera service

### Performance Tips
1. **Optimera Streamlit**:
   ```python
   # Använd session state för tunga beräkningar
   @st.cache_data
   def expensive_function():
       # ... kod ...
   ```

2. **Database optimering**:
   - SQLite fungerar bra för free plan
   - Överväg PostgreSQL för högre trafik

3. **API optimering**:
   - Implementera rate limiting
   - Cache API-svar när möjligt

## 🔗 Användbara Länkar

- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-python)  
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)
- [Render Status Page](https://status.render.com)

## 🆘 Support

### Render Support
- **Dokumentation**: [render.com/docs](https://render.com/docs)
- **Community**: [community.render.com](https://community.render.com)
- **Support**: Via dashboard för betalda planer

### AI-Coachen Support
- **GitHub Issues**: [github.com/mikaelrosendahl/AI-Coachen/issues](https://github.com/mikaelrosendahl/AI-Coachen/issues)
- **Documentation**: Se README.md och docs/

---

## ✅ Deployment Checklist

- [ ] Repository finns på GitHub
- [ ] `render.yaml` konfigurerad
- [ ] `requirements.txt` uppdaterad
- [ ] `.streamlit/config.toml` skapad
- [ ] Render-konto skapat
- [ ] Web Service konfigurerad
- [ ] Environment variables inställda
- [ ] OpenAI API-nyckel konfigurerad
- [ ] Deployment lyckad
- [ ] Applikation testad
- [ ] Auto-deploy aktiverat

**🎉 Grattis! AI-Coachen är nu live på Render!** 

URL: `https://ditt-service-namn.onrender.com`  # Behåll onrender exempel men använd ny custom domain för produktion, t.ex. https://ai-coachen.online