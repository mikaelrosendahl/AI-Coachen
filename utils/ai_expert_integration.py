"""
AI Expert Integration Layer
Integrerar AI-expertis i befintliga coaching-personas utan att öka API-kostnader
Använder RAG-system för att berika coaching med relevant AI-kunskap
"""

import logging
from typing import Dict, Optional
from enum import Enum

from .rag_system import rag_system

class AIExpertiseLevel(Enum):
    """Nivåer av AI-expertis baserat på användarfråga"""
    BASIC = "basic"           # Grundläggande AI-koncept
    INTERMEDIATE = "intermediate"  # Praktisk implementation
    ADVANCED = "advanced"     # Strategisk/teknisk djup
    EXPERT = "expert"        # Cutting-edge och forskning

class AIExpertIntegration:
    """Integration layer för AI-expertis i coaching"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def detect_expertise_level(self, user_query: str) -> AIExpertiseLevel:
        """Identifiera lämplig expertisnivå baserat på användarfråga"""
        query_lower = user_query.lower()
        
        # Advanced/Expert indicators
        advanced_terms = [
            'transformer architecture', 'attention mechanism', 'gradient descent',
            'backpropagation', 'hyperparameter tuning', 'model architecture',
            'research paper', 'state-of-the-art', 'benchmark', 'ablation study'
        ]
        
        # Technical/Strategic indicators  
        intermediate_terms = [
            'implementation', 'deploy', 'production', 'mlops', 'api integration',
            'business case', 'roi', 'transformation roadmap', 'pilot project',
            'cloud services', 'data pipeline', 'model training'
        ]
        
        # Basic learning indicators
        basic_terms = [
            'vad är', 'what is', 'grundläggande', 'basics', 'introduction', 
            'förklara', 'explain', 'skillnad mellan', 'difference between',
            'komma igång', 'getting started', 'learn', 'lära mig'
        ]
        
        # Kolla efter avancerade termer
        if any(term in query_lower for term in advanced_terms):
            return AIExpertiseLevel.EXPERT
            
        # Kolla efter tekniska/strategiska termer
        if any(term in query_lower for term in intermediate_terms):
            return AIExpertiseLevel.ADVANCED
            
        # Kolla efter grundläggande termer
        if any(term in query_lower for term in basic_terms):
            return AIExpertiseLevel.BASIC
            
        # Default till intermediate om inget hittas
        return AIExpertiseLevel.INTERMEDIATE
    
    def enhance_coaching_persona(self, base_persona: str, user_query: str, mode: str = "personal") -> str:
        """Förbättra coaching-persona med AI-expertis när det behövs"""
        
        # Kontrollera om AI-expertis behövs
        if not rag_system.is_ai_related_query(user_query):
            return base_persona
        
        expertise_level = self.detect_expertise_level(user_query)
        
        # Lägg till AI-expertis till persona baserat på nivå och mode
        ai_expertise_addon = self._get_ai_expertise_addon(expertise_level, mode)
        
        enhanced_persona = f"""{base_persona}

## AI-Expertis Enhancement
{ai_expertise_addon}

