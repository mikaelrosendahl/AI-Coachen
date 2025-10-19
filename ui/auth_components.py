# -*- coding: utf-8 -*-
"""
UI-komponenter for autentisering
Hanterar inloggning och registrering i Streamlit
"""

import streamlit as st
from typing import Optional, Tuple
from utils.auth_manager import AuthManager, User
import os
import psycopg2

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
    st.subheader("Logga In")
    
    with st.form("login_form"):
        # Pre-fill email if coming from registration
        prefill_email = st.session_state.get('prefill_email', '')
        if prefill_email:
            st.info("Email ifylld från registrering - ange bara ditt lösenord")
            # Clear the prefill after using it
            del st.session_state.prefill_email
        
        email = st.text_input("Email", value=prefill_email, placeholder="din@email.com")
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
    st.subheader("Skapa Nytt Konto")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("Fornamn", placeholder="Anna")
        with col2:
            last_name = st.text_input("Efternamn", placeholder="Andersson")
        
        email = st.text_input("Email", placeholder="anna@exempel.se")
        password = st.text_input("Losenord", type="password", help="Minst 8 tecken, stor/liten bokstav, siffra och specialtecken")
        confirm_password = st.text_input("Bekrafta Losenord", type="password")
        
        # Check if this could be first admin registration
        auth_manager = get_auth_manager()
        show_admin_option = False
        
        if auth_manager:
            try:
                if auth_manager.use_sqlite:
                    import sqlite3
                    conn = sqlite3.connect(auth_manager.database_url.replace('sqlite:///', ''))
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
                    admin_count = cursor.fetchone()[0]
                    show_admin_option = (admin_count == 0)
                    conn.close()
                else:
                    with psycopg2.connect(auth_manager.database_url, sslmode='require') as conn:
                        with conn.cursor() as cur:
                            cur.execute("SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
                            admin_count = cur.fetchone()[0]
                            show_admin_option = (admin_count == 0)
            except:
                pass  # If we can't check, don't show admin option
        
        # Admin checkbox (only visible if no admin exists)
        is_admin_registration = False
        if show_admin_option:
            st.info("Ingen admin hittades. Du kan skapa det första admin-kontot.")
            is_admin_registration = st.checkbox("Skapa som Admin (webbplats- och bloggadministratör)")
        
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
            
            # Save email for potential prefill
            st.session_state.registration_email = email
            
            # Forsok registrera
            if is_admin_registration:
                st.session_state.was_admin_registration = True
                success, message, user_id = auth_manager.create_first_admin(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                if success:
                    message = f"Admin-konto skapat för {first_name} {last_name}"
            else:
                st.session_state.was_admin_registration = False
                success, message, user_id = auth_manager.register_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                if success:
                    message = f"Konto skapat för {first_name} {last_name}"
            
            return True, message, user_id
    
    return False, "", None

def render_auth_page():
    """Visa autentiseringssida med login/registrering"""
    st.title("AI-Coachen")
    st.markdown("Din personliga AI-coach för mål, reflektion och utveckling")
    
    # Tabs for login/registration
    tab1, tab2 = st.tabs(["Logga In", "Skapa Konto"])
    
    with tab1:
        login_attempted, login_message, session_token = render_login_form()
        
        if login_attempted:
            if session_token:
                # Get user info to personalize welcome message
                auth_manager = get_auth_manager()
                if auth_manager:
                    user = auth_manager.get_user_from_session(session_token)
                    if user and user.is_admin:
                        st.success(f"**Välkommen tillbaka, Admin {user.first_name}.** Du har nu tillgång till alla admin-funktioner.")
                    elif user:
                        st.success(f"**Välkommen tillbaka, {user.first_name}.** Din coaching-session kan nu börja.")
                    else:
                        st.success("**Inloggning lyckades.** Välkommen till AI-Coachen.")
                else:
                    st.success("**Inloggning lyckades.** Välkommen till AI-Coachen.")
                
                st.session_state.session_token = session_token
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(login_message)
    
    with tab2:
        reg_attempted, reg_message, user_id = render_registration_form()
        
        if reg_attempted:
            if user_id:
                # Determine if this was admin registration
                is_admin_reg = "admin" in reg_message.lower() or st.session_state.get('was_admin_registration', False)
                
                if is_admin_reg:
                    st.success("**Admin-konto skapat.** Du har nu full kontroll över AI-Coachen webbplats och blogg.")
                else:
                    st.success("**Ditt konto är nu skapat och redo att använda.**")
                
                # Offer direct login
                st.markdown("---")
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("Logga in direkt", type="primary", use_container_width=True):
                        # Switch to login tab and pre-fill email if available
                        if 'registration_email' in st.session_state:
                            st.session_state.prefill_email = st.session_state.registration_email
                        st.session_state.active_tab = 0
                        st.rerun()
                
                with col2:
                    if st.button("Stanna kvar här", use_container_width=True):
                        # Clear the success message by rerunning
                        st.rerun()
                        
            else:
                st.error(reg_message)

def render_user_menu(user: User):
    """Visa anvandarmeny"""
    with st.sidebar:
        st.markdown("### Användarprofil")
        st.markdown(f"**Namn:** {user.first_name} {user.last_name}")
        st.markdown(f"**Email:** {user.email}")
        st.markdown(f"**Medlemskap:** {user.subscription_tier.title()}")
        
        # Show admin badge if user is admin
        if user.is_admin:
            st.markdown("---")
            st.success("**ADMINISTRATÖR**")
            st.markdown(f"**Admin-roll:** {user.role.title()}")
            st.markdown("*Fullständiga systemrättigheter*")
        else:
            st.markdown(f"**Roll:** {user.role.title()}")
        
        # Admin functions
        if user.is_admin:
            st.markdown("---")
            st.markdown("### Admin-funktioner")
            
            col_admin1, col_admin2 = st.columns(2)
            
            with col_admin1:
                if st.button("Hantera Blogg", use_container_width=True):
                    st.session_state.show_admin_blog = True
            
            with col_admin2:
                if st.button("Hantera Användare", use_container_width=True):
                    st.session_state.show_admin_users = True
            
            if st.button("Admin Dashboard", use_container_width=True):
                st.session_state.show_admin_dashboard = True
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Inställningar", use_container_width=True):
                st.session_state.show_settings = True
        
        with col2:
            if st.button("Logga Ut", use_container_width=True):
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
    st.subheader("Användarinställningar")
    
    # Profile information
    with st.expander("Profilinformation", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Fornamn", value=user.first_name, disabled=True)
            st.text_input("Email", value=user.email, disabled=True)
        
        with col2:
            st.text_input("Efternamn", value=user.last_name, disabled=True)
            st.text_input("Medlemskap", value=user.subscription_tier.title(), disabled=True)
    
    # Account security
    with st.expander("Kontosäkerhet"):
        st.info("Ändring av lösenord och säkerhetsinställningar kommer snart!")
        
        if st.button("Ändra Lösenord"):
            st.info("Lösenordsändring är inte implementerad ännu")
    
    # Privacy settings
    with st.expander("Integritetsinställningar"):
        st.info("GDPR-kompatibla integritetsinställningar kommer snart!")
        
        if st.button("Exportera Mina Data"):
            st.info("Dataexport är inte implementerad ännu")
        
        if st.button("Radera Mitt Konto"):
            st.warning("Kontoradering är inte implementerad ännu")
    
    if st.button("Tillbaka"):
        st.session_state.show_settings = False
        st.rerun()

def render_admin_dashboard(user: User):
    """Visa admin dashboard (endast for admins)"""
    if not user.is_admin:
        st.error("Endast admins har tillgång till denna sida")
        return
    
    st.title("Admin Dashboard")
    st.markdown(f"Inloggad som: **{user.first_name} {user.last_name}** ({user.role})")
    
    # Admin statistics
    auth_manager = get_auth_manager()
    if auth_manager:
        try:
            if auth_manager.use_sqlite:
                import sqlite3
                conn = sqlite3.connect(auth_manager.database_url.replace('sqlite:///', ''))
                cursor = conn.cursor()
                # User statistics
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
                total_admins = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM users WHERE created_at > datetime('now', '-7 days')")
                new_users_week = cursor.fetchone()[0]
                conn.close()
            else:
                with psycopg2.connect(auth_manager.database_url, sslmode='require') as conn:
                    with conn.cursor() as cur:
                        # User statistics
                        cur.execute("SELECT COUNT(*) FROM users")
                        total_users = cur.fetchone()[0]
                        
                        cur.execute("SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
                        total_admins = cur.fetchone()[0]
                        
                        cur.execute("SELECT COUNT(*) FROM users WHERE created_at > NOW() - INTERVAL '7 days'")
                        new_users_week = cur.fetchone()[0]
                    
                    # Display statistics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Totalt Användare", total_users)
                    
                    with col2:
                        st.metric("Admins", total_admins)
                    
                    with col3:
                        st.metric("Nya (7 dagar)", new_users_week)
                    
        except Exception as e:
            st.error(f"Fel vid hamtning av statistik: {e}")
    
    # Admin actions
    st.markdown("---")
    st.subheader("Admin-verktyg")
    
    tab1, tab2, tab3 = st.tabs(["Användarhantering", "Blogghantering", "Statistik"])
    
    with tab1:
        render_user_management(user)
    
    with tab2:
        st.info("Blogghantering kommer snart!")
        st.markdown("Har kommer du kunna:")
        st.markdown("- Skapa och redigera blogginlagg")
        st.markdown("- Hantera kategorier") 
        st.markdown("- Moderera kommentarer")
        st.markdown("- Schemalägga publicering")
    
    with tab3:
        st.info("Avancerad statistik kommer snart!")
        st.markdown("Har kommer du kunna se:")
        st.markdown("- Anvandningsstatistik")
        st.markdown("- Performance metrics")
        st.markdown("- Sakerhetshändelser")
        st.markdown("- Systemhälsa")
    
    if st.button("Tillbaka till Huvudmeny"):
        st.session_state.show_admin_dashboard = False
        st.rerun()

def render_user_management(admin_user: User):
    """Visa användarhantering (endast for admins)"""
    if not admin_user.is_admin:
        st.error("⚠️ Endast admins har tillgang")
        return
    
    st.subheader("Användarhantering")
    
    # Promote user to admin
    with st.expander("Förfram Användare till Admin"):
        email_to_promote = st.text_input("Email att forframa:")
        role_to_assign = st.selectbox("Roll:", ["admin", "moderator", "editor"])
        
        if st.button("Forfram till Admin"):
            if email_to_promote:
                auth_manager = get_auth_manager()
                if auth_manager:
                    success, message = auth_manager.promote_to_admin(email_to_promote, role_to_assign)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    # List all users (for admin overview)
    with st.expander("Alla Användare"):
        auth_manager = get_auth_manager()
        if auth_manager:
            try:
                if auth_manager.use_sqlite:
                    import sqlite3
                    conn = sqlite3.connect(auth_manager.database_url.replace('sqlite:///', ''))
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT email, first_name, last_name, is_admin, role, created_at, last_login
                        FROM users 
                        ORDER BY created_at DESC
                        LIMIT 20
                    """)
                    users = cursor.fetchall()
                    conn.close()
                    
                    if users:
                        st.markdown("**Senaste användarna:**")
                        for user in users:
                            email, fname, lname, is_admin, role, created, last_login = user
                            admin_badge = "[Admin]" if is_admin else "[User]"
                            last_login_str = last_login[:10] if last_login else "Aldrig"  # SQLite timestamp format
                            created_str = created[:10] if created else "Okänt"
                            st.markdown(f"{admin_badge} **{fname} {lname}** ({email}) - {role} - Skapad: {created_str} - Senast in: {last_login_str}")
                    else:
                        st.info("Inga användare hittades")
                else:
                    with psycopg2.connect(auth_manager.database_url, sslmode='require') as conn:
                        with conn.cursor() as cur:
                            cur.execute("""
                                SELECT email, first_name, last_name, is_admin, role, created_at, last_login
                                FROM users 
                                ORDER BY created_at DESC
                                LIMIT 20
                            """)
                            users = cur.fetchall()
                            
                            if users:
                                st.markdown("**Senaste användarna:**")
                                for user in users:
                                    email, fname, lname, is_admin, role, created, last_login = user
                                    admin_badge = "[Admin]" if is_admin else "[User]"
                                    last_login_str = last_login.strftime("%Y-%m-%d") if last_login else "Aldrig"
                                    st.markdown(f"{admin_badge} **{fname} {lname}** ({email}) - {role} - Skapad: {created.strftime('%Y-%m-%d')} - Senast in: {last_login_str}")
                            else:
                                st.info("Inga användare hittades")
                            
            except Exception as e:
                st.error(f"Fel vid hamtning av användare: {e}")