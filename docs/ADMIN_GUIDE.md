# 🔑 Admin-funktionalitet Guide
## AI-Coachen Administratörssystem

### 📋 **ÖVERSIKT**

AI-Coachen har nu en komplett admin-funktionalitet som ger dig full kontroll över webbplatsen och bloggen. Som admin har du tillgång till avancerade verktyg för att hantera användare, innehåll och systemfunktioner.

---

## 🚀 **FÖRSTA ADMIN-KONTOT**

### **Automatisk Admin-registrering**
När du startar AI-Coachen första gången och ingen admin finns:

1. **Gå till registreringssidan**
2. **Fyll i dina uppgifter** (förnamn, efternamn, email, lösenord)  
3. **Se admin-erbjudandet**: "⚠️ Ingen admin hittades. Du kan skapa det första admin-kontot."
4. **Kryssa i**: "🔑 Skapa som Admin (webbplats- och bloggadministratör)"
5. **Klicka "Skapa Konto"**

**Din första admin är nu skapad!** 🎉

---

## 🛡️ **ADMIN-PRIVILEGIER**

### **Vad kan du som admin göra?**

**✅ Webbplatsadministration:**
- Hantera alla användarkonton
- Förfram andra användare till admin
- Se användarstatistik och aktivitet
- Övervaka systemhälsa

**✅ Bloggadministration:**
- Skapa och redigera blogginlägg
- Hantera kategorier och taggar
- Publicera och dölj inlägg
- Sätt utvalda (featured) inlägg
- AI-assisterad innehållsförbättring

**✅ Säkerhetsövervakning:**
- Se inloggningsförsök och säkerhetshändelser
- Hantera användarvillkor och GDPR-efterlevnad
- Övervaka systemaktivitet

---

## 🎯 **ADMIN-GRÄNSSNITTET**

### **Admin-menyn**
När du är inloggad som admin ser du:

```
🔑 Admin - Webbplats & Blogg
🎭 Roll: Admin

🔧 Admin-funktioner
├── 📝 Hantera Blogg
├── 👥 Hantera Användare  
└── 📊 Admin Dashboard
```

### **Admin Dashboard**
Klicka på "📊 Admin Dashboard" för att komma åt:

**📈 Statistik:**
- 👥 Totalt antal användare
- 🔑 Antal admins
- 📈 Nya användare (senaste 7 dagarna)

**🛠️ Admin-verktyg:**
- **👥 Användarhantering** - Förfram användare, se alla konton
- **📝 Blogghantering** - Skapa och hantera blogginlägg (tillgängligt via Blog-fliken)
- **📊 Statistik** - Avancerad systemstatistik *(kommer snart)*

---

## � **BLOGGADMINISTRATION**

### **Skapa Blogginlägg**

1. **Gå till Blog-fliken** i huvudnavigeringen
2. **Aktivera Admin-läge** via checkboxen i sidomenyn (visas bara för admins)
3. **Klicka på "📝 Skapa Inlägg"-fliken**
4. **Fyll i formuläret:**
   - **Titel**: Catchy rubrik för ditt inlägg
   - **Kategori**: Välj från coaching, ai-tips, personlig-utveckling, etc.
   - **Taggar**: Kommaseparerade nyckelord
   - **Sammanfattning**: Kort beskrivning (valfritt)
   - **Innehåll**: Huvudtexten för inlägget

5. **Välj inställningar:**
   - ✅ **Publicera direkt** - Gör inlägget synligt på bloggen
   - ✅ **Utvalt inlägg** - Framhäv inlägget som featured
   - ✅ **AI-assistance** - Låt AI förbättra innehållet

6. **Klicka "📝 Skapa Inlägg"**

### **Hantera Befintliga Inlägg**

1. **Gå till "📋 Hantera Inlägg"-fliken**
2. **Se alla inlägg** (även opublicerade utkast)
3. **För varje inlägg kan du:**
   - 📢 **Publicera/Dölj** - Toggle publiceringstatus
   - 🗑️ **Ta bort** - Radera inlägg permanent
   - Se status, datum och kategorier

### **AI-Assisterad Innehållsförbättring**

När du aktiverar "🤖 AI-assistance" vid skapande:
- AI analyserar ditt innehåll och titel
- Förbättrar språk, struktur och flyt
- Optimerar för läsbarhet och engagement
- Lägger till relevant kontext baserat på kategori

---

