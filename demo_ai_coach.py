"""
Demo script för AI-Coachen
Visar funktionalitet utan att kräva API-nycklar
"""

import sys
import os
from datetime import datetime, timedelta

# Lägg till projektroot till Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.personal_coach import PersonalCoach, PersonalGoalType, GoalStatus
from core.university_coach import UniversityAICoach, AIUseCase, StakeholderType, UniversityProfile, AIImplementationPhase

def demo_personal_coaching():
    """Demonstrera personlig coaching"""
    print("=" * 60)
    print("🧠 PERSONAL COACHING DEMO")
    print("=" * 60)
    
    coach = PersonalCoach()
    
    print("\n📝 Skapar personliga utvecklingsmål...")
    
    # Skapa flera mål
    goal1 = coach.create_goal(
        title="Lära mig AI och Machine Learning",
        description="Bygga upp djup kompetens inom AI för att kunna implementera det på universitetet",
        goal_type=PersonalGoalType.LEARNING,
        target_date=datetime.now() + timedelta(days=180),
        completion_criteria="Slutföra online-kurs, bygga 3 projekt, få certifiering"
    )
    
    goal2 = coach.create_goal(
        title="Utveckla ledarskap för digital transformation",
        description="Bygga färdigheter för att leda AI-implementering på organisationsnivå",
        goal_type=PersonalGoalType.CAREER,
        target_date=datetime.now() + timedelta(days=120),
        completion_criteria="Genomföra ledarskapskurs, mentoring, framgångsrik pilot-implementation"
    )
    
    goal3 = coach.create_goal(
        title="Förbättra work-life balance under förändring",
        description="Behålla välmående medan jag driver stora förändringsprocesser",
        goal_type=PersonalGoalType.PERSONAL,
        target_date=datetime.now() + timedelta(days=90),
        completion_criteria="Etablera dagliga rutiner, minska stress, öka energinivå"
    )
    
    print(f"✅ Skapat mål: {goal1}")
    print(f"✅ Skapat mål: {goal2}")
    print(f"✅ Skapat mål: {goal3}")
    
    print("\n📈 Uppdaterar framsteg på målen...")
    
    # Simulera framsteg
    coach.update_goal_progress(goal1, 35, "Slutförde grundkurs i ML, började med första projektet")
    coach.update_goal_progress(goal2, 20, "Påbörjat ledarskapsprogram, identifierat mentorer")
    coach.update_goal_progress(goal3, 60, "Etablerat morgonrutin och mindfulness-praktik")
    
    # Lägg till milstolpar
    coach.add_milestone(goal1, "Slutförde Coursera ML-kurs med betyg A")
    coach.add_milestone(goal1, "Byggde första ChatBot med Python")
    coach.add_milestone(goal2, "Fick godkännande för AI-pilot på min avdelning")
    coach.add_milestone(goal3, "Genomförde första veckan med 7h sömn per natt")
    
    print("✅ Framsteg uppdaterat för alla mål")
    print("✅ Milstolpar tillagda")
    
    print("\n🤔 Lägger till reflektioner...")
    
    # Lägg till reflektioner
    coach.add_reflection(
        prompt="Vad har fungerat bäst i min AI-inlärning hittills?",
        response="Hands-on projekt har varit mycket mer värdefullt än bara teori. Att bygga något konkret hjälper mig förstå koncepten djupare.",
        mood_rating=8,
        energy_rating=7,
        insights="Praktisk tillämpning är nyckeln till djup förståelse"
    )
    
    coach.add_reflection(
        prompt="Hur hanterar jag stressen av att lära mig snabbt?",
        response="Jag märker att jag blir överambitiös och försöker lära mig för mycket på en gång. Behöver fokusera på kvalitet över kvantitet.",
        mood_rating=6,
        energy_rating=5,
        insights="Behöver bättre balans mellan utmaning och återhämtning"
    )
    
    print("✅ Reflektioner tillagda")
    
    print("\n💡 Genererar coaching-prompts baserat på din situation...")
    prompts = coach.generate_coaching_prompts()
    
    print("\n🎯 FÖRESLAGNA COACHING-FRÅGOR:")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"{i}. {prompt}")
    
    print("\n📊 PROGRESS SAMMANFATTNING:")
    summary = coach.get_progress_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    print("\n💭 PERSONLIGA RÅD:")
    advice = coach.get_personalized_advice()
    for tip in advice:
        print(f"   💡 {tip}")
    
    print("\n🎉 Personal Coaching Demo slutförd!")

