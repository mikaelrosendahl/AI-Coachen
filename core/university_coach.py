"""
University AI Coach Module - Fokuserad på AI-implementering inom universitetskontext
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class AIImplementationPhase(Enum):
    ASSESSMENT = "assessment"
    STRATEGY = "strategy" 
    PILOT = "pilot"
    DEPLOYMENT = "deployment"
    SCALING = "scaling"
    OPTIMIZATION = "optimization"

class StakeholderType(Enum):
    FACULTY = "faculty"
    RESEARCHERS = "researchers"
    IT_DEPARTMENT = "it_department"
    ADMINISTRATION = "administration"
    STUDENTS = "students"
    LEADERSHIP = "leadership"

class AIUseCase(Enum):
    RESEARCH_ACCELERATION = "research_acceleration"
    AUTOMATED_GRADING = "automated_grading"
    PERSONALIZED_LEARNING = "personalized_learning"
    ADMINISTRATIVE_AUTOMATION = "administrative_automation"
    DATA_ANALYTICS = "data_analytics"
    CONTENT_GENERATION = "content_generation"
    PREDICTIVE_MODELING = "predictive_modeling"

@dataclass
class UniversityProfile:
    name: str
    size: str  # Small, Medium, Large
    research_focus: List[str]
    current_ai_maturity: int  # 1-10 scale
    budget_range: str
    key_challenges: List[str]
    success_metrics: List[str]

@dataclass
class AIProject:
    id: str
    title: str
    description: str
    use_case: AIUseCase
    phase: AIImplementationPhase
    stakeholders: List[StakeholderType]
    start_date: datetime
    target_completion: Optional[datetime]
    budget: Optional[float]
    success_criteria: List[str]
    risks: List[str]
    progress_notes: str
    kpis: Dict[str, float]

@dataclass
class ImplementationChallenge:
    id: str
    title: str
    description: str
    category: str  # Technical, Organizational, Financial, Ethical
    severity: int  # 1-10
    stakeholders_affected: List[StakeholderType]
    proposed_solutions: List[str]
    status: str  # Open, In Progress, Resolved
    created_date: datetime

class UniversityAICoach:
    """Coach för AI-implementering på universitet"""
    
    def __init__(self):
        self.university_profile: Optional[UniversityProfile] = None
        self.projects: Dict[str, AIProject] = {}
        self.challenges: Dict[str, ImplementationChallenge] = {}
        self.stakeholder_feedback: List[Dict] = []
        
        # Knowledge base för råd och best practices
        self.knowledge_base = self._init_knowledge_base()
    
    def _init_knowledge_base(self) -> Dict:
        """Initialisera kunskapsbas med AI-implementering best practices"""
        return {
            "ethical_guidelines": [
                "Utveckla tydliga AI-etik policies",
                "Säkerställ transparens i AI-beslut",
                "Implementera bias-kontroller",
                "Skydda personlig integritet och data",
                "Skapa accountability frameworks"
            ],
            "change_management": [
                "Starta med champions och early adopters",
                "Investera i omfattande träning",
                "Kommunicera tydligt om fördelar och begränsningar",
                "Implementera gradvist med pilotprojekt",
                "Skapa feedback-loopar med användare"
            ],
            "technical_considerations": [
                "Utvärdera befintlig IT-infrastruktur",
                "Säkerställ datasäkerhet och compliance",
                "Planera för skalbarhet från start",
                "Integrera med befintliga system",
                "Implementera robust monitoring och logging"
            ],
            "success_factors": [
                "Stark ledarskapsstöd och vision",
                "Tvärdisciplinär samarbete",
                "Fokus på användarens behov",
                "Kontinuerlig utvärdering och förbättring",
                "Investeringar i kompetensutveckling"
            ]
        }
    
    def set_university_profile(self, profile: UniversityProfile):
        """Sätt universitetsprofil"""
        self.university_profile = profile
    
    def create_project(self, title: str, description: str, use_case: AIUseCase,
                      stakeholders: List[StakeholderType],
                      target_completion: Optional[datetime] = None) -> str:
        """Skapa nytt AI-projekt"""
        project_id = f"ai_project_{len(self.projects) + 1}_{datetime.now().strftime('%Y%m%d')}"
        
        project = AIProject(
            id=project_id,
            title=title,
            description=description,
            use_case=use_case,
            phase=AIImplementationPhase.ASSESSMENT,
            stakeholders=stakeholders,
            start_date=datetime.now(),
            target_completion=target_completion,
            budget=None,
            success_criteria=[],
            risks=[],
            progress_notes="",
            kpis={}
        )
        
        self.projects[project_id] = project
        return project_id
    
    def advance_project_phase(self, project_id: str, notes: str = "") -> bool:
        """Flytta projekt till nästa fas"""
        if project_id not in self.projects:
            return False
        
        project = self.projects[project_id]
        phases = list(AIImplementationPhase)
        current_index = phases.index(project.phase)
        
        if current_index < len(phases) - 1:
            project.phase = phases[current_index + 1]
            
            if notes:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                project.progress_notes += f"\n[{timestamp}] Moved to {project.phase.value}: {notes}"
            
            return True
        return False
    
    def add_challenge(self, title: str, description: str, category: str,
                     severity: int, stakeholders: List[StakeholderType]) -> str:
        """Lägg till implementationsutmaning"""
        challenge_id = f"challenge_{len(self.challenges) + 1}_{datetime.now().strftime('%Y%m%d')}"
        
        challenge = ImplementationChallenge(
            id=challenge_id,
            title=title,
            description=description,
            category=category,
            severity=severity,
            stakeholders_affected=stakeholders,
            proposed_solutions=[],
            status="Open",
            created_date=datetime.now()
        )
        
        self.challenges[challenge_id] = challenge
        return challenge_id
    
    def propose_solution(self, challenge_id: str, solution: str) -> bool:
        """Föreslå lösning på utmaning"""
        if challenge_id not in self.challenges:
            return False
        
        self.challenges[challenge_id].proposed_solutions.append(solution)
        return True
    
    def get_implementation_roadmap(self) -> List[Dict]:
        """Få implementationsroadmap baserat på universitetsprofil"""
        if not self.university_profile:
            return []
        
        roadmap = []
        
        # Fas 1: Assessment och Strategi
        roadmap.append({
            "phase": "Assessment & Strategy",
            "duration": "2-3 månader",
            "activities": [
                "Kartlägg nuvarande AI-mognad och kapacitet",
                "Identifiera high-value use cases",
                "Analysera stakeholder-behov och motstånd",
                "Utveckla AI-policy och etiska riktlinjer",
                "Skapa business case och budget"
            ],
            "deliverables": [
                "AI Maturity Assessment Report",
                "Strategic AI Implementation Plan",
                "Risk Assessment och Mitigation Plan"
            ]
        })
        
        # Fas 2: Pilot och Proof of Concept
        roadmap.append({
            "phase": "Pilot Projects",
            "duration": "3-6 månader",
            "activities": [
                "Välj 2-3 lågrisk, high-impact pilotprojekt",
                "Bygg tvärfunktionella team",
                "Implementera grundläggande AI-infrastruktur",
                "Träna nyckelpersoner och champions",
                "Utveckla mät- och utvärderingssystem"
            ],
            "deliverables": [
                "Fungerande AI-pilotlösningar",
                "Träningspaket och dokumentation",
                "Utvärderingsrapport med lessons learned"
            ]
        })
        
        # Fas 3: Scaling och Deployment
        roadmap.append({
            "phase": "Scaling & Deployment", 
            "duration": "6-12 månader",
            "activities": [
                "Rulla ut framgångsrika piloter university-wide",
                "Implementera fullskalig träningsprogram",
                "Integrera AI-verktyg med befintliga system",
                "Utveckla supportprocesser och governance",
                "Mät impact och ROI kontinuerligt"
            ],
            "deliverables": [
                "University-wide AI platform",
                "Comprehensive training program", 
                "AI Governance framework",
                "Impact och ROI rapporter"
            ]
        })
        
        return roadmap
    
    def get_stakeholder_strategy(self, stakeholder: StakeholderType) -> Dict:
        """Få strategi för specifik stakeholder-grupp"""
        strategies = {
            StakeholderType.FACULTY: {
                "key_concerns": [
                    "Academic freedom och autonomy",
                    "Påverkan på undervisningskvalitet",
                    "Tid för inlärning av nya verktyg"
                ],
                "engagement_approach": [
                    "Involvera i designprocess från början",
                    "Fokusera på pedagogiska fördelar", 
                    "Erbjud flexibel träning och support",
                    "Skapa faculty AI champions program"
                ],
                "success_metrics": [
                    "Adoption rate för AI-verktyg",
                    "Förbättring i undervisningsutvärderingar",
                    "Tid sparad på administrativa uppgifter"
                ]
            },
            StakeholderType.RESEARCHERS: {
                "key_concerns": [
                    "Forskningsetik och reproducerbarhet",
                    "Dataägarskap och IP-rättigheter",
                    "AI bias i forskningsresultat"
                ],
                "engagement_approach": [
                    "Betona accelererade forskningsresultat",
                    "Säkerställ transparens och explainability",
                    "Skapa AI research support center",
                    "Utveckla best practices för AI i forskning"
                ],
                "success_metrics": [
                    "Ökning i forskningsproduktivitet",
                    "Antal AI-enhanced publikationer",
                    "Forskningsfinansiering med AI-komponenter"
                ]
            },
            StakeholderType.IT_DEPARTMENT: {
                "key_concerns": [
                    "Säkerhet och compliance",
                    "Integration med legacy system",
                    "Skalbarhet och prestanda"
                ],
                "engagement_approach": [
                    "Involvera i teknisk planering från dag ett",
                    "Investera i IT-uppgradering och träning",
                    "Skapa tydliga säkerhets- och compliance-protocols",
                    "Implementera robust monitoring och support"
                ],
                "success_metrics": [
                    "System uptime och prestanda",
                    "Säkerhetsincidenter (ska minska)",
                    "IT support ticket volume"
                ]
            },
            StakeholderType.ADMINISTRATION: {
                "key_concerns": [
                    "Budget och ROI",
                    "Regulatory compliance",
                    "Change management impact"
                ],
                "engagement_approach": [
                    "Fokusera på kostnadsbesparingar och effektivitet",
                    "Visa tydliga KPIs och ROI",
                    "Säkerställ compliance med regelverk",
                    "Skapa smooth change management process"
                ],
                "success_metrics": [
                    "ROI på AI-investeringar",
                    "Minskning i administrativa kostnader",
                    "Förbättrad compliance och audit results"
                ]
            }
        }
        
        return strategies.get(stakeholder, {})
    
    def get_risk_assessment(self) -> List[Dict]:
        """Få riskbedömning för AI-implementering"""
        return [
            {
                "category": "Technical",
                "risks": [
                    "Integration challenges med legacy system",
                    "Data quality och availability issues", 
                    "AI model bias och fairness problem",
                    "Cybersecurity vulnerabilities"
                ],
                "mitigation": [
                    "Genomföra teknisk due diligence tidigt",
                    "Investera i data governance och quality",
                    "Implementera bias testing och monitoring",
                    "Förstärk cybersecurity protocols"
                ]
            },
            {
                "category": "Organizational", 
                "risks": [
                    "Motstånd mot förändring från faculty/staff",
                    "Bristande AI literacy och skills",
                    "Unclear governance och accountability",
                    "Kulturell kollision med akademiska värden"
                ],
                "mitigation": [
                    "Investera kraftigt i change management",
                    "Skapa omfattande träningsprogram",
                    "Etablera tydlig AI governance struktur",
                    "Align AI initiatives med akademisk mission"
                ]
            },
            {
                "category": "Ethical & Legal",
                "risks": [
                    "Student data privacy concerns",
                    "Algorithmic bias påverkar student outcomes",
                    "IP-rättigheter för AI-genererat content",
                    "Compliance med educational regulations"
                ],
                "mitigation": [
                    "Utveckla stringent data privacy policies",
                    "Implementera kontinuerlig bias monitoring",
                    "Skapa tydliga IP policies för AI",
                    "Säkerställ regulatory compliance från start"
                ]
            }
        ]
    
    def generate_university_coaching_prompts(self) -> List[str]:
        """Generera coaching-frågor för universitets-AI implementering"""
        prompts = []
        
        # Baserat på nuvarande projekt
        active_projects = [p for p in self.projects.values() 
                         if p.phase != AIImplementationPhase.OPTIMIZATION]
        
        if active_projects:
            project = active_projects[0]
            prompts.extend([
                f"Hur går implementeringen av '{project.title}'? Vilka framsteg har ni gjort?",
                f"Vilka utmaningar stöter ni på i {project.phase.value}-fasen?",
                f"Hur har stakeholders reagerat på projektet hittills?"
            ])
        
        # Baserat på utmaningar
        open_challenges = [c for c in self.challenges.values() if c.status == "Open"]
        if open_challenges:
            challenge = open_challenges[0]
            prompts.append(f"Låt oss diskutera '{challenge.title}' - vilka lösningsalternativ har ni övervägt?")
        
        # Allmänna strategiska frågor
        strategic_prompts = [
            "Vilken är er vision för AI:s roll på universitetet de kommande 5 åren?",
            "Vilka fakulteter eller avdelningar visar mest intresse för AI-adoption?",
            "Hur planerar ni att mäta framgången av era AI-initiativ?",
            "Vilka etiska riktlinjer har ni etablerat för AI-användning?",
            "Hur arbetar ni med att bygga AI-kompetens bland er personal?",
            "Vilka externa partners eller leverantörer överväger ni?",
            "Hur säkerställer ni att AI-implementeringen stödjer er forskningsstrategi?",
            "Vilken roll spelar studentperspektivet i era AI-planer?"
        ]
        
        prompts.extend(strategic_prompts[:3])
        return prompts
    
    def get_implementation_status(self) -> Dict:
        """Få status för AI-implementering"""
        if not self.projects:
            return {"message": "Inga AI-projekt startade än"}
        
        total_projects = len(self.projects)
        by_phase = {}
        for phase in AIImplementationPhase:
            count = len([p for p in self.projects.values() if p.phase == phase])
            by_phase[phase.value] = count
        
        open_challenges = len([c for c in self.challenges.values() if c.status == "Open"])
        high_severity_challenges = len([c for c in self.challenges.values() 
                                      if c.severity >= 7 and c.status == "Open"])
        
        return {
            "total_projects": total_projects,
            "projects_by_phase": by_phase,
            "open_challenges": open_challenges,
            "high_severity_challenges": high_severity_challenges,
            "university_profile": self.university_profile.name if self.university_profile else "Not set",
            "ai_maturity": self.university_profile.current_ai_maturity if self.university_profile else "Not assessed"
        }
    
    def export_university_data(self) -> Dict:
        """Exportera universitets AI-coaching data"""
        return {
            "university_profile": {
                "name": self.university_profile.name,
                "size": self.university_profile.size,
                "research_focus": self.university_profile.research_focus,
                "current_ai_maturity": self.university_profile.current_ai_maturity,
                "budget_range": self.university_profile.budget_range,
                "key_challenges": self.university_profile.key_challenges,
                "success_metrics": self.university_profile.success_metrics
            } if self.university_profile else None,
            "projects": {
                project_id: {
                    "title": project.title,
                    "description": project.description,
                    "use_case": project.use_case.value,
                    "phase": project.phase.value,
                    "stakeholders": [s.value for s in project.stakeholders],
                    "start_date": project.start_date.isoformat(),
                    "target_completion": project.target_completion.isoformat() if project.target_completion else None,
                    "success_criteria": project.success_criteria,
                    "risks": project.risks,
                    "progress_notes": project.progress_notes,
                    "kpis": project.kpis
                } for project_id, project in self.projects.items()
            },
            "challenges": {
                challenge_id: {
                    "title": challenge.title,
                    "description": challenge.description,
                    "category": challenge.category,
                    "severity": challenge.severity,
                    "stakeholders_affected": [s.value for s in challenge.stakeholders_affected],
                    "proposed_solutions": challenge.proposed_solutions,
                    "status": challenge.status,
                    "created_date": challenge.created_date.isoformat()
                } for challenge_id, challenge in self.challenges.items()
            }
        }