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
from utils.logging_utils import setup_logging

# Setup logger
logger = setup_logging()

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
    is_admin: bool = False
    role: str = "user"

class AuthManager:
    """Manages all authentication and session management"""
    
    def __init__(self, database_url: str = None):
        """Initialize AuthManager with database connection"""
        self.database_url = database_url or os.getenv('DATABASE_URL')
        
        # Use SQLite for local development if no DATABASE_URL is set
        if not self.database_url:
            # Development mode - use SQLite
            os.makedirs('data', exist_ok=True)
            self.database_url = "sqlite:///data/local_auth.db"
            self.use_sqlite = True
            logger.info("Using local SQLite database for development")
        else:
            self.use_sqlite = self.database_url.startswith('sqlite')
            
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
        if self.use_sqlite:
            self._init_sqlite_database()
        else:
            self._init_postgres_database()
    
    def _init_sqlite_database(self):
        """Initialize SQLite database"""
        import sqlite3
        try:
            conn = sqlite3.connect(self.database_url.replace('sqlite:///', ''))
            cursor = conn.cursor()
            
            # Users table for SQLite
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    subscription_tier TEXT DEFAULT 'free',
                    failed_login_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP,
                    email_verified BOOLEAN DEFAULT FALSE,
                    is_admin BOOLEAN DEFAULT FALSE,
                    role TEXT DEFAULT 'user'
                )
            """)
            
            # Sessions table for SQLite
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Login attempts table for SQLite
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    ip_address TEXT,
                    success BOOLEAN NOT NULL,
                    failure_reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("SQLite database tables created/verified successfully")
            
        except Exception as e:
            logger.error(f"SQLite database initialization failed: {e}")
            raise
    
    def _init_postgres_database(self):
        """Initialize PostgreSQL database"""
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
                            email_verified BOOLEAN DEFAULT FALSE,
                            is_admin BOOLEAN DEFAULT FALSE,
                            role VARCHAR(20) DEFAULT 'user'
                        )
                    """)
                    
                    # Add admin columns to existing users table if they don't exist
                    cur.execute("""
                        ALTER TABLE users 
                        ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE,
                        ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'user'
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
                    logger.info("PostgreSQL database tables created/verified successfully")
                    
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
            validated_email = validate_email(email, check_deliverability=False)
            return True, validated_email.email
        except EmailNotValidError as e:
            return False, str(e)
    
    def register_user(self, email: str, password: str, first_name: str, last_name: str, is_admin: bool = False, role: str = "user") -> Tuple[bool, str, Optional[str]]:
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
            
            # Check if user already exists and create new user
            if self.use_sqlite:
                import sqlite3
                conn = sqlite3.connect(self.database_url.replace('sqlite:///', ''))
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
                if cursor.fetchone():
                    conn.close()
                    return False, "Email already registered", None
                
                # Create new user
                user_id = str(uuid.uuid4())
                password_hash = self._hash_password(password)
                
                cursor.execute("""
                    INSERT INTO users (id, email, password_hash, first_name, last_name, is_admin, role)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, email, password_hash, first_name, last_name, 1 if is_admin else 0, role))
                
                conn.commit()
                conn.close()
                logger.info(f"User registered successfully: {email}")
                return True, "User registered successfully", user_id
            else:
                with psycopg2.connect(self.database_url, sslmode='require') as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                        if cur.fetchone():
                            return False, "Email already registered", None
                        
                        # Create new user
                        user_id = str(uuid.uuid4())
                        password_hash = self._hash_password(password)
                        
                        cur.execute("""
                            INSERT INTO users (id, email, password_hash, first_name, last_name, is_admin, role)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (user_id, email, password_hash, first_name, last_name, is_admin, role))
                        
                        conn.commit()
                        logger.info(f"User registered successfully: {email}")
                        return True, "User registered successfully", user_id
                    
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return False, "Registration failed", None
    
    def login_user(self, email: str, password: str, ip_address: str = None) -> Tuple[bool, str, Optional[str]]:
        """Login user and create session"""
        try:
            if self.use_sqlite:
                import sqlite3
                conn = sqlite3.connect(self.database_url.replace('sqlite:///', ''))
                conn.row_factory = sqlite3.Row  # Enable dictionary-like access
                cursor = conn.cursor()
                
                # Get user
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                user_data = cursor.fetchone()
                
                if not user_data:
                    self._log_login_attempt(email, False, "User not found", ip_address)
                    conn.close()
                    return False, "Invalid credentials", None
                
                # Convert to dict for compatibility
                user_dict = dict(user_data)
                
                # Check if account is locked (SQLite stores datetime as string)
                if user_dict['locked_until']:
                    locked_until = datetime.fromisoformat(user_dict['locked_until'])
                    if locked_until > datetime.now():
                        conn.close()
                        return False, "Account temporarily locked", None
                
                # Verify password
                if not self._verify_password(password, user_dict['password_hash']):
                    # Increment failed attempts
                    failed_attempts = user_dict['failed_login_attempts'] + 1
                    locked_until = None
                    
                    if failed_attempts >= self.max_login_attempts:
                        locked_until = datetime.now().isoformat()
                        
                    cursor.execute("""
                        UPDATE users 
                        SET failed_login_attempts = ?, locked_until = ?
                        WHERE email = ?
                    """, (failed_attempts, locked_until, email))
                    
                    self._log_login_attempt(email, False, "Invalid password", ip_address)
                    conn.commit()
                    conn.close()
                    return False, "Invalid credentials", None
                
                # Reset failed attempts and create session
                session_token = str(uuid.uuid4())
                now_iso = datetime.now().isoformat()
                expires_at_iso = (datetime.now() + self.session_timeout).isoformat()
                
                cursor.execute("""
                    UPDATE users 
                    SET failed_login_attempts = 0, locked_until = NULL, last_login = ?
                    WHERE email = ?
                """, (now_iso, email))
                
                cursor.execute("""
                    INSERT INTO user_sessions (id, user_id, session_token, expires_at, ip_address)
                    VALUES (?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), user_dict['id'], session_token, expires_at_iso, ip_address))
                
                self._log_login_attempt(email, True, "Success", ip_address)
                conn.commit()
                conn.close()
                
                logger.info(f"User logged in successfully: {email}")
                return True, "Login successful", session_token
                
            else:
                with psycopg2.connect(self.database_url, sslmode='require') as conn:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        # Get user
                        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                        user_data = cur.fetchone()
                        
                        if not user_data:
                            self._log_login_attempt(email, False, "User not found", ip_address)
                            return False, "Invalid credentials", None
                        
                        # Check if account is locked
                        if user_data['locked_until'] and user_data['locked_until'] > datetime.now():
                            return False, "Account temporarily locked", None
                        
                        # Verify password
                        if not self._verify_password(password, user_data['password_hash']):
                            # Increment failed attempts
                            failed_attempts = user_data['failed_login_attempts'] + 1
                            locked_until = None
                            
                            if failed_attempts >= self.max_login_attempts:
                                locked_until = datetime.now() + self.lockout_duration
                                
                            cur.execute("""
                                UPDATE users 
                                SET failed_login_attempts = %s, locked_until = %s
                                WHERE email = %s
                            """, (failed_attempts, locked_until, email))
                            
                            self._log_login_attempt(email, False, "Invalid password", ip_address)
                            conn.commit()
                            return False, "Invalid credentials", None
                        
                        # Reset failed attempts and create session
                        session_token = str(uuid.uuid4())
                        expires_at = datetime.now() + self.session_timeout
                        
                        cur.execute("""
                            UPDATE users 
                            SET failed_login_attempts = 0, locked_until = NULL, last_login = %s
                            WHERE email = %s
                        """, (datetime.now(), email))
                        
                        cur.execute("""
                            INSERT INTO user_sessions (id, user_id, session_token, expires_at, ip_address)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (str(uuid.uuid4()), user_data['id'], session_token, expires_at, ip_address))
                        
                        self._log_login_attempt(email, True, "Success", ip_address)
                        conn.commit()
                        
                        logger.info(f"User logged in successfully: {email}")
                        return True, "Login successful", session_token
                    
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False, "Login failed", None
    
    def get_user_from_session(self, session_token: str) -> Optional[User]:
        """Get user from session token"""
        try:
            if self.use_sqlite:
                import sqlite3
                conn = sqlite3.connect(self.database_url.replace('sqlite:///', ''))
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT u.* FROM users u
                    JOIN user_sessions s ON u.id = s.user_id
                    WHERE s.session_token = ? 
                    AND s.expires_at > ?
                """, (session_token, datetime.now().isoformat()))
                
                user_data = cursor.fetchone()
                conn.close()
                
                if user_data:
                    user_dict = dict(user_data)
                    return User(
                        id=user_dict['id'],
                        email=user_dict['email'],
                        first_name=user_dict['first_name'],
                        last_name=user_dict['last_name'],
                        created_at=datetime.fromisoformat(user_dict['created_at']) if user_dict['created_at'] else datetime.now(),
                        last_login=datetime.fromisoformat(user_dict['last_login']) if user_dict['last_login'] else None,
                        is_active=bool(user_dict['is_active']),
                        subscription_tier=user_dict.get('subscription_tier', 'free'),
                        failed_login_attempts=user_dict['failed_login_attempts'],
                        locked_until=datetime.fromisoformat(user_dict['locked_until']) if user_dict['locked_until'] else None,
                        email_verified=bool(user_dict.get('email_verified', 0)),
                        is_admin=bool(user_dict['is_admin']),
                        role=user_dict['role']
                    )
            else:
                with psycopg2.connect(self.database_url, sslmode='require') as conn:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("""
                            SELECT u.* FROM users u
                            JOIN user_sessions s ON u.id = s.user_id
                            WHERE s.session_token = %s 
                            AND s.expires_at > %s 
                            AND s.is_active = TRUE
                        """, (session_token, datetime.now()))
                        
                        user_data = cur.fetchone()
                        if user_data:
                            return User(
                                id=user_data['id'],
                                email=user_data['email'],
                                first_name=user_data['first_name'],
                                last_name=user_data['last_name'],
                                created_at=user_data['created_at'],
                                last_login=user_data['last_login'],
                                is_active=user_data['is_active'],
                                subscription_tier=user_data['subscription_tier'],
                                failed_login_attempts=user_data['failed_login_attempts'],
                                locked_until=user_data['locked_until'],
                                email_verified=user_data['email_verified'],
                                is_admin=user_data.get('is_admin', False),
                                role=user_data.get('role', 'user')
                            )
            return None
                    
        except Exception as e:
            logger.error(f"Session validation failed: {e}")
            return None
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user by invalidating session"""
        try:
            if self.use_sqlite:
                import sqlite3
                conn = sqlite3.connect(self.database_url.replace('sqlite:///', ''))
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM user_sessions 
                    WHERE session_token = ?
                """, (session_token,))
                conn.commit()
                conn.close()
                logger.info("User logged out successfully")
                return True
            else:
                with psycopg2.connect(self.database_url, sslmode='require') as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE user_sessions 
                            SET is_active = FALSE 
                            WHERE session_token = %s
                        """, (session_token,))
                        
                        conn.commit()
                        logger.info("User logged out successfully")
                        return True
                    
        except Exception as e:
            logger.error(f"Logout failed: {e}")
            return False
    
    def promote_to_admin(self, email: str, role: str = "admin") -> Tuple[bool, str]:
        """Promote user to admin (only callable by existing admin)"""
        try:
            if self.use_sqlite:
                import sqlite3
                conn = sqlite3.connect(self.database_url.replace('sqlite:///', ''))
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET is_admin = 1, role = ?
                    WHERE email = ?
                """, (role, email))
                
                if cursor.rowcount == 0:
                    conn.close()
                    return False, "User not found"
                
                conn.commit()
                conn.close()
                logger.info(f"User promoted to admin: {email}")
                return True, f"User {email} promoted to {role}"
            else:
                with psycopg2.connect(self.database_url, sslmode='require') as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE users 
                            SET is_admin = TRUE, role = %s
                            WHERE email = %s
                        """, (role, email))
                        
                        if cur.rowcount == 0:
                            return False, "User not found"
                        
                        conn.commit()
                        logger.info(f"User promoted to admin: {email}")
                        return True, f"User {email} promoted to {role}"
                    
        except Exception as e:
            logger.error(f"Admin promotion failed: {e}")
            return False, "Admin promotion failed"
    
    def create_first_admin(self, email: str, password: str, first_name: str, last_name: str) -> Tuple[bool, str, Optional[str]]:
        """Create the first admin user (special method for initial setup)"""
        try:
            if self.use_sqlite:
                import sqlite3
                conn = sqlite3.connect(self.database_url.replace('sqlite:///', ''))
                cursor = conn.cursor()
                # Check if any admin exists
                cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
                admin_count = cursor.fetchone()[0]
                conn.close()
                
                if admin_count > 0:
                    return False, "Admin already exists", None
                
                # Create first admin
                return self.register_user(email, password, first_name, last_name, is_admin=True, role="admin")
            else:
                with psycopg2.connect(self.database_url, sslmode='require') as conn:
                    with conn.cursor() as cur:
                        # Check if any admin exists
                        cur.execute("SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
                        admin_count = cur.fetchone()[0]
                        
                        if admin_count > 0:
                            return False, "Admin already exists", None
                        
                        # Create first admin
                        return self.register_user(email, password, first_name, last_name, is_admin=True, role="admin")
                    
        except Exception as e:
            logger.error(f"First admin creation failed: {e}")
            return False, "First admin creation failed", None
    
    def _log_login_attempt(self, email: str, success: bool, reason: str, ip_address: str = None):
        """Log login attempt for security monitoring"""
        try:
            if self.use_sqlite:
                import sqlite3
                conn = sqlite3.connect(self.database_url.replace('sqlite:///', ''))
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO login_attempts (id, email, ip_address, success, failure_reason)
                    VALUES (?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), email, ip_address, 1 if success else 0, reason if not success else None))
                conn.commit()
                conn.close()
            else:
                with psycopg2.connect(self.database_url, sslmode='require') as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO login_attempts (id, email, ip_address, success, failure_reason)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (str(uuid.uuid4()), email, ip_address, success, reason if not success else None))
                        conn.commit()
                    
        except Exception as e:
            logger.error(f"Failed to log login attempt: {e}")

# Note: Global auth manager instance will be created in main.py when DATABASE_URL is available