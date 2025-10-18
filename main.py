"""
Huvudapplikation för AI-Coachen
Streamlit-baserat gränssnitt för både personlig coaching och universitets AI-implementering
"""

import streamlit as st
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Ladda environment variables
load_dotenv()

# Kontrollera om vi kör i molnmiljö (Render)
IS_CLOUD_DEPLOYMENT = os.getenv('RENDER') is not None or os.getenv('PORT') is not None

# Importera våra moduler
from core.ai_coach import AICoach, CoachingMode, create_ai_coach
from core.personal_coach import PersonalCoach, PersonalGoalType, GoalStatus
from core.university_coach import UniversityAICoach, AIUseCase, StakeholderType, UniversityProfile, AIImplementationPhase
from utils.data_manager import DataManager
from utils.api_usage_tracker import usage_tracker

# Streamlit konfiguration
st.set_page_config(
    page_title="AI-Coachen 🤖🎓",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisera session state
if 'ai_coach' not in st.session_state:
    try:
        st.session_state.ai_coach = create_ai_coach()
    except ValueError as e:
        st.error(f"Fel vid initialisering av AI-coach: {str(e)}")
        st.stop()

if 'personal_coach' not in st.session_state:
    st.session_state.personal_coach = PersonalCoach()

if 'university_coach' not in st.session_state:
    st.session_state.university_coach = UniversityAICoach()

if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()

if 'current_mode' not in st.session_state:
    st.session_state.current_mode = CoachingMode.HYBRID

if 'session_started' not in st.session_state:
    st.session_state.session_started = False

if 'selected_blog_post' not in st.session_state:
    st.session_state.selected_blog_post = None

def main():
    """Huvudfunktion för applikationen"""
    
    # Sidebar för navigation och inställningar
    with st.sidebar:
        st.title("🤖 AI-Coachen")
        st.markdown("Din intelligenta coach för personlig utveckling och AI-implementering")
        
        # Mode selection
        mode_options = {
            "Personlig Coach": CoachingMode.PERSONAL,
            "Universitets AI-Coach": CoachingMode.UNIVERSITY, 
            "Hybrid (Båda)": CoachingMode.HYBRID
        }
        
        selected_mode = st.selectbox(
            "Välj coaching-läge:",
            options=list(mode_options.keys()),
            index=2  # Default to Hybrid
        )
        
        st.session_state.current_mode = mode_options[selected_mode]
        
        # Session management
        st.subheader("Session")
        if not st.session_state.session_started:
            if st.button("Starta Coaching-Session"):
                user_id = "user_1"  # I production, detta skulle komma från auth
                session_id = st.session_state.ai_coach.start_session(
                    user_id=user_id,
                    mode=st.session_state.current_mode
                )
                st.session_state.session_started = True
                st.session_state.session_id = session_id
                st.success(f"Session startad: {session_id}")
                st.rerun()
        else:
            st.success("✅ Session aktiv")
            if st.button("Avsluta Session"):
                summary = st.session_state.ai_coach.end_session()
                st.session_state.session_started = False
                st.info("Session avslutad")
                st.json(summary)
        
        # Quick stats
        if st.session_state.session_started:
            st.subheader("Session Info")
            summary = st.session_state.ai_coach.get_session_summary()
            st.metric("Meddelanden", summary.get('message_count', 0))
            st.metric("Läge", summary.get('mode', 'N/A'))
    
    # Main content area
    if not st.session_state.session_started:
        show_main_navigation()
    else:
        show_coaching_interface()

def show_main_navigation():
    """Visa huvudnavigation med blog och coaching"""
    st.title("AI-Coachen 🤖🎓")
    
    # Navigation tabs
    main_tabs = st.tabs(["🏠 Hem", "📰 Blog", "🤖 Starta Coaching"])
    
    with main_tabs[0]:
        show_welcome_content()
    
    with main_tabs[1]:
        show_blog_interface()
        
    with main_tabs[2]:
        show_coaching_start()

def show_welcome_content():
    """Visa välkomstinnehåll"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🧠 Personlig Coach")
        st.markdown("""
        **Utveckla dig själv med AI-hjälp:**
        - Sätt och följ upp personliga mål
        - Få motiverande coaching och feedback
        - Reflektion och progress tracking  
        - Anpassad utvecklingsplan
        - Balans mellan arbete och välmående
        """)
        
        if st.button("Starta Personlig Coaching", type="primary"):
            st.session_state.current_mode = CoachingMode.PERSONAL
            user_id = "user_1"
            session_id = st.session_state.ai_coach.start_session(user_id, CoachingMode.PERSONAL)
            st.session_state.session_started = True
            st.session_state.session_id = session_id
            st.rerun()
    
    with col2:
        st.header("🎓 Universitets AI-Coach")
        st.markdown("""
        **Implementera AI på ditt universitet:**
        - Strategisk planering för AI-adoption
        - Forskningsintegration och metodologi
        - Stakeholder management och training
        - Etiska riktlinjer och compliance
        - Projektledning och riskhantering
        """)
        
        if st.button("Starta Universitets-Coaching", type="primary"):
            st.session_state.current_mode = CoachingMode.UNIVERSITY
            user_id = "user_1"  
            session_id = st.session_state.ai_coach.start_session(user_id, CoachingMode.UNIVERSITY)
            st.session_state.session_started = True
            st.session_state.session_id = session_id
            st.rerun()
    
    st.markdown("---")
    
    # Hybrid option
    st.header("🔄 Hybrid Coaching")
    st.markdown("""
    **Få det bästa av båda världarna:**
    Kombinerar personlig utveckling med AI-expertis för att hjälpa dig både som individ 
    och som ledare i AI-transformation på universitet.
    """)
    
    if st.button("Starta Hybrid Coaching", type="primary"):
        st.session_state.current_mode = CoachingMode.HYBRID
        user_id = "user_1"
        session_id = st.session_state.ai_coach.start_session(user_id, CoachingMode.HYBRID)
        st.session_state.session_started = True
        st.session_state.session_id = session_id
        st.rerun()

def show_coaching_interface():
    """Visa coaching-gränssnittet"""
    
    # Skapa tabs baserat på läge
    if st.session_state.current_mode == CoachingMode.PERSONAL:
        tabs = st.tabs(["💬 Chat", "🎯 Mål", "📝 Reflektion", "📊 Progress", "💳 API Usage"])
        
        with tabs[0]:
            show_chat_interface()
        with tabs[1]:
            show_personal_goals_interface()
        with tabs[2]:
            show_reflection_interface()
        with tabs[3]:
            show_personal_progress_interface()
        with tabs[4]:
            show_api_usage_interface()
            
    elif st.session_state.current_mode == CoachingMode.UNIVERSITY:
        tabs = st.tabs(["💬 Chat", "🏗️ Projekt", "⚠️ Utmaningar", "📈 Status", "🗺️ Roadmap", "💳 API Usage"])
        
        with tabs[0]:
            show_chat_interface()
        with tabs[1]:
            show_university_projects_interface()
        with tabs[2]:
            show_challenges_interface()
        with tabs[3]:
            show_university_status_interface()
        with tabs[4]:
            show_roadmap_interface()
        with tabs[5]:
            show_api_usage_interface()
            
    else:  # HYBRID
        tabs = st.tabs(["💬 Chat", "🎯 Personliga Mål", "🏗️ AI-Projekt", "📊 Översikt", "💳 API Usage"])
        
        with tabs[0]:
            show_chat_interface()
        with tabs[1]:
            show_personal_goals_interface()
        with tabs[2]:
            show_university_projects_interface()
        with tabs[3]:
            show_hybrid_overview_interface()
        with tabs[4]:
            show_api_usage_interface()

def show_chat_interface():
    """Visa chat-gränssnitt"""
    st.header("💬 Coaching Conversation")
    
    # Chat history
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "timestamp" in message:
                st.caption(message["timestamp"])
    
    # Chat input
    if prompt := st.chat_input("Skriv ditt meddelande här..."):
        # Add user message to chat history
        st.session_state.chat_messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Get AI response
        try:
            response, metadata = st.session_state.ai_coach.get_response(prompt)
            
            # Add assistant response to chat history
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": response, 
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Fel vid kommunikation med AI-coach: {str(e)}")
    
    # Quick prompts baserat på läge
    st.subheader("💡 Föreslagna Frågor")
    
    if st.session_state.current_mode == CoachingMode.PERSONAL:
        prompts = st.session_state.personal_coach.generate_coaching_prompts()
    elif st.session_state.current_mode == CoachingMode.UNIVERSITY:
        prompts = st.session_state.university_coach.generate_university_coaching_prompts()
    else:
        prompts = (st.session_state.personal_coach.generate_coaching_prompts()[:2] + 
                  st.session_state.university_coach.generate_university_coaching_prompts()[:2])
    
    for i, prompt in enumerate(prompts[:4]):  # Visa max 4 förslag
        if st.button(prompt, key=f"prompt_{i}"):
            # Simulera att användaren klickade på prompten
            st.session_state.chat_messages.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            try:
                response, metadata = st.session_state.ai_coach.get_response(prompt)
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.rerun()
            except Exception as e:
                st.error(f"Fel: {str(e)}")

def show_personal_goals_interface():
    """Visa personliga mål-gränssnitt"""
    st.header("🎯 Personliga Mål")
    
    # Skapa nytt mål
    with st.expander("➕ Skapa Nytt Mål"):
        with st.form("new_goal_form"):
            title = st.text_input("Måltitel")
            description = st.text_area("Beskrivning")
            goal_type = st.selectbox("Måltyp", [t.value for t in PersonalGoalType])
            target_date = st.date_input("Målsatt slutdatum (valfritt)")
            completion_criteria = st.text_area("Framgångskriterier")
            
            if st.form_submit_button("Skapa Mål"):
                if title and description:
                    goal_type_enum = PersonalGoalType(goal_type)
                    target_datetime = datetime.combine(target_date, datetime.min.time()) if target_date else None
                    
                    goal_id = st.session_state.personal_coach.create_goal(
                        title=title,
                        description=description,
                        goal_type=goal_type_enum,
                        target_date=target_datetime,
                        completion_criteria=completion_criteria
                    )
                    st.success(f"Mål skapat: {goal_id}")
                    st.rerun()
                else:
                    st.error("Titel och beskrivning krävs")
    
    # Visa aktiva mål
    active_goals = st.session_state.personal_coach.get_active_goals()
    
    if active_goals:
        st.subheader("🚀 Aktiva Mål")
        
        for goal in active_goals:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{goal.title}**")
                    st.write(goal.description)
                    if goal.target_date:
                        days_left = (goal.target_date - datetime.now()).days
                        if days_left > 0:
                            st.info(f"⏰ {days_left} dagar kvar")
                        else:
                            st.warning("⚠️ Försenat")
                
                with col2:
                    st.metric("Progress", f"{goal.progress_percentage}%")
                    st.progress(goal.progress_percentage / 100)
                
                with col3:
                    new_progress = st.number_input(
                        "Uppdatera %", 
                        min_value=0, 
                        max_value=100,
                        value=goal.progress_percentage,
                        key=f"progress_{goal.id}"
                    )
                    
                    if st.button("Uppdatera", key=f"update_{goal.id}"):
                        st.session_state.personal_coach.update_goal_progress(
                            goal.id, 
                            new_progress
                        )
                        st.success("Progress uppdaterad!")
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("Inga aktiva mål än. Skapa ditt första mål ovan! 🎯")

def show_reflection_interface():
    """Visa reflektionsgränssnitt"""
    st.header("📝 Reflektion & Självutvärdering")
    
    # Ny reflektion
    with st.expander("✨ Ny Reflektion"):
        prompts = st.session_state.personal_coach.generate_weekly_review_questions()
        selected_prompt = st.selectbox("Välj reflektionsfråga:", ["Egen fråga..."] + prompts)
        
        if selected_prompt == "Egen fråga...":
            prompt = st.text_input("Din egen reflektionsfråga:")
        else:
            prompt = selected_prompt
            
        response = st.text_area("Ditt svar:", height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            mood = st.slider("Humör (1-10)", 1, 10, 7)
        with col2:
            energy = st.slider("Energinivå (1-10)", 1, 10, 7)
            
        insights = st.text_area("Insikter och lärdomar:", height=100)
        
        if st.button("Spara Reflektion"):
            if prompt and response:
                reflection_id = st.session_state.personal_coach.add_reflection(
                    prompt=prompt,
                    response=response,
                    mood_rating=mood,
                    energy_rating=energy,
                    insights=insights
                )
                st.success("Reflektion sparad!")
                st.rerun()
            else:
                st.error("Fråga och svar krävs")
    
    # Visa senaste reflektioner
    recent_reflections = st.session_state.personal_coach.get_recent_reflections(14)
    
    if recent_reflections:
        st.subheader("🔍 Senaste Reflektioner")
        
        for reflection in recent_reflections[-5:]:  # Visa senaste 5
            with st.expander(f"📅 {reflection.date.strftime('%Y-%m-%d')} - {reflection.prompt[:50]}..."):
                st.write("**Fråga:** " + reflection.prompt)
                st.write("**Svar:** " + reflection.response)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Humör", f"{reflection.mood_rating}/10")
                with col2:
                    st.metric("Energi", f"{reflection.energy_rating}/10")
                
                if reflection.insights:
                    st.write("**Insikter:** " + reflection.insights)
    else:
        st.info("Inga reflektioner än. Börja reflektera för bättre självkännedom! 🤔")

def show_personal_progress_interface():
    """Visa personlig progress-översikt"""
    st.header("📊 Progress Översikt")
    
    summary = st.session_state.personal_coach.get_progress_summary()
    
    if "message" in summary:
        st.info(summary["message"])
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Totala Mål", summary["total_goals"])
    with col2:
        st.metric("Slutförda", summary["completed_goals"])
    with col3:
        st.metric("Pågående", summary["in_progress_goals"])
    with col4:
        st.metric("Slutförandegrad", summary["completion_rate"])
    
    # Progress chart (simpel version)
    st.subheader("📈 Målfördelning")
    
    # Personliga råd
    advice = st.session_state.personal_coach.get_personalized_advice()
    if advice:
        st.subheader("💡 Personliga Råd")
        for tip in advice:
            st.info(tip)

def show_university_projects_interface():
    """Visa universitets AI-projekt gränssnitt"""
    st.header("🏗️ AI-Projekt på Universitetet")
    
    # Skapa nytt projekt
    with st.expander("➕ Skapa Nytt AI-Projekt"):
        with st.form("new_project_form"):
            title = st.text_input("Projekttitel")
            description = st.text_area("Projektbeskrivning")
            use_case = st.selectbox("AI Use Case", [uc.value for uc in AIUseCase])
            stakeholders = st.multiselect("Involverade Stakeholders", [s.value for s in StakeholderType])
            target_date = st.date_input("Målsatt slutdatum (valfritt)")
            
            if st.form_submit_button("Skapa Projekt"):
                if title and description and stakeholders:
                    use_case_enum = AIUseCase(use_case)
                    stakeholder_enums = [StakeholderType(s) for s in stakeholders]
                    target_datetime = datetime.combine(target_date, datetime.min.time()) if target_date else None
                    
                    project_id = st.session_state.university_coach.create_project(
                        title=title,
                        description=description,
                        use_case=use_case_enum,
                        stakeholders=stakeholder_enums,
                        target_completion=target_datetime
                    )
                    st.success(f"Projekt skapat: {project_id}")
                    st.rerun()
                else:
                    st.error("Titel, beskrivning och stakeholders krävs")
    
    # Visa aktiva projekt
    projects = list(st.session_state.university_coach.projects.values())
    
    if projects:
        st.subheader("📋 Aktiva Projekt")
        
        for project in projects:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**{project.title}**")
                    st.write(project.description)
                    st.write(f"**Use Case:** {project.use_case.value}")
                    st.write(f"**Stakeholders:** {', '.join([s.value for s in project.stakeholders])}")
                
                with col2:
                    st.metric("Fas", project.phase.value)
                    
                    if st.button("Nästa Fas", key=f"advance_{project.id}"):
                        if st.session_state.university_coach.advance_project_phase(project.id):
                            st.success("Projekt avancerat till nästa fas!")
                            st.rerun()
                        else:
                            st.info("Projekt redan i slutfas")
                
                st.markdown("---")
    else:
        st.info("Inga AI-projekt än. Skapa ditt första projekt ovan! 🚀")

def show_challenges_interface():
    """Visa utmanings-hantering gränssnitt"""
    st.header("⚠️ Implementationsutmaningar")
    
    # Lägg till ny utmaning
    with st.expander("➕ Rapportera Ny Utmaning"):
        with st.form("new_challenge_form"):
            title = st.text_input("Utmaningens titel")
            description = st.text_area("Detaljerad beskrivning")
            category = st.selectbox("Kategori", ["Technical", "Organizational", "Financial", "Ethical"])
            severity = st.slider("Allvarlighetsgrad (1-10)", 1, 10, 5)
            stakeholders = st.multiselect("Påverkade Stakeholders", [s.value for s in StakeholderType])
            
            if st.form_submit_button("Rapportera Utmaning"):
                if title and description and stakeholders:
                    stakeholder_enums = [StakeholderType(s) for s in stakeholders]
                    
                    challenge_id = st.session_state.university_coach.add_challenge(
                        title=title,
                        description=description,
                        category=category,
                        severity=severity,
                        stakeholders=stakeholder_enums
                    )
                    st.success(f"Utmaning rapporterad: {challenge_id}")
                    st.rerun()
                else:
                    st.error("Alla fält krävs")
    
    # Visa aktiva utmaningar
    challenges = list(st.session_state.university_coach.challenges.values())
    open_challenges = [c for c in challenges if c.status == "Open"]
    
    if open_challenges:
        st.subheader("🚨 Öppna Utmaningar")
        
        for challenge in sorted(open_challenges, key=lambda x: x.severity, reverse=True):
            severity_color = "🔴" if challenge.severity >= 8 else "🟡" if challenge.severity >= 5 else "🟢"
            
            with st.expander(f"{severity_color} {challenge.title} (Severity: {challenge.severity}/10)"):
                st.write(f"**Kategori:** {challenge.category}")
                st.write(f"**Beskrivning:** {challenge.description}")
                st.write(f"**Påverkade:** {', '.join([s.value for s in challenge.stakeholders_affected])}")
                
                # Lägg till lösningsförslag
                st.write("**Lösningsförslag:**")
                for solution in challenge.proposed_solutions:
                    st.write(f"- {solution}")
                
                new_solution = st.text_input(f"Lägg till lösning:", key=f"solution_{challenge.id}")
                if st.button("Lägg till", key=f"add_solution_{challenge.id}"):
                    if new_solution:
                        st.session_state.university_coach.propose_solution(challenge.id, new_solution)
                        st.success("Lösning tillagd!")
                        st.rerun()
    else:
        st.info("Inga öppna utmaningar. Bra jobbat! 🎉")

def show_university_status_interface():
    """Visa universitets AI-status översikt"""
    st.header("📈 AI-Implementering Status")
    
    status = st.session_state.university_coach.get_implementation_status()
    
    if "message" in status:
        st.info(status["message"])
        return
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Totala Projekt", status["total_projects"])
    with col2:
        st.metric("Öppna Utmaningar", status["open_challenges"]) 
    with col3:
        st.metric("Högprioriterade Utmaningar", status["high_severity_challenges"])
    
    # Projekt per fas
    st.subheader("📊 Projekt per Implementationsfas")
    for phase, count in status["projects_by_phase"].items():
        if count > 0:
            st.write(f"**{phase.replace('_', ' ').title()}:** {count} projekt")

def show_roadmap_interface():
    """Visa implementationsroadmap"""
    st.header("🗺️ AI-Implementering Roadmap")
    
    roadmap = st.session_state.university_coach.get_implementation_roadmap()
    
    for phase_info in roadmap:
        with st.expander(f"📅 {phase_info['phase']} ({phase_info['duration']})"):
            st.write("**Aktiviteter:**")
            for activity in phase_info['activities']:
                st.write(f"• {activity}")
            
            st.write("**Leverabler:**")
            for deliverable in phase_info['deliverables']:
                st.write(f"📋 {deliverable}")

def show_hybrid_overview_interface():
    """Visa hybrid-översikt"""
    st.header("🔄 Hybrid Coaching Översikt")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Personlig Utveckling")
        personal_summary = st.session_state.personal_coach.get_progress_summary()
        
        if "message" not in personal_summary:
            st.metric("Aktiva Mål", personal_summary.get("in_progress_goals", 0))
            st.metric("Slutförandgrad", personal_summary.get("completion_rate", "0%"))
        else:
            st.info("Inga personliga mål satta än")
    
    with col2:
        st.subheader("🎓 AI-Implementering")
        university_status = st.session_state.university_coach.get_implementation_status()
        
        if "message" not in university_status:
            st.metric("AI-Projekt", university_status.get("total_projects", 0))
            st.metric("Utmaningar", university_status.get("open_challenges", 0))
        else:
            st.info("Inga AI-projekt startade än")
    
    # Kombinerade insikter och råd
    st.subheader("💡 Integrerade Insikter")
    st.info("""
    Som hybrid-coach kombinerar jag personlig utveckling med AI-expertis. 
    Jag kan hjälpa dig utveckla ledarskapsförmågor för AI-transformation, 
    hantera stress vid förändring, och balansera innovation med ansvar.
    """)

def show_api_usage_interface():
    """Visa API-användning och kostnader"""
    st.header("💳 API Användning & Kostnader")
    
    # Hämta användningssammanfattning
    summary = usage_tracker.get_usage_summary()
    
    # Dagens användning
    st.subheader("📅 Idag")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Requests", summary['today']['total_requests'])
    with col2:
        st.metric("Tokens", f"{summary['today']['total_tokens']:,}")
    with col3:
        st.metric("Kostnad (USD)", f"${summary['today']['total_cost_usd']:.3f}")
    with col4:
        st.metric("Kostnad (SEK)", f"{summary['today']['total_cost_sek']:.2f} kr")
    
    # Månadens användning
    st.subheader("📊 Denna Månad")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Totala Requests", summary['month']['total_requests'])
    with col2:
        st.metric("Total Kostnad (USD)", f"${summary['month']['total_cost_usd']:.2f}")
    with col3:
        st.metric("Snitt per Request", f"${summary['month']['average_cost_per_request']:.4f}")
    
    # Rekommendationer
    st.subheader("💡 Rekommendationer")
    for rec in summary['recommendations']:
        if rec.startswith("🚨"):
            st.error(rec)
        elif rec.startswith("💰"):
            st.warning(rec)
        elif rec.startswith("📊"):
            st.info(rec)
        else:
            st.success(rec)
    
    # Användning per läge
    if summary['today']['by_mode']:
        st.subheader("📈 Användning per Coaching-läge (Idag)")
        for mode, count in summary['today']['by_mode'].items():
            st.write(f"**{mode.title()}**: {count} requests")
    
    # Detaljerad information
    with st.expander("🔍 Detaljerad Information"):
        st.write("**OpenAI Pricing (per 1000 tokens):**")
        st.write("- GPT-4: $0.03 input, $0.06 output")
        st.write("- GPT-4 Turbo: $0.01 input, $0.03 output")
        
        st.write("**Tips för att spara kostnader:**")
        st.write("- Använd kortare meddelanden")
        st.write("- Undvik upprepade frågor")
        st.write("- Sätt mål och reflektion istället för bara chat")
        
    # Export-funktion
    if st.button("📤 Exportera användningsdata"):
        export_data = usage_tracker.export_usage_data()
        st.download_button(
            label="💾 Ladda ner användningsdata (JSON)",
            data=json.dumps(export_data, indent=2, ensure_ascii=False),
            file_name=f"ai_coach_usage_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

def show_coaching_start():
    """Visa coaching-startskärm"""
    st.header("🚀 Starta din Coaching-resa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Personlig Coach")
        st.markdown("""
        **Utveckla dig själv med AI-hjälp:**
        - Sätt och följ upp personliga mål
        - Få motiverande coaching och feedback
        - Reflektion och progress tracking  
        - Anpassad utvecklingsplan
        """)
        
        if st.button("Starta Personlig Coaching", type="primary", key="personal_start"):
            st.session_state.current_mode = CoachingMode.PERSONAL
            user_id = "user_1"
            session_id = st.session_state.ai_coach.start_session(user_id, CoachingMode.PERSONAL)
            st.session_state.session_started = True
            st.session_state.session_id = session_id
            st.rerun()
    
    with col2:
        st.subheader("🎓 Universitets AI-Coach")
        st.markdown("""
        **Implementera AI på ditt universitet:**
        - Strategisk planering för AI-adoption
        - Forskningsintegration och metodologi
        - Stakeholder management och training
        - Etiska riktlinjer och compliance
        """)
        
        if st.button("Starta Universitets-Coaching", type="primary", key="university_start"):
            st.session_state.current_mode = CoachingMode.UNIVERSITY
            user_id = "user_1"  
            session_id = st.session_state.ai_coach.start_session(user_id, CoachingMode.UNIVERSITY)
            st.session_state.session_started = True
            st.session_state.session_id = session_id
            st.rerun()

def show_blog_interface():
    """Visa blog-gränssnitt"""
    st.header("📰 AI-Coaching Blog")
    
    # Admin-läge för att skapa inlägg (enkel löning)
    admin_mode = st.sidebar.checkbox("🔧 Admin-läge", help="Aktivera för att skapa och redigera blogginlägg")
    
    if admin_mode:
        show_blog_admin()
    else:
        show_blog_public()

def show_blog_admin():
    """Visa admin-gränssnitt för blog"""
    st.subheader("🔧 Blog Administration")
    
    admin_tabs = st.tabs(["📝 Skapa Inlägg", "📋 Hantera Inlägg"])
    
    with admin_tabs[0]:
        st.subheader("Skapa nytt blogginlägg")
        
        with st.form("create_blog_post"):
            title = st.text_input("Titel", placeholder="Hur AI kan transformera din coaching-resa")
            
            category = st.selectbox("Kategori", [
                "coaching", "ai-tips", "personlig-utveckling", 
                "universitet", "teknologi", "framtid"
            ])
            
            tags_input = st.text_input("Taggar (kommaseparerade)", 
                                     placeholder="AI, coaching, personlig utveckling")
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            
            excerpt = st.text_area("Sammanfattning (valfritt)", 
                                 placeholder="En kort beskrivning av inlägget...")
            
            content = st.text_area("Innehåll", height=300,
                                 placeholder="Skriv ditt blogginlägg här...")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                published = st.checkbox("Publicera direkt")
            with col2:
                featured = st.checkbox("Utvalt inlägg")
            with col3:
                ai_assist = st.checkbox("🤖 AI-assistance")
            
            if st.form_submit_button("📝 Skapa Inlägg"):
                if title and content:
                    # AI-assistance för innehåll
                    if ai_assist and content:
                        with st.spinner("🤖 Förbättrar innehåll med AI..."):
                            try:
                                enhanced_content = enhance_blog_content_with_ai(content, title, category)
                                content = enhanced_content
                                st.success("✨ Innehåll förbättrat med AI!")
                            except Exception as e:
                                st.warning(f"AI-assistance misslyckades: {str(e)}")
                    
                    post_id = st.session_state.data_manager.create_blog_post(
                        title=title,
                        content=content,
                        category=category,
                        tags=tags,
                        published=published,
                        featured=featured,
                        excerpt=excerpt
                    )
                    
                    if post_id:
                        st.success(f"✅ Blogginlägg skapat! ID: {post_id}")
                        if published:
                            st.info("📢 Inlägget är nu live på bloggen!")
                    else:
                        st.error("❌ Fel vid skapande av blogginlägg")
                else:
                    st.error("⚠️ Titel och innehåll krävs")
    
    with admin_tabs[1]:
        st.subheader("Hantera befintliga inlägg")
        
        # Hämta alla inlägg (även opublicerade)
        all_posts = st.session_state.data_manager.get_blog_posts(published_only=False)
        
        if all_posts:
            for post in all_posts:
                with st.expander(f"{'📢' if post['published'] else '📝'} {post['title']}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Kategori:** {post['category']}")
                        # Hantera datetime för PostgreSQL
                        created_date = post['created_at']
                        if hasattr(created_date, 'strftime'):
                            date_str = created_date.strftime('%Y-%m-%d %H:%M')
                        else:
                            date_str = str(created_date)
                        st.write(f"**Skapad:** {date_str}")
                        if post.get('tags'):
                            st.write(f"**Taggar:** {', '.join(post['tags'])}")
                    
                    with col2:
                        st.write(f"**Status:** {'Publicerad' if post['published'] else 'Utkast'}")
                        st.write(f"**Utvald:** {'Ja' if post['featured'] else 'Nej'}")
                    
                    with col3:
                        if st.button(f"🗑️ Ta bort", key=f"delete_{post['id']}"):
                            if st.session_state.data_manager.delete_blog_post(post['id']):
                                st.success("Inlägg borttaget!")
                                st.rerun()
                        
                        # Toggle publish status
                        new_status = not post['published']
                        status_text = "Publicera" if not post['published'] else "Dölj"
                        if st.button(f"📢 {status_text}", key=f"toggle_{post['id']}"):
                            if st.session_state.data_manager.update_blog_post(post['id'], published=new_status):
                                st.success(f"Status ändrad till {'publicerad' if new_status else 'dold'}!")
                                st.rerun()
        else:
            st.info("📝 Inga blogginlägg skapade än")

def show_blog_public():
    """Visa publik blog-vy"""
    # Sök och filter
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("🔍 Sök i bloggen", placeholder="Sök efter nyckelord...")
    
    with col2:
        categories = st.session_state.data_manager.get_blog_categories()
        selected_category = st.selectbox("📂 Kategori", ["Alla"] + categories)
    
    # Hämta inlägg
    if search_term:
        posts = st.session_state.data_manager.search_blog_posts(search_term)
    else:
        category_filter = None if selected_category == "Alla" else selected_category
        posts = st.session_state.data_manager.get_blog_posts(
            published_only=True, 
            category=category_filter
        )
    
    # Visa utvalda inlägg först
    featured_posts = [p for p in posts if p.get('featured')]
    regular_posts = [p for p in posts if not p.get('featured')]
    
    if featured_posts:
        st.subheader("⭐ Utvalda Inlägg")
        for post in featured_posts[:2]:  # Visa max 2 utvalda
            show_blog_post_card(post, featured=True)
        
        st.markdown("---")
    
    if regular_posts:
        st.subheader("📰 Senaste Inlägg")
        for post in regular_posts:
            show_blog_post_card(post)
    
    if not posts:
        if search_term:
            st.info(f"🔍 Inga inlägg hittades för '{search_term}'")
        else:
            st.info("📝 Inga blogginlägg publicerade än")

def show_blog_post_card(post, featured=False):
    """Visa ett blogginlägg som kort"""
    # Styling för utvalda inlägg
    container = st.container()
    if featured:
        container.markdown("""
        <div style="padding: 1rem; border: 2px solid #ff6b6b; border-radius: 10px; margin-bottom: 1rem; background: linear-gradient(135deg, #ff6b6b10, #4ecdc410);">
        """, unsafe_allow_html=True)
    
    with container:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if featured:
                st.markdown(f"### ⭐ {post['title']}")
            else:
                st.markdown(f"### {post['title']}")
            
            # Excerpt eller förkortad content
            display_text = post.get('excerpt', '')
            if not display_text:
                display_text = post['content'][:200] + "..." if len(post['content']) > 200 else post['content']
            
            st.write(display_text)
            
            # Metadata
            col_meta1, col_meta2, col_meta3 = st.columns(3)
            with col_meta1:
                # Hantera datetime objekt från PostgreSQL
                created_date = post['created_at']
                if hasattr(created_date, 'strftime'):
                    date_str = created_date.strftime('%Y-%m-%d')
                else:
                    date_str = str(created_date)[:10]
                st.caption(f"📅 {date_str}")
            with col_meta2:
                st.caption(f"📂 {post['category']}")
            with col_meta3:
                if post.get('tags'):
                    st.caption(f"🏷️ {', '.join(post['tags'][:2])}")
        
        with col2:
            if st.button(f"📖 Läs mer", key=f"read_{post['id']}"):
                st.session_state.selected_blog_post = post
                st.rerun()
    
    if featured:
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Visa fullständigt inlägg om valt
    if st.session_state.get('selected_blog_post', {}).get('id') == post['id']:
        with st.expander("📖 Fullständigt inlägg", expanded=True):
            st.markdown(f"# {post['title']}")
            # Hantera datetime för PostgreSQL
            created_date = post['created_at']
            if hasattr(created_date, 'strftime'):
                date_str = created_date.strftime('%Y-%m-%d')
            else:
                date_str = str(created_date)
            st.caption(f"📅 {date_str} | 📂 {post['category']} | ✍️ {post['author']}")
            
            if post.get('tags'):
                tag_html = " ".join([f"<span style='background-color: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.8em;'>{tag}</span>" for tag in post['tags']])
                st.markdown(f"🏷️ {tag_html}", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown(post['content'])
            
            if st.button("❌ Stäng"):
                st.session_state.selected_blog_post = None
                st.rerun()

def enhance_blog_content_with_ai(content, title, category):
    """Förbättra blogginlägg med AI"""
    try:
        ai_coach = st.session_state.ai_coach
        
        prompt = f"""
        Som en expert på AI-coaching och personlig utveckling, förbättra följande blogginlägg:
        
        Titel: {title}
        Kategori: {category}
        Ursprungligt innehåll: {content}
        
        Förbättra innehållet genom att:
        1. Göra det mer engagerande och läsbart
        2. Lägga till praktiska tips och exempel
        3. Strukturera med rubriker och punktlistor
        4. Använda emojis och coaching-språk
        5. Lägga till en inspirerande avslutning
        
        Behåll den ursprungliga tonen men gör det mer professionellt och värdefullt för läsaren.
        Skriv på svenska och använd markdown-formatering.
        """
        
        response, _ = ai_coach.get_response(prompt)
        return response
        
    except Exception as e:
        raise Exception(f"AI-enhancement misslyckades: {str(e)}")

if __name__ == "__main__":
    main()