def demo_university_ai_coaching():
    """Demonstrera universitets AI-coaching"""
    print("\n\n" + "=" * 60)
    print("🎓 UNIVERSITY AI COACHING DEMO")
    print("=" * 60)
    
    coach = UniversityAICoach()
    
    print("\n🏛️ Sätter upp universitetsprofil...")
    
    # Sätt universitetsprofil
    profile = UniversityProfile(
        name="Svenskt Universitet för Teknik och Innovation",
        size="Medium",
        research_focus=["Artificial Intelligence", "Sustainable Technology", "Digital Health", "Cybersecurity"],
        current_ai_maturity=4,  # På en skala 1-10
        budget_range="50-100M SEK",
        key_challenges=[
            "Bristande AI-kompetens bland faculty",
            "Fragmenterade datasystem",
            "Motstånd mot förändring",
            "Begränsade resurser för implementering",
            "Etiska och regulatoriska concerns"
        ],
        success_metrics=[
            "Ökad forskningsproduktivitet",
            "Förbättrade studentresultat", 
            "Kostnadseffektivitet i administration",
            "Konkurrenskraft internationellt"
        ]
    )
    
    coach.set_university_profile(profile)
    print(f"✅ Universitetsprofil satt för: {profile.name}")
    print(f"   AI-mognad: {profile.current_ai_maturity}/10")
    print(f"   Forskningsfokus: {', '.join(profile.research_focus)}")
    
    print("\n🚀 Skapar AI-implementeringsprojekt...")
    
    # Skapa olika AI-projekt
    project1 = coach.create_project(
        title="Intelligent Forskningsassistent",
        description="AI-driven system för att hjälpa forskare hitta relevanta publikationer och identifiera samarbetsmöjligheter",
        use_case=AIUseCase.RESEARCH_ACCELERATION,
        stakeholders=[StakeholderType.RESEARCHERS, StakeholderType.IT_DEPARTMENT, StakeholderType.LEADERSHIP],
        target_completion=datetime.now() + timedelta(days=365)
    )
    
    project2 = coach.create_project(
        title="Adaptiv Lärplattform",
        description="Personaliserad lärupplevelse som anpassar sig till studenters individuella behov och lärstilar",
        use_case=AIUseCase.PERSONALIZED_LEARNING,
        stakeholders=[StakeholderType.FACULTY, StakeholderType.STUDENTS, StakeholderType.IT_DEPARTMENT],
        target_completion=datetime.now() + timedelta(days=270)
    )
    
    project3 = coach.create_project(
        title="Smart Campus Operations",
        description="AI-optimering av campus-resurser: energiförbrukning, säkerhet, och logistik",
        use_case=AIUseCase.ADMINISTRATIVE_AUTOMATION,
        stakeholders=[StakeholderType.ADMINISTRATION, StakeholderType.IT_DEPARTMENT],
        target_completion=datetime.now() + timedelta(days=180)
    )
    
    print(f"✅ Skapat projekt: {project1}")
    print(f"✅ Skapat projekt: {project2}")
    print(f"✅ Skapat projekt: {project3}")
    
    print("\n⚡ Avancerar projekt genom implementeringsfaser...")
    
    # Simulera projektframsteg
    coach.advance_project_phase(project3, "Slutförde teknisk feasibility study - mycket lovande resultat")
    coach.advance_project_phase(project3, "Godkännande från IT och administration erhållet")
    coach.advance_project_phase(project2, "Pilotgrupp med 50 studenter identifierad och rekryterad")
    
    print("✅ Projekt avancerade till nästa fas")
    
    print("\n⚠️ Identifierar och hanterar implementationsutmaningar...")
    
    # Lägg till utmaningar
    challenge1 = coach.add_challenge(
        title="Faculty motstånd mot AI i undervisning",
        description="Många lärare är oroliga att AI kommer att ersätta dem eller minska undervisningskvaliteten",
        category="Organizational",
        severity=8,
        stakeholders=[StakeholderType.FACULTY, StakeholderType.LEADERSHIP]
    )
    
    challenge2 = coach.add_challenge(
        title="Datasäkerhet och integritet",
        description="Oro för hur studentdata och forskningsdata kommer att hanteras av AI-system",
        category="Ethical",
        severity=9,
        stakeholders=[StakeholderType.STUDENTS, StakeholderType.RESEARCHERS, StakeholderType.ADMINISTRATION]
    )
    
    challenge3 = coach.add_challenge(
        title="Budget och resursbegränsningar",
        description="Begränsad budget för AI-infrastruktur och kompetensuppbyggnad",
        category="Financial",
        severity=7,
        stakeholders=[StakeholderType.LEADERSHIP, StakeholderType.ADMINISTRATION]
    )
    
    print(f"⚠️ Utmaning identifierad: {challenge1}")
    print(f"⚠️ Utmaning identifierad: {challenge2}")
    print(f"⚠️ Utmaning identifierad: {challenge3}")
    
    # Föreslå lösningar
    coach.propose_solution(challenge1, "Organisera hands-on workshops där faculty får testa AI-verktyg som stöd snarare än ersättning")
    coach.propose_solution(challenge1, "Skapa AI champions-program med early adopters som ambassadörer")
    coach.propose_solution(challenge1, "Utveckla tydliga riktlinjer för när och hur AI ska användas i undervisning")
    
    coach.propose_solution(challenge2, "Implementera privacy-by-design principer i alla AI-system")
    coach.propose_solution(challenge2, "Skapa transparent datahanteringspolicy och få studentgodkännande")
    coach.propose_solution(challenge2, "Använda federated learning för att minimera centraliserad datalagring")
    
    coach.propose_solution(challenge3, "Starta med small-scale piloter som visar ROI innan större investeringar")
    coach.propose_solution(challenge3, "Söka externa forskningsanslag för AI-implementering")
    coach.propose_solution(challenge3, "Partnerships med teknologiföretag för delad kostnad och expertis")
    
    print("✅ Lösningar föreslagna för alla utmaningar")
    
    print("\n🎯 Genererar coaching-prompts för universitets-context...")
    prompts = coach.generate_university_coaching_prompts()
    
    print("\n📋 UNIVERSITETS COACHING-FRÅGOR:")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"{i}. {prompt}")
    
    print("\n🗺️ AI-IMPLEMENTERINGS ROADMAP:")
    roadmap = coach.get_implementation_roadmap()
    
    for phase in roadmap:
        print(f"\n📅 {phase['phase']} ({phase['duration']})")
        print("   Aktiviteter:")
        for activity in phase['activities']:
            print(f"   • {activity}")
        print("   Leverabler:")
        for deliverable in phase['deliverables']:
            print(f"   📋 {deliverable}")
    
    print("\n📊 IMPLEMENTERINGSSTATUS:")
    status = coach.get_implementation_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n🚨 RISKANALYS OCH REKOMMENDATIONER:")
    risks = coach.get_risk_assessment()
    
    for risk_category in risks:
        print(f"\n⚠️ {risk_category['category']} Risker:")
        for risk in risk_category['risks']:
            print(f"   • {risk}")
        print("   Åtgärder:")
        for mitigation in risk_category['mitigation']:
            print(f"   ✓ {mitigation}")
    
    print("\n🎉 University AI Coaching Demo slutförd!")

