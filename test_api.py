#!/usr/bin/env python3
"""
Snabb test för att verifiera OpenAI API-anslutning
"""

import os
from dotenv import load_dotenv
import openai

def test_openai_connection():
    """Testa OpenAI API-anslutning"""
    
    # Ladda environment variables
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    
    print(f"🔑 API Key: {api_key[:8]}...{api_key[-8:] if api_key else 'NOT FOUND'}")
    print(f"🤖 Model: {model}")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ Fel: API-nyckel inte konfigurerad korrekt")
        return False
    
    try:
        # Skapa OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Testa enkel förfrågan
        print("🧪 Testar API-anslutning...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Du är en hjälpsam AI-assistent."},
                {"role": "user", "content": "Säg bara 'Hej, API fungerar!'"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API-test lyckades!")
        print(f"📝 Svar: {result}")
        print(f"💰 Tokens: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ API-test misslyckades: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testar OpenAI API-anslutning för AI-Coachen\n")
    success = test_openai_connection()
    
    if success:
        print("\n🎉 Allt fungerar! Du kan nu använda AI-Coachen.")
    else:
        print("\n⚠️ Det finns problem som behöver åtgärdas.")
        print("📖 Kontrollera .env-filen och API-nyckeln.")