# 🚀 GitHub Setup Guide för AI-Coachen

## Steg 1: Skapa nytt repository på GitHub

1. Gå till [GitHub.com](https://github.com) och logga in
2. Klicka på "New" eller "+" → "New repository"  
3. Fyll i repository-information:
   - **Repository name**: `AI-Coachen`
   - **Description**: `🤖🎓 Intelligent AI-coach för personlig utveckling och universitets AI-implementering`
   - **Visibility**: Public (eller Private om du föredrar)
   - **VIKTIGT**: ✅ **KRYSSA INTE I** "Add a README file", "Add .gitignore", eller "Choose a license" 
     (Vi har redan dessa filer lokalt)

4. Klicka "Create repository"

## Steg 2: Länka lokalt repository till GitHub

Efter att du skapat repository på GitHub, kopiera kommandona som visas under "…or push an existing repository from the command line":

```bash
git remote add origin https://github.com/mikaelrosendahl/AI-Coachen.git
git branch -M main
git push -u origin main
```

**Eller kör dessa kommandon i terminalen:**

```powershell
# Lägg till GitHub som remote origin
git remote add origin https://github.com/mikaelrosendahl/AI-Coachen.git

# Byt till main branch (modern standard)
git branch -M main  

# Push till GitHub
git push -u origin main
```

## Steg 3: Verifiera Upload

1. Gå tillbaka till ditt GitHub repository
2. Uppdatera sidan - du ska nu se alla filer
3. Kontrollera att README.md visas korrekt med all formattering
4. Verifiera att .gitignore fungerar (inga .env-filer eller databaser ska synas)

## 🎉 Klart!

Ditt AI-Coachen projekt är nu på GitHub och redo för:
- ✅ Samarbete med andra utvecklare
- ✅ Version control och backup  
- ✅ Issue tracking och project management
- ✅ Automatiska workflows (CI/CD)
- ✅ Delning och distribution

## Nästa steg: Sätt upp API-nycklar

Nu när projektet är säkert på GitHub kan vi sätta upp API-nycklarna lokalt:

```bash
# Kopiera environment template
cp .env.example .env

# Redigera .env och lägg till din OpenAI API-nyckel
# OPENAI_API_KEY=sk-...your-key-here
```

**VIKTIGT**: `.env` filen är redan i `.gitignore` så dina API-nycklar kommer aldrig att committas till GitHub! 🔒

## Framtida utveckling

För fortsatt utveckling:

```bash
# Hämta ändringar från GitHub
git pull origin main

# Gör ändringar...

# Commita och pusha ändringar  
git add .
git commit -m "Beskrivning av ändring"
git push origin main
```

Lycka till med ditt AI-Coachen projekt på GitHub! 🚀