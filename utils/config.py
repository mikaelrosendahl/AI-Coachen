"""
Configuration utilities för AI-Coachen
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Ladda environment variables
load_dotenv()

class Config:
    """Konfigurationsklass för AI-Coachen"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/coach_data.db")
    
    # Coaching settings
    DEFAULT_COACHING_MODE = os.getenv("DEFAULT_COACHING_MODE", "hybrid")
    ENABLE_MEMORY = os.getenv("ENABLE_MEMORY", "true").lower() == "true"
    CONVERSATION_HISTORY_LIMIT = int(os.getenv("CONVERSATION_HISTORY_LIMIT", "50"))
    
    # University settings
    UNIVERSITY_NAME = os.getenv("UNIVERSITY_NAME", "Your University")
    RESEARCH_FOCUS_AREAS = os.getenv("RESEARCH_FOCUS_AREAS", "AI,ML,NLP").split(",")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/coach.log")
    
    # AI Model settings
    AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validera konfiguration"""
        issues = []
        warnings = []
        
        # Kontrollera API keys
        if not cls.OPENAI_API_KEY:
            issues.append("OPENAI_API_KEY saknas - AI-funktioner kommer inte fungera")
        
        # Kontrollera paths
        if not os.path.exists(os.path.dirname(cls.DATABASE_PATH)):
            warnings.append(f"Database directory {os.path.dirname(cls.DATABASE_PATH)} finns inte ännu")
        
        if not os.path.exists(os.path.dirname(cls.LOG_FILE)):
            warnings.append(f"Log directory {os.path.dirname(cls.LOG_FILE)} finns inte ännu")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    @classmethod
    def get_summary(cls) -> Dict[str, Any]:
        """Få sammanfattning av konfiguration"""
        return {
            "ai_model": cls.AI_MODEL,
            "database_path": cls.DATABASE_PATH,
            "default_mode": cls.DEFAULT_COACHING_MODE,
            "memory_enabled": cls.ENABLE_MEMORY,
            "university": cls.UNIVERSITY_NAME,
            "research_areas": cls.RESEARCH_FOCUS_AREAS,
            "has_openai_key": bool(cls.OPENAI_API_KEY),
            "log_level": cls.LOG_LEVEL
        }