## �👥 **ANVÄNDARHANTERING**

### **Förfram användare till Admin**

1. **Gå till Admin Dashboard → Användarhantering**
2. **Expandera "🔑 Förfram Användare till Admin"**
3. **Ange användarens email**
4. **Välj roll:**
   - **Admin** - Full kontroll över allt
   - **Moderator** - Kan moderera innehåll
   - **Editor** - Kan redigera blogginlägg
5. **Klicka "Förfram till Admin"**

### **Se alla användare**
- **Expandera "📋 Alla Användare"** för att se:
  - Email och namn
  - Admin-status (🔑 för admin, 👤 för användare)
  - Roll och behörigheter
  - Registreringsdatum
  - Senaste inloggning

---

## 🗃️ **DATABAS & SÄKERHET**

### **Admin-relaterade fält i databasen:**
```sql
-- Nya fält tillagda automatiskt
ALTER TABLE users 
ADD COLUMN is_admin BOOLEAN DEFAULT FALSE,
ADD COLUMN role VARCHAR(20) DEFAULT 'user';
```

### **Admin-roller:**
- **admin** - Full systemkontroll
- **moderator** - Innehållsmoderation
- **editor** - Innehållsredigering
- **user** - Standard användarroll

### **Säkerhet:**
- ✅ Endast befintliga admins kan förframa nya admins
- ✅ Admin-funktioner är dolda för vanliga användare
- ✅ Alla admin-åtgärder loggas för revision
- ✅ Session-baserad åtkomstkontroll

---

## 🔧 **ADMIN-FUNKTIONER** 

### **Nuvarande funktioner (v1.0):**
- ✅ **Första admin-registrering**
- ✅ **Användarstatistik och översikt**
- ✅ **Förfrämning av användare till admin**
- ✅ **Admin dashboard med verktygsöversikt**
- ✅ **Säker rollbaserad åtkomst**
- ✅ **Komplett blogghanteringssystem**
  - Skapa blogginlägg med AI-assistance
  - Hantera kategorier och taggar
  - Publicera/dölj inlägg
  - Sätt utvalda (featured) inlägg
  - Sök och filtrera inlägg

### **Kommande funktioner (v1.1+):**
- 🔄 **Avancerad användarhantering** (inaktivera, radera, etc.)
- 🔄 **Systemkonfiguration** (inställningar, API-nycklar, etc.)
- 🔄 **Backup och återställning**
- 🔄 **Email-notifikationer** till admins
- 🔄 **Audit log** för alla admin-åtgärder
- 🔄 **Kommentarssystem** för blogginlägg
- 🔄 **Schemalagd publicering**

---

## 🚨 **FELSÖKNING**

### **"Admin-checkbox syns inte vid registrering"**
**Orsak:** Det finns redan minst en admin i systemet
**Lösning:** Be en befintlig admin att förframa dig via Admin Dashboard

### **"Kan inte komma åt Admin Dashboard"**
**Orsak:** Du har inte admin-behörighet
**Lösning:** Kontakta en befintlig admin för förfrämning

### **"Får inte admin-menyn efter förfrämning"**
**Orsak:** Din session behöver uppdateras
**Lösning:** Logga ut och logga in igen

### **"Database error vid admin-funktioner"**  
**Orsak:** Databasanslutning eller behörighetsproblem
**Lösning:** Kontrollera DATABASE_URL och att databasen är tillgänglig

---

## 📞 **ADMIN-SUPPORT**

### **För tekniska problem:**
1. **Kontrollera systemloggar** i `logs/ai_coach.log`
2. **Verifiera databasanslutning** och admin-fält
3. **Kör autentiseringstester:** `python test_auth.py`

### **För säkerhetsfrågor:**
- **Rapportera säkerhetsincidenter** omedelbart
- **Övervaka inloggningsförsök** regelbundet
- **Uppdatera admin-lösenord** regelbundet

---

## 🎉 **DU ÄR REDO!**

Som admin av AI-Coachen har du nu:
- ✅ **Full kontroll** över webbplatsen och användare
- ✅ **Säkra admin-verktyg** för daglig hantering  
- ✅ **Bloggadministration** förberedd för framtida innehåll
- ✅ **Skalbar arkitektur** för växande användarantal

**Välkommen som AI-Coachen Admin!** 🚀

---

*Skapat: 2025-10-19 | Version: 1.0 | Säker admin-funktionalitet implementerad*