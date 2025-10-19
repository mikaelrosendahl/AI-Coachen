import sys
sys.path.append('.')
from utils.auth_manager import AuthManager

def create_test_admin():
    print("=== Creating Fresh Admin User ===")
    auth = AuthManager()
    print('Database URL:', auth.database_url)
    print('Using SQLite:', auth.use_sqlite)
    
    # Create admin user
    print("\n--- Creating Admin User ---")
    success, msg, user_id = auth.register_user(
        'testadmin@test.com', 
        'TestAdmin123!', 
        'Test', 
        'Admin', 
        is_admin=True, 
        role='admin'
    )
    print(f'Admin registration: success={success}, message={msg}')
    
    if success:
        print(f'✅ Admin created! User ID: {user_id}')
        print('📧 Email: testadmin@test.com')
        print('🔑 Password: TestAdmin123!')
        
        # Test login immediately
        print("\n--- Testing Login ---")
        login_success, login_msg, token = auth.login_user('testadmin@test.com', 'TestAdmin123!')
        print(f'Login test: success={login_success}, message={login_msg}')
        
        if login_success and token:
            user = auth.get_user_from_session(token)
            if user:
                print(f'✅ Login successful! Admin: {user.is_admin}, Role: {user.role}')
            else:
                print('❌ Session validation failed')
        else:
            print('❌ Login failed')
    
    print("\n=== Test Complete ===")

try:
    create_test_admin()
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()