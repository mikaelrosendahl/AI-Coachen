"""
AI Coach - Huvudmodell för intelligent coaching
Kombinerar personlig coaching med universitets AI-implementering
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import openai
from pydantic import BaseModel
import tiktoken

class CoachingMode(Enum):
    PERSONAL = "personal"
    UNIVERSITY = "university"
    HYBRID = "hybrid"

class ConversationRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class CoachingSession:
    session_id: str
    user_id: str
    mode: CoachingMode
    start_time: datetime
    messages: List[Dict]
    context: Dict
    goals: List[str]
    progress_notes: str

class AICoach:
    """Huvudklass för AI-coachen med dubbla roller"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)
        self.max_tokens = 4000
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Coaching personas
        self.personas = {
            CoachingMode.PERSONAL: self._get_personal_coach_persona(),
            CoachingMode.UNIVERSITY: self._get_university_coach_persona(),
            CoachingMode.HYBRID: self._get_hybrid_coach_persona()
        }
        
        # Current session
        self.current_session: Optional[CoachingSession] = None
        
    def _get_personal_coach_persona(self) -> str:
        """Personlig coach-persona"""
        return """
        Du är en erfaren och empatisk personlig coach med expertis inom:
        - Personlig utveckling och målsättning
        - Motivational coaching och accountability
        - Stress-hantering och work-life balance
        - Karriärutveckling och kompetensutveckling
        
        Din approach är:
        - Lyssna aktivt och ställ genomtänkta frågor
        - Hjälp användaren reflektera och hitta sina egna svar
        - Ge konstruktiv feedback och uppmuntran
        - Anpassa din stil till användarens behov
        - Håll koll på framsteg och utmaningar
        
        Kommunicera på svenska med värme och professionalitet.
        """
    
    def _get_university_coach_persona(self) -> str:
        """Universitets AI-implementering coach-persona"""
        return """
        Du är en expert på AI-implementering inom akademisk miljö med djup kunskap om:
        - Strategisk AI-adoption på universitet
        - Forskningsintegration med AI/ML
        - Etiska riktlinjer och compliance inom akademi
        - Change management för teknisk innovation
        - Pedagogisk integration av AI-verktyg
        
        Din expertis inkluderar:
        - AI governance och policy utveckling
        - Forskarträning och capacity building
        - Infrastruktur och teknisk implementation
        - Samarbeten mellan fakulteter och IT
        - Mätning av AI-impact på forskning och utbildning
        
        Ge praktiska, evidensbaserade råd med akademisk rigor.
        Kommunicera på svenska med professionell ton.
        """
    
    def _get_hybrid_coach_persona(self) -> str:
        """Hybrid coach som kombinerar båda rollerna"""
        return """
        Du är en unik AI-coach som kombinerar personlig utveckling med AI-expertis.
        Du hjälper användaren både personligt och professionellt inom AI-implementering på universitet.
        
        Som personlig coach hjälper du med:
        - Ledarskapsutveckling för AI-transformation
        - Hantering av stress och motstånd vid förändring
        - Karriärutveckling inom AI-området
        - Balance mellan innovation och ansvar
        
        Som AI-expert guidar du:
        - Strategisk planering för universitets AI-satsning
        - Praktisk implementering och pilotprojekt
        - Team-building och kompetenslyft
        - Kommunikation med stakeholders
        
        Din unika värde är att förstå både de mänskliga och tekniska aspekterna
        av AI-transformation inom akademi.
        """
    
    def start_session(self, user_id: str, mode: CoachingMode, 
                     context: Dict = None) -> str:
        """Starta en ny coaching-session"""
        session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_session = CoachingSession(
            session_id=session_id,
            user_id=user_id,
            mode=mode,
            start_time=datetime.now(),
            messages=[],
            context=context or {},
            goals=[],
            progress_notes=""
        )
        
        # Lägg till system-prompt baserat på läge
        system_prompt = self.personas[mode]
        self.current_session.messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        self.logger.info(f"Started session {session_id} in {mode.value} mode")
        return session_id
    
    def add_message(self, message: str, role: ConversationRole = ConversationRole.USER) -> str:
        """Lägg till meddelande i sessionen"""
        if not self.current_session:
            raise ValueError("Ingen aktiv session. Starta en session först.")
        
        self.current_session.messages.append({
            "role": role.value,
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        return "Message added successfully"
    
    def get_response(self, user_message: str) -> Tuple[str, Dict]:
        """Få svar från AI-coachen"""
        if not self.current_session:
            raise ValueError("Ingen aktiv session. Starta en session först.")
        
        # Lägg till användarmeddelande
        self.add_message(user_message, ConversationRole.USER)
        
        try:
            # Förbered meddelanden för API-anrop
            messages_for_api = []
            for msg in self.current_session.messages:
                if msg["role"] in ["system", "user", "assistant"]:
                    messages_for_api.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Kontrollera token-längd
            total_tokens = sum(len(self.encoding.encode(msg["content"])) 
                             for msg in messages_for_api)
            
            if total_tokens > self.max_tokens:
                # Trimma historia men behåll system-prompt
                system_msg = messages_for_api[0]
                recent_messages = messages_for_api[-10:]  # Behåll senaste 10
                messages_for_api = [system_msg] + recent_messages
            
            # Anropa OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages_for_api,
                max_tokens=1000,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Spåra API-användning
            from utils.api_usage_tracker import usage_tracker
            api_usage = usage_tracker.track_usage(
                response=response,
                session_id=self.current_session.session_id,
                mode=self.current_session.mode.value,
                model=self.model
            )
            
            # Lägg till assistent-svar
            self.add_message(assistant_response, ConversationRole.ASSISTANT)
            
            # Generera metadata
            metadata = {
                "session_id": self.current_session.session_id,
                "mode": self.current_session.mode.value,
                "message_count": len(self.current_session.messages),
                "timestamp": datetime.now().isoformat(),
                "tokens_used": response.usage.total_tokens if response.usage else None
            }
            
            return assistant_response, metadata
            
        except Exception as e:
            self.logger.error(f"Error getting response: {str(e)}")
            error_response = "Jag beklagar, det uppstod ett fel. Kan du försöka igen?"
            return error_response, {"error": str(e)}
    
    def set_goals(self, goals: List[str]):
        """Sätt mål för sessionen"""
        if not self.current_session:
            raise ValueError("Ingen aktiv session.")
        
        self.current_session.goals = goals
        self.logger.info(f"Set {len(goals)} goals for session {self.current_session.session_id}")
    
    def add_progress_note(self, note: str):
        """Lägg till progress-anteckning"""
        if not self.current_session:
            raise ValueError("Ingen aktiv session.")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.current_session.progress_notes += f"\n[{timestamp}] {note}"
    
    def get_session_summary(self) -> Dict:
        """Få sammanfattning av sessionen"""
        if not self.current_session:
            return {"error": "Ingen aktiv session"}
        
        return {
            "session_id": self.current_session.session_id,
            "mode": self.current_session.mode.value,
            "duration": str(datetime.now() - self.current_session.start_time),
            "message_count": len(self.current_session.messages),
            "goals": self.current_session.goals,
            "progress_notes": self.current_session.progress_notes,
            "context": self.current_session.context
        }
    
    def end_session(self) -> Dict:
        """Avsluta sessionen och få sammanfattning"""
        if not self.current_session:
            return {"error": "Ingen aktiv session att avsluta"}
        
        summary = self.get_session_summary()
        self.logger.info(f"Ended session {self.current_session.session_id}")
        self.current_session = None
        
        return summary

# Factory function för enkel instansiering
def create_ai_coach(api_key: str = None, model: str = "gpt-3.5-turbo") -> AICoach:
    """Skapa AI-coach instans"""
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key krävs")
    
    return AICoach(api_key=api_key, model=model)