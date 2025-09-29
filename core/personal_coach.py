"""
Personal Coach Module - Fokuserad på personlig utveckling och målsättning
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class PersonalGoalType(Enum):
    CAREER = "career"
    HEALTH = "health"
    RELATIONSHIPS = "relationships"
    LEARNING = "learning"
    PERSONAL = "personal"
    FINANCIAL = "financial"

class GoalStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

@dataclass
class PersonalGoal:
    id: str
    title: str
    description: str
    goal_type: PersonalGoalType
    status: GoalStatus
    created_date: datetime
    target_date: Optional[datetime]
    completion_criteria: str
    progress_percentage: int
    milestones: List[str]
    notes: str

@dataclass
class ReflectionEntry:
    date: datetime
    prompt: str
    response: str
    mood_rating: int  # 1-10
    energy_rating: int  # 1-10
    insights: str

class PersonalCoach:
    """Personlig coach för utveckling och målsättning"""
    
    def __init__(self):
        self.goals: Dict[str, PersonalGoal] = {}
        self.reflections: List[ReflectionEntry] = []
        self.coaching_history: List[Dict] = []
        
    def create_goal(self, title: str, description: str, goal_type: PersonalGoalType,
                   target_date: Optional[datetime] = None, 
                   completion_criteria: str = "") -> str:
        """Skapa ett nytt personligt mål"""
        goal_id = f"goal_{len(self.goals) + 1}_{datetime.now().strftime('%Y%m%d')}"
        
        goal = PersonalGoal(
            id=goal_id,
            title=title,
            description=description,
            goal_type=goal_type,
            status=GoalStatus.NOT_STARTED,
            created_date=datetime.now(),
            target_date=target_date,
            completion_criteria=completion_criteria,
            progress_percentage=0,
            milestones=[],
            notes=""
        )
        
        self.goals[goal_id] = goal
        return goal_id
    
    def update_goal_progress(self, goal_id: str, progress: int, 
                           notes: str = "") -> bool:
        """Uppdatera framsteg för ett mål"""
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        goal.progress_percentage = min(100, max(0, progress))
        
        if notes:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            goal.notes += f"\n[{timestamp}] {notes}"
        
        # Uppdatera status baserat på framsteg
        if progress >= 100:
            goal.status = GoalStatus.COMPLETED
        elif progress > 0:
            goal.status = GoalStatus.IN_PROGRESS
        
        return True
    
    def add_milestone(self, goal_id: str, milestone: str) -> bool:
        """Lägg till milstolpe för mål"""
        if goal_id not in self.goals:
            return False
        
        self.goals[goal_id].milestones.append(f"{datetime.now().date()}: {milestone}")
        return True
    
    def get_active_goals(self) -> List[PersonalGoal]:
        """Få alla aktiva mål"""
        return [goal for goal in self.goals.values() 
                if goal.status in [GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS]]
    
    def get_overdue_goals(self) -> List[PersonalGoal]:
        """Få försenade mål"""
        today = datetime.now()
        return [goal for goal in self.goals.values() 
                if goal.target_date and goal.target_date < today 
                and goal.status != GoalStatus.COMPLETED]
    
    def add_reflection(self, prompt: str, response: str, 
                      mood_rating: int, energy_rating: int, 
                      insights: str = "") -> str:
        """Lägg till reflektion"""
        reflection = ReflectionEntry(
            date=datetime.now(),
            prompt=prompt,
            response=response,
            mood_rating=mood_rating,
            energy_rating=energy_rating,
            insights=insights
        )
        
        self.reflections.append(reflection)
        return f"reflection_{len(self.reflections)}"
    
    def get_recent_reflections(self, days: int = 7) -> List[ReflectionEntry]:
        """Få senaste reflektioner"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [r for r in self.reflections if r.date >= cutoff_date]
    
    def generate_coaching_prompts(self) -> List[str]:
        """Generera coaching-prompts baserat på användarens situation"""
        prompts = []
        
        # Baserade på aktiva mål
        active_goals = self.get_active_goals()
        if active_goals:
            goal = active_goals[0]  # Fokusera på första aktiva målet
            prompts.extend([
                f"Hur går det med ditt mål '{goal.title}'? Vad har du gjort denna vecka för att komma närmare?",
                f"Vilka hinder har du stött på med '{goal.title}' och hur kan vi tackle dem?",
                f"Vad motiverar dig mest med att uppnå '{goal.title}'?"
            ])
        
        # Baserade på försenade mål
        overdue_goals = self.get_overdue_goals()
        if overdue_goals:
            prompts.extend([
                f"Jag ser att '{overdue_goals[0].title}' är försenat. Vill du justera målet eller behöver vi hitta nya strategier?",
                "Vad har gjort det svårt att hålla deadlines? Låt oss diskutera hur vi kan förbättra planeringen."
            ])
        
        # Allmänna utvecklingsprompts
        general_prompts = [
            "Vad är du mest stolt över som du har åstadkommit denna vecka?",
            "Vilken utmaning ser du fram emot att tackle nästa?",
            "På en skala 1-10, hur nöjd känner du dig med din progress just nu?",
            "Vad skulle göra nästa vecka till en riktigt bra vecka för dig?",
            "Vilken färdighet eller kunskap skulle du vilja utveckla mest?",
            "Hur mår du med balansen mellan arbete och vila just nu?",
            "Vad ger dig mest energi i ditt dagliga liv?",
            "Om du kunde ge dig själv för 6 månader sedan ett råd, vad skulle det vara?"
        ]
        
        prompts.extend(general_prompts[:3])  # Lägg till 3 allmänna
        
        return prompts
    
    def get_progress_summary(self) -> Dict:
        """Få sammanfattning av framsteg"""
        all_goals = list(self.goals.values())
        
        if not all_goals:
            return {"message": "Inga mål satta än"}
        
        completed = len([g for g in all_goals if g.status == GoalStatus.COMPLETED])
        in_progress = len([g for g in all_goals if g.status == GoalStatus.IN_PROGRESS])
        not_started = len([g for g in all_goals if g.status == GoalStatus.NOT_STARTED])
        
        avg_progress = sum(g.progress_percentage for g in all_goals) / len(all_goals)
        
        recent_reflections = self.get_recent_reflections(7)
        avg_mood = sum(r.mood_rating for r in recent_reflections) / len(recent_reflections) if recent_reflections else 0
        avg_energy = sum(r.energy_rating for r in recent_reflections) / len(recent_reflections) if recent_reflections else 0
        
        return {
            "total_goals": len(all_goals),
            "completed_goals": completed,
            "in_progress_goals": in_progress,
            "not_started_goals": not_started,
            "completion_rate": f"{(completed / len(all_goals)) * 100:.1f}%",
            "average_progress": f"{avg_progress:.1f}%",
            "recent_mood_avg": f"{avg_mood:.1f}/10",
            "recent_energy_avg": f"{avg_energy:.1f}/10",
            "overdue_goals": len(self.get_overdue_goals())
        }
    
    def generate_weekly_review_questions(self) -> List[str]:
        """Generera frågor för veckoreflektion"""
        return [
            "Vad är du mest tacksam för denna vecka?",
            "Vilken utmaning lyckades du hantera bra?",
            "Vad lärde du dig om dig själv?",
            "Vilken progress är du mest nöjd med?",
            "Vad skulle du göra annorlunda om du kunde göra om veckan?",
            "Hur känner du dig inför nästa vecka?",
            "Vilken positiv vana vill du fortsätta bygga på?",
            "Vad behöver du mest stöd med framöver?"
        ]
    
    def get_personalized_advice(self) -> List[str]:
        """Få personliga råd baserat på data"""
        advice = []
        
        # Baserat på mål-mönster
        goal_types = [goal.goal_type for goal in self.goals.values()]
        if goal_types.count(PersonalGoalType.CAREER) > 2:
            advice.append("Jag ser att du fokuserar mycket på karriär. Kom ihåg att balansera med personligt välmående.")
        
        # Baserat på reflektion-mönster
        recent_reflections = self.get_recent_reflections(14)
        if recent_reflections:
            avg_mood = sum(r.mood_rating for r in recent_reflections) / len(recent_reflections)
            if avg_mood < 6:
                advice.append("Ditt humör verkar ha varit lite lågt senaste tiden. Vill du prata om vad som påverkar dig?")
            elif avg_mood > 8:
                advice.append("Du verkar vara på topp! Vad fungerar extra bra för dig just nu?")
        
        # Baserat på mål-framsteg
        overdue = self.get_overdue_goals()
        if len(overdue) > 2:
            advice.append("Du har flera försenade mål. Kanske dags att omprioritera eller justera dina deadlines?")
        
        # Allmänna råd om inga specifika mönster
        if not advice:
            advice.extend([
                "Kom ihåg att fira små framsteg - de leder till stora förändringar!",
                "Är du nöjd med balansen mellan att utmana dig själv och att vila?",
                "Vad roligt planerar du att göra för dig själv denna vecka?"
            ])
        
        return advice[:3]  # Returnera max 3 råd
    
    def export_data(self) -> Dict:
        """Exportera all personalcoaching-data"""
        return {
            "goals": {goal_id: {
                "title": goal.title,
                "description": goal.description,
                "goal_type": goal.goal_type.value,
                "status": goal.status.value,
                "created_date": goal.created_date.isoformat(),
                "target_date": goal.target_date.isoformat() if goal.target_date else None,
                "progress_percentage": goal.progress_percentage,
                "milestones": goal.milestones,
                "notes": goal.notes
            } for goal_id, goal in self.goals.items()},
            "reflections": [{
                "date": r.date.isoformat(),
                "prompt": r.prompt,
                "response": r.response,
                "mood_rating": r.mood_rating,
                "energy_rating": r.energy_rating,
                "insights": r.insights
            } for r in self.reflections]
        }