def demo_stakeholder_strategies():
    """Demonstrera stakeholder-specifika strategier"""
    print("\n\n" + "=" * 60)
    print("👥 STAKEHOLDER STRATEGIER DEMO")
    print("=" * 60)
    
    coach = UniversityAICoach()
    
    stakeholders = [StakeholderType.FACULTY, StakeholderType.RESEARCHERS, StakeholderType.IT_DEPARTMENT, StakeholderType.ADMINISTRATION]
    
    for stakeholder in stakeholders:
        print(f"\n🎯 STRATEGI FÖR: {stakeholder.value.upper()}")
        print("-" * 50)
        
        strategy = coach.get_stakeholder_strategy(stakeholder)
        
        if strategy:
            print("📋 Huvudconcerns:")
            for concern in strategy['key_concerns']:
                print(f"   • {concern}")
            
            print("\n🤝 Engagement Approach:")
            for approach in strategy['engagement_approach']:
                print(f"   • {approach}")
            
            print("\n📈 Success Metrics:")
            for metric in strategy['success_metrics']:
                print(f"   • {metric}")
        else:
            print("   Ingen specifik strategi tillgänglig")

def main():
    """Kör fullständig demo"""
    print("🤖🎓 AI-COACHEN FUNKTIONALITETS-DEMO")
    print("Denna demo visar alla funktioner utan att kräva API-nycklar")
    print("\n" + "=" * 80)
    
    try:
        demo_personal_coaching()
        demo_university_ai_coaching()
        demo_stakeholder_strategies()
        
        print("\n\n" + "🎉" * 20)
        print("DEMO SLUTFÖRD FRAMGÅNGSRIKT!")
        print("🎉" * 20)
        
        print(f"""
✨ SAMMANFATTNING AV AI-COACHEN:

🧠 PERSONLIG COACHING:
   • Målsättning och progress tracking
   • Reflektioner och självutvärdering  
   • Personaliserade råd och coaching-prompts
   • Mood och energy tracking

🎓 UNIVERSITETS AI-IMPLEMENTERING:
   • Strategisk planering och roadmap
   • Projekthantering genom implementeringsfaser
   • Utmaningsidentifiering och lösningsförslag
   • Stakeholder-specifika strategier
   • Risk assessment och mitigation

🔄 HYBRID FUNCTIONALITY:
   • Kombinerar personlig utveckling med AI-expertis
   • Hjälper dig både som individ och som ledare
   • Integrerad approach för holistisk coaching

📚 NÄSTA STEG:
   1. Sätt upp din OpenAI API-nyckel i .env filen
   2. Kör: streamlit run main.py
   3. Börja din AI-coaching resa!

Lycka till med din AI-transformation! 🚀
        """)
        
    except Exception as e:
        print(f"\n❌ Demo misslyckades: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()