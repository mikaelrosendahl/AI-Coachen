"""
Data Manager - Hantering av persistent data för AI-coachen
Använder PostgreSQL-databas ai-coachen-db
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
from dotenv import load_dotenv

# PostgreSQL support
import psycopg2
from psycopg2.extras import RealDictCursor

class DataManager:
    """Hanterar datalagring och hämtning för AI-coachen via PostgreSQL"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Ladda miljövariabler
        load_dotenv()
        
        # Hämta databas-URL
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL miljövariabel saknas! Kontrollera .env filen.")
            
        self.logger.info("Using PostgreSQL database: ai-coachen-db")
        
        # Initialisera databas
        self._init_database()
    
    def _get_connection(self):
        """Få PostgreSQL-anslutning"""
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
    
    def _init_database(self):
        """Initialisera PostgreSQL-schema"""
        try:
            self._init_postgres_schema()
        except Exception as e:
            self.logger.error(f"Database initialization failed: {str(e)}")
            raise
    
    def _init_postgres_schema(self):
        """Initialisera PostgreSQL schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Blog posts tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blog_posts (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    slug VARCHAR(255) UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    excerpt TEXT,
                    author VARCHAR(100) DEFAULT 'AI-Coach',
                    category VARCHAR(50) DEFAULT 'coaching',
                    tags TEXT[],
                    published BOOLEAN DEFAULT FALSE,
                    featured BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Blog comments tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blog_comments (
                    id SERIAL PRIMARY KEY,
                    post_id INTEGER REFERENCES blog_posts(id) ON DELETE CASCADE,
                    author_name VARCHAR(100) NOT NULL,
                    author_email VARCHAR(255),
                    content TEXT NOT NULL,
                    approved BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Coaching sessions tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS coaching_sessions (
                    id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    mode VARCHAR(50) NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    message_count INTEGER DEFAULT 0,
                    context TEXT,
                    goals TEXT,
                    progress_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Messages tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL REFERENCES coaching_sessions(id),
                    role VARCHAR(20) NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tokens_used INTEGER DEFAULT 0,
                    cost_usd DECIMAL(10,6) DEFAULT 0.0
                )
            """)
            
            conn.commit()
    
    def _init_sqlite_schema(self):
        """Initialisera SQLite schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Blog posts tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blog_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    slug TEXT UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    excerpt TEXT,
                    author TEXT DEFAULT 'AI-Coach',
                    category TEXT DEFAULT 'coaching',
                    tags TEXT,
                    published BOOLEAN DEFAULT 0,
                    featured BOOLEAN DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Blog comments tabell
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blog_comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    author_name TEXT NOT NULL,
                    author_email TEXT,
                    content TEXT NOT NULL,
                    approved BOOLEAN DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES blog_posts (id)
                )
            """)
            
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
    
    # =========================
    # BLOG FUNCTIONALITY
    # =========================
    
    def create_blog_post(self, title: str, content: str, category: str = "coaching", 
                        tags: List[str] = None, published: bool = False, 
                        featured: bool = False, excerpt: str = None) -> Optional[int]:
        """Skapa nytt blogginlägg"""
        try:
            # Generera slug från title
            import re
            slug = re.sub(r'[^\w\s-]', '', title.lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            
            # Generera excerpt om inte angiven
            if not excerpt and len(content) > 200:
                excerpt = content[:200] + "..."
            
            if self.use_postgres:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO blog_posts (title, slug, content, excerpt, category, tags, published, featured)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (title, slug, content, excerpt, category, tags or [], published, featured))
                    
                    post_id = cursor.fetchone()['id']
                    conn.commit()
                    return post_id
            else:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO blog_posts (title, slug, content, excerpt, category, tags, published, featured)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (title, slug, content, excerpt, category, json.dumps(tags or []), published, featured))
                    
                    post_id = cursor.lastrowid
                    conn.commit()
                    return post_id
                    
        except Exception as e:
            self.logger.error(f"Error creating blog post: {str(e)}")
            return None
    
    def get_blog_posts(self, published_only: bool = True, limit: int = None, 
                      category: str = None) -> List[Dict]:
        """Hämta blogginlägg"""
        try:
            where_conditions = []
            params = []
            
            if published_only:
                where_conditions.append("published = %s" if self.use_postgres else "published = ?")
                params.append(True)
            
            if category:
                where_conditions.append("category = %s" if self.use_postgres else "category = ?")
                params.append(category)
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            order_clause = "ORDER BY created_at DESC"
            limit_clause = ""
            if limit:
                limit_clause = f"LIMIT {limit}"
            
            query = f"""
                SELECT id, title, slug, content, excerpt, author, category, tags, 
                       published, featured, created_at, updated_at
                FROM blog_posts 
                {where_clause} 
                {order_clause} 
                {limit_clause}
            """
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                if self.use_postgres:
                    posts = [dict(row) for row in cursor.fetchall()]
                else:
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    posts = [dict(zip(columns, row)) for row in rows]
                
                # Parse tags for SQLite
                if not self.use_postgres:
                    for post in posts:
                        if post.get('tags'):
                            try:
                                post['tags'] = json.loads(post['tags'])
                            except:
                                post['tags'] = []
                        else:
                            post['tags'] = []
                
                return posts
                
        except Exception as e:
            self.logger.error(f"Error getting blog posts: {str(e)}")
            return []
    
    def get_blog_post_by_slug(self, slug: str) -> Optional[Dict]:
        """Hämta blogginlägg via slug"""
        try:
            query = """
                SELECT id, title, slug, content, excerpt, author, category, tags, 
                       published, featured, created_at, updated_at
                FROM blog_posts 
                WHERE slug = %s
            """ if self.use_postgres else """
                SELECT id, title, slug, content, excerpt, author, category, tags, 
                       published, featured, created_at, updated_at
                FROM blog_posts 
                WHERE slug = ?
            """
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (slug,))
                
                if self.use_postgres:
                    row = cursor.fetchone()
                    if row:
                        return dict(row)
                else:
                    row = cursor.fetchone()
                    if row:
                        columns = [desc[0] for desc in cursor.description]
                        post = dict(zip(columns, row))
                        
                        # Parse tags for SQLite
                        if post.get('tags'):
                            try:
                                post['tags'] = json.loads(post['tags'])
                            except:
                                post['tags'] = []
                        else:
                            post['tags'] = []
                        
                        return post
                
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting blog post by slug: {str(e)}")
            return None
    
    def update_blog_post(self, post_id: int, **kwargs) -> bool:
        """Uppdatera blogginlägg"""
        try:
            # Tillåtna fält att uppdatera
            allowed_fields = ['title', 'content', 'excerpt', 'category', 'tags', 'published', 'featured']
            
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    if field == 'tags' and not self.use_postgres:
                        value = json.dumps(value) if isinstance(value, list) else value
                    
                    update_fields.append(f"{field} = %s" if self.use_postgres else f"{field} = ?")
                    values.append(value)
            
            if not update_fields:
                return False
            
            # Lägg till updated_at
            update_fields.append("updated_at = %s" if self.use_postgres else "updated_at = CURRENT_TIMESTAMP")
            if self.use_postgres:
                values.append(datetime.now())
            
            values.append(post_id)
            
            query = f"""
                UPDATE blog_posts 
                SET {', '.join(update_fields)}
                WHERE id = %s
            """ if self.use_postgres else f"""
                UPDATE blog_posts 
                SET {', '.join(update_fields)}
                WHERE id = ?
            """
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error updating blog post: {str(e)}")
            return False
    
    def delete_blog_post(self, post_id: int) -> bool:
        """Ta bort blogginlägg"""
        try:
            query = "DELETE FROM blog_posts WHERE id = %s" if self.use_postgres else "DELETE FROM blog_posts WHERE id = ?"
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (post_id,))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Error deleting blog post: {str(e)}")
            return False
    
    def get_blog_categories(self) -> List[str]:
        """Hämta alla blog-kategorier"""
        try:
            query = "SELECT DISTINCT category FROM blog_posts WHERE published = %s" if self.use_postgres else "SELECT DISTINCT category FROM blog_posts WHERE published = ?"
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (True,))
                
                if self.use_postgres:
                    return [row['category'] for row in cursor.fetchall()]
                else:
                    return [row[0] for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error getting blog categories: {str(e)}")
            return []
    
    def search_blog_posts(self, search_term: str, published_only: bool = True) -> List[Dict]:
        """Sök i blogginlägg"""
        try:
            where_conditions = []
            params = []
            
            # Sök i title och content
            if self.use_postgres:
                where_conditions.append("(title ILIKE %s OR content ILIKE %s)")
                params.extend([f"%{search_term}%", f"%{search_term}%"])
            else:
                where_conditions.append("(title LIKE ? OR content LIKE ?)")
                params.extend([f"%{search_term}%", f"%{search_term}%"])
            
            if published_only:
                where_conditions.append("published = %s" if self.use_postgres else "published = ?")
                params.append(True)
            
            where_clause = "WHERE " + " AND ".join(where_conditions)
            
            query = f"""
                SELECT id, title, slug, excerpt, author, category, tags, created_at
                FROM blog_posts 
                {where_clause}
                ORDER BY created_at DESC
            """
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                if self.use_postgres:
                    posts = [dict(row) for row in cursor.fetchall()]
                else:
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    posts = [dict(zip(columns, row)) for row in rows]
                    
                    # Parse tags for SQLite
                    for post in posts:
                        if post.get('tags'):
                            try:
                                post['tags'] = json.loads(post['tags'])
                            except:
                                post['tags'] = []
                        else:
                            post['tags'] = []
                
                return posts
                
        except Exception as e:
            self.logger.error(f"Error searching blog posts: {str(e)}")
            return []