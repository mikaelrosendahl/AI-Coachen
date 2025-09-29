"""
Data Manager - Hantering av persistent data för AI-coachen
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

class DataManager:
    """Hanterar datalagring och hämtning för AI-coachen"""
    
    def __init__(self, db_path: str = "data/coach_data.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
        # Skapa data-mapp om den inte finns
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialisera databas
        self._init_database()
    
    def _init_database(self):
        """Initialisera databas-schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Coaching sessions tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS coaching_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    message_count INTEGER DEFAULT 0,
                    context TEXT,
                    goals TEXT,
                    progress_notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Messages tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES coaching_sessions (id)
                )
            """)
            
            # Personal goals tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS personal_goals (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    goal_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    target_date TEXT,
                    completion_criteria TEXT,
                    progress_percentage INTEGER DEFAULT 0,
                    milestones TEXT,
                    notes TEXT
                )
            """)
            
            # Reflections tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reflections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    mood_rating INTEGER,
                    energy_rating INTEGER,
                    insights TEXT
                )
            """)
            
            # University projects tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS university_projects (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    use_case TEXT NOT NULL,
                    phase TEXT NOT NULL,
                    stakeholders TEXT,
                    start_date TEXT NOT NULL,
                    target_completion TEXT,
                    budget REAL,
                    success_criteria TEXT,
                    risks TEXT,
                    progress_notes TEXT,
                    kpis TEXT
                )
            """)
            
            # Implementation challenges tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS implementation_challenges (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    severity INTEGER NOT NULL,
                    stakeholders_affected TEXT,
                    proposed_solutions TEXT,
                    status TEXT NOT NULL,
                    created_date TEXT NOT NULL
                )
            """)
            
            # University profiles tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS university_profiles (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    size TEXT,
                    research_focus TEXT,
                    current_ai_maturity INTEGER,
                    budget_range TEXT,
                    key_challenges TEXT,
                    success_metrics TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def save_session(self, session_data: Dict) -> bool:
        """Spara coaching session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO coaching_sessions 
                    (id, user_id, mode, start_time, end_time, message_count, context, goals, progress_notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_data['session_id'],
                    session_data['user_id'],
                    session_data['mode'],
                    session_data['start_time'],
                    session_data.get('end_time'),
                    session_data.get('message_count', 0),
                    json.dumps(session_data.get('context', {})),
                    json.dumps(session_data.get('goals', [])),
                    session_data.get('progress_notes', '')
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving session: {str(e)}")
            return False
    
    def save_message(self, session_id: str, role: str, content: str, 
                    timestamp: str, metadata: Dict = None) -> bool:
        """Spara meddelande"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO messages (session_id, role, content, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    session_id,
                    role,
                    content,
                    timestamp,
                    json.dumps(metadata) if metadata else None
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving message: {str(e)}")
            return False
    
    def save_personal_goal(self, goal_data: Dict) -> bool:
        """Spara personligt mål"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO personal_goals 
                    (id, user_id, title, description, goal_type, status, created_date, 
                     target_date, completion_criteria, progress_percentage, milestones, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    goal_data['id'],
                    goal_data['user_id'],
                    goal_data['title'],
                    goal_data['description'],
                    goal_data['goal_type'],
                    goal_data['status'],
                    goal_data['created_date'],
                    goal_data.get('target_date'),
                    goal_data.get('completion_criteria', ''),
                    goal_data.get('progress_percentage', 0),
                    json.dumps(goal_data.get('milestones', [])),
                    goal_data.get('notes', '')
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving personal goal: {str(e)}")
            return False
    
    def save_reflection(self, reflection_data: Dict) -> bool:
        """Spara reflektion"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO reflections 
                    (user_id, date, prompt, response, mood_rating, energy_rating, insights)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    reflection_data['user_id'],
                    reflection_data['date'],
                    reflection_data['prompt'],
                    reflection_data['response'],
                    reflection_data['mood_rating'],
                    reflection_data['energy_rating'],
                    reflection_data.get('insights', '')
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving reflection: {str(e)}")
            return False
    
    def save_university_project(self, project_data: Dict) -> bool:
        """Spara universitets AI-projekt"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO university_projects 
                    (id, user_id, title, description, use_case, phase, stakeholders,
                     start_date, target_completion, budget, success_criteria, risks, 
                     progress_notes, kpis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    project_data['id'],
                    project_data['user_id'],
                    project_data['title'],
                    project_data['description'],
                    project_data['use_case'],
                    project_data['phase'],
                    json.dumps(project_data.get('stakeholders', [])),
                    project_data['start_date'],
                    project_data.get('target_completion'),
                    project_data.get('budget'),
                    json.dumps(project_data.get('success_criteria', [])),
                    json.dumps(project_data.get('risks', [])),
                    project_data.get('progress_notes', ''),
                    json.dumps(project_data.get('kpis', {}))
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving university project: {str(e)}")
            return False
    
    def save_challenge(self, challenge_data: Dict) -> bool:
        """Spara implementationsutmaning"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO implementation_challenges 
                    (id, user_id, title, description, category, severity, 
                     stakeholders_affected, proposed_solutions, status, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    challenge_data['id'],
                    challenge_data['user_id'],
                    challenge_data['title'],
                    challenge_data['description'],
                    challenge_data['category'],
                    challenge_data['severity'],
                    json.dumps(challenge_data.get('stakeholders_affected', [])),
                    json.dumps(challenge_data.get('proposed_solutions', [])),
                    challenge_data['status'],
                    challenge_data['created_date']
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving challenge: {str(e)}")
            return False
    
    def load_user_sessions(self, user_id: str) -> List[Dict]:
        """Ladda användarens coaching sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM coaching_sessions 
                    WHERE user_id = ? 
                    ORDER BY start_time DESC
                """, (user_id,))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                sessions = []
                for row in rows:
                    session_dict = dict(zip(columns, row))
                    # Parse JSON fields
                    session_dict['context'] = json.loads(session_dict['context']) if session_dict['context'] else {}
                    session_dict['goals'] = json.loads(session_dict['goals']) if session_dict['goals'] else []
                    sessions.append(session_dict)
                
                return sessions
                
        except Exception as e:
            self.logger.error(f"Error loading user sessions: {str(e)}")
            return []
    
    def load_session_messages(self, session_id: str) -> List[Dict]:
        """Ladda meddelanden för session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM messages 
                    WHERE session_id = ? 
                    ORDER BY timestamp
                """, (session_id,))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                messages = []
                for row in rows:
                    message_dict = dict(zip(columns, row))
                    message_dict['metadata'] = json.loads(message_dict['metadata']) if message_dict['metadata'] else {}
                    messages.append(message_dict)
                
                return messages
                
        except Exception as e:
            self.logger.error(f"Error loading session messages: {str(e)}")
            return []
    
    def load_user_goals(self, user_id: str) -> List[Dict]:
        """Ladda användarens mål"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM personal_goals 
                    WHERE user_id = ? 
                    ORDER BY created_date DESC
                """, (user_id,))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                goals = []
                for row in rows:
                    goal_dict = dict(zip(columns, row))
                    goal_dict['milestones'] = json.loads(goal_dict['milestones']) if goal_dict['milestones'] else []
                    goals.append(goal_dict)
                
                return goals
                
        except Exception as e:
            self.logger.error(f"Error loading user goals: {str(e)}")
            return []
    
    def load_user_reflections(self, user_id: str, days: int = 30) -> List[Dict]:
        """Ladda användarens reflektioner"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff_date = datetime.now().strftime('%Y-%m-%d')
                
                cursor.execute("""
                    SELECT * FROM reflections 
                    WHERE user_id = ? AND date >= datetime(?, '-{} days')
                    ORDER BY date DESC
                """.format(days), (user_id, cutoff_date))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Error loading user reflections: {str(e)}")
            return []
    
    def export_user_data(self, user_id: str) -> Dict:
        """Exportera all användardata"""
        return {
            "sessions": self.load_user_sessions(user_id),
            "goals": self.load_user_goals(user_id),
            "reflections": self.load_user_reflections(user_id, days=365),
            "export_timestamp": datetime.now().isoformat()
        }
    
    def backup_database(self, backup_path: str) -> bool:
        """Skapa backup av databasen"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            self.logger.info(f"Database backed up to {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error backing up database: {str(e)}")
            return False