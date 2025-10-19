"""
Secure authentication management for AI-Coachen
Handles login, registration and session security
"""

import bcrypt
import uuid
import re
import time
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.logging_utils import setup_logger

# Setup logger
logger = setup_logger()

@dataclass
class User:
    """Dataclass for User objects"""
    id: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    subscription_tier: str = "free"
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    email_verified: bool = False

class AuthManager:
    """Manages all authentication and session management"""
    
    def __init__(self, database_url: str = None):
        """Initialize AuthManager with database connection"""
        self.database_url = database_url or os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL must be set")
            
        # Security settings
        self.min_password_length = 8
        self.require_uppercase = True
        self.require_lowercase = True  
        self.require_digit = True
        self.require_special = True
        self.session_timeout = timedelta(hours=24)
        self.max_login_attempts = 5
        self.lockout_duration = timedelta(minutes=30)
        
        # Initialize database
        self._init_database()
        
        logger.info("AuthManager initialized successfully")
    
    def _init_database(self):
        """Create tables if they don't exist"""
        try:
            with psycopg2.connect(self.database_url, sslmode='require') as conn:
                with conn.cursor() as cur:
                    # Users table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id UUID PRIMARY KEY,
                            email VARCHAR(255) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            first_name VARCHAR(100) NOT NULL,
                            last_name VARCHAR(100) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_login TIMESTAMP,
                            is_active BOOLEAN DEFAULT TRUE,
                            subscription_tier VARCHAR(20) DEFAULT 'free',
                            failed_login_attempts INTEGER DEFAULT 0,
                            locked_until TIMESTAMP,
                            email_verified BOOLEAN DEFAULT FALSE
                        )
                    """)
                    
                    # Sessions table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS user_sessions (
                            id UUID PRIMARY KEY,
                            user_id UUID REFERENCES users(id),
                            session_token VARCHAR(255) UNIQUE NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            expires_at TIMESTAMP NOT NULL,
                            ip_address INET,
                            user_agent TEXT,
                            is_active BOOLEAN DEFAULT TRUE
                        )
                    """)
                    
                    # Login attempts table for security
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS login_attempts (
                            id UUID PRIMARY KEY,
                            email VARCHAR(255) NOT NULL,
                            ip_address INET,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            success BOOLEAN NOT NULL,
                            user_agent TEXT,
                            failure_reason VARCHAR(255)
                        )
                    """)
                    
                    conn.commit()
                    logger.info("Database tables created/verified successfully")
                    
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def _validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validate password meets security requirements"""
        if len(password) < self.min_password_length:
            return False, f"Password must be at least {self.min_password_length} characters"
        
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if self.require_lowercase and not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if self.require_digit and not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, "Password meets requirements"
    
    def _validate_email(self, email: str) -> Tuple[bool, str]:
        """Validate email format"""
        try:
            validated_email = validate_email(email)
            return True, validated_email.email
        except EmailNotValidError as e:
            return False, str(e)
    
    def register_user(self, email: str, password: str, first_name: str, last_name: str) -> Tuple[bool, str, Optional[str]]:
        """Register a new user"""
        try:
            # Validate email
            email_valid, email_result = self._validate_email(email)
            if not email_valid:
                return False, email_result, None
            email = email_result
            
            # Validate password strength
            password_valid, password_message = self._validate_password_strength(password)
            if not password_valid:
                return False, password_message, None
            
            # Check if user already exists
            with psycopg2.connect(self.database_url, sslmode='require') as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                    if cur.fetchone():
                        return False, "Email already registered", None
                    
                    # Create new user
                    user_id = str(uuid.uuid4())
                    password_hash = self._hash_password(password)
                    
                    cur.execute("""
                        INSERT INTO users (id, email, password_hash, first_name, last_name)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (user_id, email, password_hash, first_name, last_name))
                    
                    conn.commit()
                    logger.info(f"User registered successfully: {email}")
                    return True, "User registered successfully", user_id
                    
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return False, "Registration failed", None

# Create global auth manager instance
auth_manager = AuthManager()