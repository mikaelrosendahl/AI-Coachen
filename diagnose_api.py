#!/usr/bin/env python3
"""
Detaljerad diagnostik av OpenAI API-problem
"""

import os
from dotenv import load_dotenv
import openai
import requests

def detailed_api_diagnosis():
    """Detaljerad analys av API-problem"""
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("🔍 DETALJERAD API-DIAGNOSTIK")
    print("=" * 50)
    
    # 1. Kontrollera API-nyckelformat
    print(f"🔑 API-nyckel längd: {len(api_key) if api_key else 0}")
    print(f"🔑 Börjar med: {api_key[:10] if api_key else 'N/A'}")
    print(f"🔑 Slutar med: {api_key[-10:] if api_key else 'N/A'}")
    
    # 2. Kontrollera om nyckeln är äkta
    if api_key and api_key.startswith('sk-'):
        print("✅ API-nyckel har korrekt format")
    else:
        print("❌ API-nyckel har fel format")
        return
    
    # 3. Testa grundläggande autentisering
    try:
        print("\n🧪 Testar grundläggande autentisering...")
        client = openai.OpenAI(api_key=api_key)
        
        # Försök lista modeller (använder inga tokens)
        models = client.models.list()
        print(f"✅ Autentisering OK - {len(models.data)} modeller tillgängliga")
        
        # Visa några modeller
        available_models = [m.id for m in models.data if 'gpt' in m.id][:5]
        print(f"📋 Tillgängliga GPT-modeller: {available_models}")
        
    except Exception as e:
        print(f"❌ Autentiseringsfel: {e}")
        
        # Kontrollera specifika feltyper
        if "invalid_api_key" in str(e):
            print("🔍 Feltyp: Ogiltig API-nyckel")
        elif "insufficient_quota" in str(e):
            print("🔍 Feltyp: Kvot överskriden")
        elif "rate_limit" in str(e):
            print("🔍 Feltyp: Rate limit")
        return
    
    # 4. Testa minimal förfrågan
    try:
        print("\n🧪 Testar minimal API-förfrågan...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=1  # Minimal användning
        )
        print("✅ API-förfrågan lyckades!")
        print(f"💰 Tokens använda: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"❌ API-förfrågan misslyckades: {e}")
    
    # 5. Kontrollera manuellt via curl (om möjligt)
    print("\n🔧 MANUELL KONTROLL:")
    print("Kör detta kommando i terminal för att kontrollera direkt:")
    print(f'curl -H "Authorization: Bearer {api_key}" https://api.openai.com/v1/models')

if __name__ == "__main__":
    detailed_api_diagnosis()