**Integration approach**: Kombinera din coaching-expertis med AI-kunskap genom att:
- Ställa reflekterande frågor som hjälper användaren tänka igenom AI-beslut
- Ge praktisk vägledning baserad på användarens kontext och mognadsnivå
- Balansera teknisk information med personlig utveckling och coaching
- Hjälpa användaren utveckla AI-kompetens steg för steg
- Fokusera på användbar, actionable rådgivning snarare än bara teoretisk kunskap
"""
        
        self.logger.info(f"Förbättrade coaching-persona med AI-expertis på {expertise_level.value} nivå")
        return enhanced_persona
    
    def _get_ai_expertise_addon(self, level: AIExpertiseLevel, mode: str) -> str:
        """Skapa AI-expertis tillägg baserat på nivå och mode"""
        
        base_ai_knowledge = """
        Du har djup expertis inom AI och machine learning, inklusive:
        - Moderna AI-modeller (LLMs, Transformers, Generativ AI)
        - Praktisk AI-implementation och MLOps
        - AI-strategi och business transformation
        - Ethical AI och responsible deployment
        """
        
        level_specific = {
            AIExpertiseLevel.BASIC: """
            **Fokus för grundläggande frågor**:
            - Förklara komplexa AI-koncept med enkla, relatable exempel
            - Hjälp användaren bygga AI-förståelse steg för steg
            - Koppla AI-teorier till praktiska tillämpningar
            - Uppmuntra nyfikenhet och fortsatt lärande
            - Ge rekommendationer för nästa steg i AI-journey
            """,
            
            AIExpertiseLevel.INTERMEDIATE: """
            **Fokus för praktisk implementation**:
            - Ge konkret vägledning för AI-projekt och implementation
            - Hjälp med verktygsval och tekniska beslut
            - Diskutera best practices och vanliga fallgropar
            - Stötta projekt-planning och risk-bedömning
            - Balansera tekniska och affärsmässiga överväganden
            """,
            
            AIExpertiseLevel.ADVANCED: """
            **Fokus för strategisk och teknisk djup**:
            - Fördjupa diskussioner om AI-arkitektur och design decisions
            - Ge strategisk vägledning för AI-transformation
            - Diskutera industry trends och emerging technologies
            - Hjälpa med complex technical challenges
            - Stötta ledarskap i AI-relaterade beslut
            """,
            
            AIExpertiseLevel.EXPERT: """
            **Fokus för cutting-edge expertis**:
            - Diskutera latest research och state-of-the-art techniques  
            - Ge insikter om emerging AI paradigms
            - Stötta innovation och experimentation
            - Hjälpa med forskningsfrågor och advanced implementations
            - Balansera teoretisk fördjupning med praktisk applicering
            """
        }
        
        mode_specific = ""
        if mode == "university":
            mode_specific = """
            **Universitets-specifik AI-expertis**:
            - Academic research applications av AI
            - Learning analytics och educational technology
            - AI governance och policy development för universitet
            - Forskningsintegritet och ethical considerations
            - Faculty training och capacity building för AI
            """
        elif mode == "personal":
            mode_specific = """
            **Personlig AI-utveckling**:
            - Individuell AI-kompetensbyggande
            - Career development inom AI-området
            - Personliga AI-projekt och portfolioutveckling
            - Networking och community building inom AI
            - Balans mellan teknisk och business-orienterad AI-kunskap
            """
        
        return f"{base_ai_knowledge}\n{level_specific[level]}\n{mode_specific}"
    
    def create_enhanced_prompt(self, base_persona: str, user_query: str, mode: str = "personal") -> str:
        """Skapa fullt förbättrat prompt med AI-expertis och RAG-kontext"""
        
        # Förbättra persona med AI-expertis
        enhanced_persona = self.enhance_coaching_persona(base_persona, user_query, mode)
        
        # Lägg till RAG-kontext genom RAG-systemet
        final_prompt = rag_system.enhance_prompt_with_context(enhanced_persona, user_query)
        
        return final_prompt
    
    def get_ai_coaching_guidelines(self, expertise_level: AIExpertiseLevel) -> Dict[str, str]:
        """Hämta coaching-riktlinjer baserat på AI-expertisnivå"""
        
        guidelines = {
            AIExpertiseLevel.BASIC: {
                "tone": "Pedagogisk och uppmuntrande, använd enkla förklaringar",
                "approach": "Bygg förståelse steg för steg, använd analogier och exempel",
                "focus": "Grundläggande koncept och praktiska tillämpningar",
                "questions": "Vad vill du uppnå med AI? Vilken är din bakgrund inom tech?"
            },
            
            AIExpertiseLevel.INTERMEDIATE: {
                "tone": "Praktisk och handledande, fokusera på implementation",
                "approach": "Ge konkreta steg och best practices, diskutera alternativ",
                "focus": "Implementation, verktyg och projektledning",
                "questions": "Vad är dina specifika utmaningar? Vilka resurser har du tillgängliga?"
            },
            
            AIExpertiseLevel.ADVANCED: {
                "tone": "Strategisk och djupgående, diskutera komplexitet",
                "approach": "Analysera pros/cons, diskutera industry context",
                "focus": "Arkitektur, strategi och transformation",
                "questions": "Vad är era strategiska mål? Hur ser organisationens AI-mognad ut?"
            },
            
            AIExpertiseLevel.EXPERT: {
                "tone": "Kollegial och forskningsorienterad, diskutera cutting-edge",
                "approach": "Djupgående teknisk diskussion, explore innovation",
                "focus": "Research, innovation och state-of-the-art",
                "questions": "Vilka forskningsfrågor utforskar ni? Vad är era hypoteser?"
            }
        }
        
        return guidelines[expertise_level]

# Globalt integration instance
ai_expert_integration = AIExpertIntegration()