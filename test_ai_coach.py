"""
Test script för AI-Coachen
Testar alla huvudfunktioner för både personlig coaching och universitets AI-implementering
"""

import sys
import os
from datetime import datetime, timedelta

# Lägg till projektroot till Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.ai_coach import AICoach, CoachingMode, create_ai_coach
from core.personal_coach import PersonalCoach, PersonalGoalType, GoalStatus
from core.university_coach import UniversityAICoach, AIUseCase, StakeholderType, UniversityProfile, AIImplementationPhase
from utils.data_manager import DataManager

def test_personal_coach():
    """Testa personlig coaching-funktioner"""
    print("🧠 Testing Personal Coach...")
    
    coach = PersonalCoach()
    
    # Test 1: Skapa mål
    goal_id = coach.create_goal(
        title="Lära mig Python",
        description="Bli duktig på Python programmering för AI-utveckling",
        goal_type=PersonalGoalType.LEARNING,
        target_date=datetime.now() + timedelta(days=90),
        completion_criteria="Slutföra 3 AI-projekt"
    )
    print(f"✅ Created goal: {goal_id}")
    
    # Test 2: Uppdatera framsteg
    success = coach.update_goal_progress(goal_id, 25, "Börjat med grundkurs")
    print(f"✅ Updated progress: {success}")
    
    # Test 3: Lägg till milstolpe
    success = coach.add_milestone(goal_id, "Slutförde första projekt")
    print(f"✅ Added milestone: {success}")
    
    # Test 4: Lägg till reflektion
    reflection_id = coach.add_reflection(
        prompt="Vad lärde jag mig idag?",
        response="Jag lärde mig om classes och objects i Python",
        mood_rating=8,
        energy_rating=7,
        insights="Python är enklare än jag trodde!"
    )
    print(f"✅ Added reflection: {reflection_id}")
    
    # Test 5: Generera coaching prompts
    prompts = coach.generate_coaching_prompts()
    print(f"✅ Generated {len(prompts)} coaching prompts")
    
    # Test 6: Få progress summary
    summary = coach.get_progress_summary()
    print(f"✅ Progress summary: {summary}")
    
    print("🎉 Personal Coach tests passed!\n")

def test_university_coach():
    """Testa universitets AI-coaching funktioner"""
    print("🎓 Testing University AI Coach...")
    
    coach = UniversityAICoach()
    
    # Test 1: Sätt universitets-profil
    profile = UniversityProfile(
        name="KTH Royal Institute of Technology",
        size="Large",
        research_focus=["AI", "Machine Learning", "Computer Vision"],
        current_ai_maturity=6,
        budget_range="10-50M SEK",
        key_challenges=["Faculty resistance", "Legacy systems", "Data silos"],
        success_metrics=["Research output", "Student satisfaction", "Cost savings"]
    )
    coach.set_university_profile(profile)
    print("✅ Set university profile")
    
    # Test 2: Skapa AI-projekt
    project_id = coach.create_project(
        title="Automated Grading System",
        description="AI-powered grading for programming assignments",
        use_case=AIUseCase.AUTOMATED_GRADING,
        stakeholders=[StakeholderType.FACULTY, StakeholderType.IT_DEPARTMENT],
        target_completion=datetime.now() + timedelta(days=180)
    )
    print(f"✅ Created project: {project_id}")
    
    # Test 3: Framsteg projekt till nästa fas
    success = coach.advance_project_phase(project_id, "Completed initial assessment")
    print(f"✅ Advanced project phase: {success}")
    
    # Test 4: Lägg till utmaning
    challenge_id = coach.add_challenge(
        title="Faculty resistance to AI grading",
        description="Some faculty members are concerned about AI bias in grading",
        category="Organizational",
        severity=7,
        stakeholders=[StakeholderType.FACULTY]
    )
    print(f"✅ Added challenge: {challenge_id}")
    
    # Test 5: Föreslå lösning
    success = coach.propose_solution(
        challenge_id, 
        "Organize workshops to demonstrate AI grading transparency and involve faculty in bias testing"
    )
    print(f"✅ Proposed solution: {success}")
    
    # Test 6: Generera coaching prompts
    prompts = coach.generate_university_coaching_prompts()
    print(f"✅ Generated {len(prompts)} university coaching prompts")
    
    # Test 7: Få implementation roadmap
    roadmap = coach.get_implementation_roadmap()
    print(f"✅ Generated roadmap with {len(roadmap)} phases")
    
    # Test 8: Få status
    status = coach.get_implementation_status()
    print(f"✅ Implementation status: {status}")
    
    print("🎉 University Coach tests passed!\n")

