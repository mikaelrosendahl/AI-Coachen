# -*- coding: utf-8 -*-
"""
UI-komponenter for autentisering
Hanterar inloggning och registrering i Streamlit
"""

import streamlit as st
from typing import Optional, Tuple
from utils.auth_manager import AuthManager, User
import os

# Create auth manager instance if DATABASE_URL is available
def get_auth_manager():
    """Get AuthManager instance with proper error handling"""
    try:
        return AuthManager()
    except ValueError as e:
        st.error(f"Database configuration error: {e}")
        return None

def render_login_form() -> Tuple[bool, str, Optional[str]]:
    """
    Visa inloggningsformular
    Returns: (login_attempted, message, session_token)
    """
    st.subheader("🔐 Logga In")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="din@email.com")
        password = st.text_input("Losenord", type="password")
        submit_button = st.form_submit_button("Logga In", type="primary")
        
        if submit_button:
            if not email or not password:
                return True, "Email och losenord kravs", None
            
            # Get auth manager
            auth_manager = get_auth_manager()
            if not auth_manager:
                return True, "Database not available", None
            
            # Forsok logga in
            success, message, session_token = auth_manager.login_user(
                email=email,
                password=password,
                ip_address=st.session_state.get('client_ip', 'unknown')
            )
            
            return True, message, session_token
    
    return False, "", None

def render_registration_form() -> Tuple[bool, str, Optional[str]]:
    """
    Visa registreringsformular
    Returns: (registration_attempted, message, user_id)
    """
    st.subheader("✨ Skapa Nytt Konto")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("Fornamn", placeholder="Anna")
        with col2:
            last_name = st.text_input("Efternamn", placeholder="Andersson")
        
        email = st.text_input("Email", placeholder="anna@exempel.se")
        password = st.text_input("Losenord", type="password", help="Minst 8 tecken, stor/liten bokstav, siffra och specialtecken")
        confirm_password = st.text_input("Bekrafta Losenord", type="password")
        
        terms_accepted = st.checkbox("Jag accepterar användarvillkoren")
        
        submit_button = st.form_submit_button("Skapa Konto", type="primary")
        
        if submit_button:
            if not all([first_name, last_name, email, password, confirm_password]):
                return True, "Alla falt maste fyllas i", None
            
            if password != confirm_password:
                return True, "Losenorden matchar inte", None
            
            if not terms_accepted:
                return True, "Du maste acceptera användarvillkoren", None
            
            # Get auth manager
            auth_manager = get_auth_manager()
            if not auth_manager:
                return True, "Database not available", None
            
            # Forsok registrera
            success, message, user_id = auth_manager.register_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            return True, message, user_id
    
    return False, "", None

def render_auth_page():
    """Visa autentiseringssida med login/registrering"""
    st.title("🎯 AI-Coachen")
    st.markdown("Din personliga AI-coach for mal, reflektion och utveckling")
    
    # Tabs for login/registration
    tab1, tab2 = st.tabs(["Logga In", "Skapa Konto"])
    
    with tab1:
        login_attempted, login_message, session_token = render_login_form()
        
        if login_attempted:
            if session_token:
                st.success(login_message)
                st.session_state.session_token = session_token
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(login_message)
    
    with tab2:
        reg_attempted, reg_message, user_id = render_registration_form()
        
        if reg_attempted:
            if user_id:
                st.success(f"{reg_message} Nu kan du logga in!")
                # Switch to login tab automatically
                st.session_state.active_tab = 0
                st.rerun()
            else:
                st.error(reg_message)

def render_user_menu(user: User):
    """Visa anvandarmeny"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"### 👤 {user.first_name} {user.last_name}")
        st.markdown(f"📧 {user.email}")
        st.markdown(f"⭐ {user.subscription_tier.title()}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⚙️ Installningar", use_container_width=True):
                st.session_state.show_settings = True
        
        with col2:
            if st.button("🚪 Logga Ut", use_container_width=True):
                if st.session_state.get('session_token'):
                    auth_manager = get_auth_manager()
                    if auth_manager:
                        auth_manager.logout_user(st.session_state.session_token)
                
                # Rensa session state
                for key in ['session_token', 'authenticated', 'current_user']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.rerun()

def check_authentication() -> Optional[User]:
    """Kontrollera om anvandare ar autentiserad"""
    # Kontrollera cached authentication
    if st.session_state.get('authenticated') and st.session_state.get('current_user'):
        return st.session_state.current_user
    
    # Kontrollera session token
    session_token = st.session_state.get('session_token')
    if not session_token:
        return None
    
    # Get auth manager
    auth_manager = get_auth_manager()
    if not auth_manager:
        return None
    
    # Hamta anvandare fran session
    user = auth_manager.get_user_from_session(session_token)
    if user:
        st.session_state.current_user = user
        st.session_state.authenticated = True
        return user
    else:
        # Session ogiltig - rensa
        st.session_state.authenticated = False
        if 'session_token' in st.session_state:
            del st.session_state['session_token']
        return None

def require_auth(func):
    """Decorator som kraver autentisering"""
    def wrapper(*args, **kwargs):
        user = check_authentication()
        if not user:
            render_auth_page()
            return None
        return func(user, *args, **kwargs)
    return wrapper

def render_user_settings(user: User):
    """Visa anvandarsettings"""
    st.subheader("⚙️ Anvandarsettings")
    
    # Profile information
    with st.expander("📝 Profilinformation", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Fornamn", value=user.first_name, disabled=True)
            st.text_input("Email", value=user.email, disabled=True)
        
        with col2:
            st.text_input("Efternamn", value=user.last_name, disabled=True)
            st.text_input("Medlemskap", value=user.subscription_tier.title(), disabled=True)
    
    # Account security
    with st.expander("🔒 Kontosakerhet"):
        st.info("Andring av losenord och sakerhetsinställningar kommer snart!")
        
        if st.button("🔄 Andra Losenord"):
            st.info("Losenordsandring ar inte implementerad annu")
    
    # Privacy settings
    with st.expander("🛡️ Integritetsinställningar"):
        st.info("GDPR-kompatibla integritetsinställningar kommer snart!")
        
        if st.button("📄 Exportera Mina Data"):
            st.info("Dataexport ar inte implementerad annu")
        
        if st.button("🗑️ Radera Mitt Konto"):
            st.warning("Kontoradering ar inte implementerad annu")
    
    if st.button("🔙 Tillbaka"):
        st.session_state.show_settings = False
        st.rerun()