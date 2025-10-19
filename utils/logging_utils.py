# -*- coding: utf-8 -*-
"""
Logging utilities för AI-Coachen
"""

import logging
import os
from datetime import datetime
from typing import Optional

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Konfigurera logging för AI-coachen"""
    
    # Skapa logs directory om det inte finns
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Konvertera log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Konfigurera logging
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler(log_file) if log_file else logging.NullHandler()
        ]
    )
    
    logger = logging.getLogger("AICoach")
    logger.info(f"Logging initialized at level {log_level}")
    
    return logger

def log_session_event(logger: logging.Logger, session_id: str, event: str, details: str = ""):
    """Logga session-händelse"""
    logger.info(f"Session {session_id}: {event} - {details}")

def log_coaching_interaction(logger: logging.Logger, session_id: str, mode: str, 
                           user_input_length: int, response_length: int):
    """Logga coaching-interaktion"""
    logger.info(f"Coaching interaction - Session: {session_id}, Mode: {mode}, "
                f"Input: {user_input_length} chars, Response: {response_length} chars")

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Logga fel med kontext"""
    logger.error(f"Error in {context}: {type(error).__name__}: {str(error)}")

def log_performance_metric(logger: logging.Logger, metric_name: str, value: float, unit: str = ""):
    """Logga prestandametrik"""
    logger.info(f"Performance metric - {metric_name}: {value} {unit}")

class SessionLogger:
    """Logger för coaching sessions"""
    
    def __init__(self, session_id: str, base_logger: logging.Logger):
        self.session_id = session_id
        self.logger = base_logger
        self.start_time = datetime.now()
        
    def log_message(self, role: str, message_length: int):
        """Logga meddelande"""
        self.logger.debug(f"Session {self.session_id} - {role} message: {message_length} chars")
    
    def log_goal_created(self, goal_title: str):
        """Logga att mål skapats"""
        self.logger.info(f"Session {self.session_id} - Goal created: {goal_title}")
    
    def log_reflection_added(self, mood: int, energy: int):
        """Logga reflektion"""
        self.logger.info(f"Session {self.session_id} - Reflection added: mood={mood}, energy={energy}")
    
    def log_project_created(self, project_title: str, use_case: str):
        """Logga AI-projekt"""
        self.logger.info(f"Session {self.session_id} - AI Project created: {project_title} ({use_case})")
    
    def log_session_end(self):
        """Logga session-slut"""
        duration = datetime.now() - self.start_time
        self.logger.info(f"Session {self.session_id} ended - Duration: {duration}")