"""
API Usage Tracker för AI-Coachen
Spårar OpenAI API-användning, kostnader och begränsningar
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import openai
from dataclasses import dataclass

@dataclass
class APIUsage:
    timestamp: datetime
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    session_id: str
    mode: str

class APIUsageTracker:
    """Spårar API-användning och kostnader"""
    
    def __init__(self, usage_file: str = "data/api_usage.json"):
        self.usage_file = usage_file
        self.usage_history: List[APIUsage] = []
        self.load_usage_history()
        
        # OpenAI priser (per 1000 tokens) - uppdatera vid behov
        self.pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
        }
    
    def load_usage_history(self):
        """Ladda användningshistorik från fil"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.usage_history = [
                        APIUsage(
                            timestamp=datetime.fromisoformat(item['timestamp']),
                            model=item['model'],
                            prompt_tokens=item['prompt_tokens'],
                            completion_tokens=item['completion_tokens'],
                            total_tokens=item['total_tokens'],
                            cost_usd=item['cost_usd'],
                            session_id=item['session_id'],
                            mode=item['mode']
                        ) for item in data
                    ]
            except Exception as e:
                print(f"Fel vid laddning av usage history: {e}")
                self.usage_history = []
    
    def save_usage_history(self):
        """Spara användningshistorik till fil"""
        os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
        
        data = [
            {
                'timestamp': usage.timestamp.isoformat(),
                'model': usage.model,
                'prompt_tokens': usage.prompt_tokens,
                'completion_tokens': usage.completion_tokens,
                'total_tokens': usage.total_tokens,
                'cost_usd': usage.cost_usd,
                'session_id': usage.session_id,
                'mode': usage.mode
            } for usage in self.usage_history
        ]
        
        with open(self.usage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Beräkna kostnad för API-anrop"""
        if model not in self.pricing:
            model = "gpt-4"  # Default fallback
        
        prices = self.pricing[model]
        
        input_cost = (prompt_tokens / 1000) * prices["input"]
        output_cost = (completion_tokens / 1000) * prices["output"]
        
        return input_cost + output_cost
    
    def track_usage(self, response, session_id: str, mode: str, model: str = "gpt-4"):
        """Spåra en API-användning"""
        if hasattr(response, 'usage') and response.usage:
            usage = response.usage
            
            cost = self.calculate_cost(
                model=model,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens
            )
            
            api_usage = APIUsage(
                timestamp=datetime.now(),
                model=model,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
                cost_usd=cost,
                session_id=session_id,
                mode=mode
            )
            
            self.usage_history.append(api_usage)
            self.save_usage_history()
            
            return api_usage
        
        return None
    
    def get_daily_usage(self, date: datetime = None) -> Dict:
        """Få användning för en specifik dag"""
        if date is None:
            date = datetime.now()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        daily_usage = [
            u for u in self.usage_history 
            if start_of_day <= u.timestamp < end_of_day
        ]
        
        return {
            'total_requests': len(daily_usage),
            'total_tokens': sum(u.total_tokens for u in daily_usage),
            'total_cost_usd': sum(u.cost_usd for u in daily_usage),
            'total_cost_sek': sum(u.cost_usd for u in daily_usage) * 10.5,  # Ungefär växelkurs
            'by_mode': {
                mode: len([u for u in daily_usage if u.mode == mode])
                for mode in set(u.mode for u in daily_usage)
            }
        }
    
    def get_monthly_usage(self) -> Dict:
        """Få månadens användning"""
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        monthly_usage = [
            u for u in self.usage_history 
            if u.timestamp >= start_of_month
        ]
        
        return {
            'total_requests': len(monthly_usage),
            'total_tokens': sum(u.total_tokens for u in monthly_usage),
            'total_cost_usd': sum(u.cost_usd for u in monthly_usage),
            'total_cost_sek': sum(u.cost_usd for u in monthly_usage) * 10.5,
            'average_cost_per_request': sum(u.cost_usd for u in monthly_usage) / len(monthly_usage) if monthly_usage else 0,
            'days_this_month': (now - start_of_month).days + 1
        }
    
    def check_openai_limits(self) -> Dict:
        """Kontrollera OpenAI-gränser via API"""
        try:
            # Detta kräver att du har tillgång till organization info
            # Annars kan vi bara visa vad vi spårat lokalt
            return {
                "status": "info_not_available",
                "message": "OpenAI visar inte rate limits via API. Kontrollera på platform.openai.com/account/usage"
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Kunde inte hämta OpenAI-gränser: {str(e)}"
            }
    
    def get_usage_summary(self) -> Dict:
        """Få komplett användningssammanfattning"""
        daily = self.get_daily_usage()
        monthly = self.get_monthly_usage()
        
        # Beräkna trend
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_usage = self.get_daily_usage(yesterday)
        
        return {
            'today': daily,
            'yesterday': yesterday_usage,
            'month': monthly,
            'limits': self.check_openai_limits(),
            'recommendations': self._get_recommendations(daily, monthly)
        }
    
    def _get_recommendations(self, daily: Dict, monthly: Dict) -> List[str]:
        """Generera rekommendationer baserat på användning"""
        recommendations = []
        
        if daily['total_cost_usd'] > 5:  # $5 per dag
            recommendations.append("🚨 Hög daglig kostnad! Överväg att begränsa antal meddelanden.")
        
        if monthly['total_cost_usd'] > 50:  # $50 per månad
            recommendations.append("💰 Månadskostnad över $50. Kanske dags att sätta en budget-gräns?")
        
        if daily['total_requests'] > 100:
            recommendations.append("📊 Många requests idag. Kontrollera att du inte kör automatiska loops.")
        
        if len(recommendations) == 0:
            recommendations.append("✅ Användningen ser bra ut! Fortsätt så.")
        
        return recommendations
    
    def export_usage_data(self) -> Dict:
        """Exportera all användningsdata"""
        return {
            'export_date': datetime.now().isoformat(),
            'total_sessions': len(set(u.session_id for u in self.usage_history)),
            'usage_history': [
                {
                    'date': u.timestamp.date().isoformat(),
                    'time': u.timestamp.time().isoformat(),
                    'model': u.model,
                    'tokens': u.total_tokens,
                    'cost_usd': u.cost_usd,
                    'mode': u.mode
                } for u in self.usage_history
            ],
            'summary': self.get_usage_summary()
        }

# Singleton instance för global användning
usage_tracker = APIUsageTracker()