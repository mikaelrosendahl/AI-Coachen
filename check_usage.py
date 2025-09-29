#!/usr/bin/env python3
"""
Kontrollera OpenAI API-användning och kvotinformation
"""

import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta

def check_usage_and_quota():
    """Kontrollera API-användning och kvot"""
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("💰 KONTROLLERAR API-ANVÄNDNING OCH KVOT")
    print("=" * 50)
    
    # 1. Försök hämta användningsstatistik
    try:
        # Beräkna datum för de senaste 30 dagarna
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        usage_url = f"https://api.openai.com/v1/usage?start_date={start_date}&end_date={end_date}"
        
        print(f"📅 Kontrollerar användning från {start_date} till {end_date}")
        
        response = requests.get(usage_url, headers=headers)
        
        if response.status_code == 200:
            usage_data = response.json()
            print("✅ Användningsdata hämtad!")
            
            total_cost = 0
            total_requests = 0
            
            if 'data' in usage_data:
                for day_data in usage_data['data']:
                    if day_data.get('n_requests', 0) > 0:
                        cost = day_data.get('cost', 0) / 100  # Konvertera från cent
                        requests_count = day_data.get('n_requests', 0)
                        total_cost += cost
                        total_requests += requests_count
                        print(f"📊 {day_data['aggregation_timestamp']}: ${cost:.4f} ({requests_count} requests)")
            
            print(f"\n💵 Total kostnad senaste 30 dagarna: ${total_cost:.4f}")
            print(f"📋 Totalt antal requests: {total_requests}")
            
        else:
            print(f"❌ Kunde inte hämta användningsdata: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Fel vid hämtning av användningsdata: {e}")
    
    # 2. Kontrollera konto-information
    try:
        print(f"\n🏦 KONTOINFORMATION")
        print("-" * 30)
        
        # Detta endpoint kanske inte finns, men vi testar
        billing_url = "https://api.openai.com/v1/dashboard/billing/subscription"
        response = requests.get(billing_url, headers=headers)
        
        if response.status_code == 200:
            billing_data = response.json()
            print("✅ Faktureringsinformation hämtad!")
            print(json.dumps(billing_data, indent=2))
        else:
            print(f"ℹ️ Faktureringsinformation inte tillgänglig via API")
            
    except Exception as e:
        print(f"ℹ️ Kunde inte hämta faktureringsinformation: {e}")
    
    # 3. Ge rekommendationer
    print(f"\n🎯 REKOMMENDATIONER")
    print("-" * 30)
    print("1. Logga in på https://platform.openai.com/account/billing")
    print("2. Kontrollera 'Usage' för att se exakt användning")
    print("3. Kontrollera 'Billing' för betalningsmetoder och begränsningar")
    print("4. Kolla om du har 'Free tier' credits kvar")
    print("5. Kontrollera om det finns spending limits satta")

if __name__ == "__main__":
    check_usage_and_quota()