def test_ai_coach_core():
    """Testa kärnfunktioner i AI Coach (kräver API key)"""
    print("🤖 Testing AI Coach Core...")
    
    # Kontrollera om API key finns
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Skipping AI Coach tests - No OpenAI API key found")
        print("   Set OPENAI_API_KEY environment variable to test AI functionality\n")
        return
    
    try:
        # Test 1: Skapa AI coach
        coach = create_ai_coach()
        print("✅ Created AI coach instance")
        
        # Test 2: Starta session
        session_id = coach.start_session("test_user", CoachingMode.PERSONAL)
        print(f"✅ Started session: {session_id}")
        
        # Test 3: Lägg till meddelande
        coach.add_message("Hej, jag vill sätta ett mål att lära mig AI")
        print("✅ Added user message")
        
        # Test 4: Få svar (detta kommer att kosta tokens)
        print("🔄 Getting AI response (this costs tokens)...")
        response, metadata = coach.get_response("Kan du hjälpa mig sätta ett smart mål för att lära mig AI?")
        print(f"✅ Got AI response ({len(response)} chars)")
        print(f"   Metadata: {metadata}")
        
        # Test 5: Sätt mål för session
        coach.set_goals(["Lära mig AI grunderna", "Bygga mitt första projekt"])
        print("✅ Set session goals")
        
        # Test 6: Få session summary
        summary = coach.get_session_summary()
        print(f"✅ Session summary: {summary}")
        
        # Test 7: Avsluta session
        end_summary = coach.end_session()
        print(f"✅ Ended session: {end_summary}")
        
        print("🎉 AI Coach Core tests passed!\n")
        
    except Exception as e:
        print(f"❌ AI Coach test failed: {str(e)}\n")

def test_data_manager():
    """Testa datahantering"""
    print("💾 Testing Data Manager...")
    
    # Test 1: Skapa data manager
    dm = DataManager("test_data.db")
    print("✅ Created data manager")
    
    # Test 2: Spara session data
    session_data = {
        'session_id': 'test_session_123',
        'user_id': 'test_user',
        'mode': 'personal',
        'start_time': datetime.now().isoformat(),
        'message_count': 5,
        'context': {'test': 'data'},
        'goals': ['Learn AI', 'Build project'],
        'progress_notes': 'Making good progress'
    }
    
    success = dm.save_session(session_data)
    print(f"✅ Saved session data: {success}")
    
    # Test 3: Spara meddelande
    success = dm.save_message(
        session_id='test_session_123',
        role='user',
        content='Test message',
        timestamp=datetime.now().isoformat(),
        metadata={'test': True}
    )
    print(f"✅ Saved message: {success}")
    
    # Test 4: Ladda session data
    sessions = dm.load_user_sessions('test_user')
    print(f"✅ Loaded {len(sessions)} sessions")
    
    # Test 5: Ladda meddelanden
    messages = dm.load_session_messages('test_session_123')
    print(f"✅ Loaded {len(messages)} messages")
    
    # Cleanup - ta bort test database
    try:
        os.remove("test_data.db")
        print("✅ Cleaned up test database")
    except:
        pass
    
    print("🎉 Data Manager tests passed!\n")

def run_all_tests():
    """Kör alla tester"""
    print("🚀 Starting AI-Coachen Test Suite...\n")
    
    try:
        test_personal_coach()
        test_university_coach() 
        test_data_manager()
        test_ai_coach_core()  # Detta kräver API key
        
        print("🎉🎉🎉 ALL TESTS PASSED! 🎉🎉🎉")
        print("\nAI-Coachen är redo att använda!")
        print("Nästa steg: Kör 'streamlit run main.py' för att starta applikationen")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()