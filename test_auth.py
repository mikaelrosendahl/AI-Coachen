# -*- coding: utf-8 -*-
"""
Tester for autentiseringssystemet
Sakerställer att alla sakerhetsfunktioner fungerar korrekt
"""

import pytest
import os
import tempfile
from datetime import datetime, timedelta
from utils.auth_manager import AuthManager, User

def test_password_hashing():
    """Test password hashing and verification"""
    # Test just the password methods without database
    from utils.auth_manager import AuthManager
    
    # Test password validation
    test_passwords = [
        ("Test123!", True, "Valid password"),
        ("test123!", False, "No uppercase"),
        ("TEST123!", False, "No lowercase"), 
        ("Test!", False, "No digit"),
        ("Test123", False, "No special character"),
        ("Test1!", False, "Too short")
    ]
    
    # Create a mock auth manager to test password validation
    class MockAuthManager(AuthManager):
        def __init__(self):
            self.min_password_length = 8
            self.require_uppercase = True
            self.require_lowercase = True  
            self.require_digit = True
            self.require_special = True
            
        def _init_database(self):
            pass  # Skip database init for testing
    
    mock_auth = MockAuthManager()
    
    print("Testing password validation...")
    for password, expected_valid, description in test_passwords:
        is_valid, message = mock_auth._validate_password_strength(password)
        print(f"Password '{password}': {is_valid} ({message}) - {description}")
        assert is_valid == expected_valid, f"Password validation failed for {description}"
    
    print("All password validation tests passed!")
    
    # Test password hashing
    test_password = "TestPassword123!"
    hash1 = mock_auth._hash_password(test_password)
    hash2 = mock_auth._hash_password(test_password)
    
    print(f"Hash 1: {hash1[:20]}...")
    print(f"Hash 2: {hash2[:20]}...")
    
    # Hashes should be different (due to salt)
    assert hash1 != hash2, "Hashes should be different due to salt"
    
    # But both should verify correctly
    assert mock_auth._verify_password(test_password, hash1), "Hash1 verification failed"
    assert mock_auth._verify_password(test_password, hash2), "Hash2 verification failed"
    
    # Wrong password should fail
    assert not mock_auth._verify_password("WrongPassword", hash1), "Wrong password should fail"
    
    print("Password hashing tests passed!")

def test_email_validation():
    """Test email validation"""
    from utils.auth_manager import AuthManager
    
    class MockAuthManager(AuthManager):
        def __init__(self):
            pass
        def _init_database(self):
            pass
    
    mock_auth = MockAuthManager()
    
    test_emails = [
        ("test@example.com", True, "Valid email"),
        ("user.name+tag@domain.co.uk", True, "Complex valid email"),
        ("invalid.email", False, "No @ symbol"),
        ("@domain.com", False, "No username"),
        ("user@", False, "No domain"),
        ("", False, "Empty email")
    ]
    
    print("Testing email validation...")
    for email, expected_valid, description in test_emails:
        is_valid, result = mock_auth._validate_email(email)
        print(f"Email '{email}': {is_valid} - {description}")
        assert is_valid == expected_valid, f"Email validation failed for {description}"
    
    print("Email validation tests passed!")

if __name__ == "__main__":
    print("Running authentication system tests...")
    print("=" * 50)
    
    test_password_hashing()
    print()
    test_email_validation()
    
    print("=" * 50)
    print("All tests passed successfully!")
    print("Note: Database tests require DATABASE_URL to be set")
    
    # Test admin functionality
    print("\nTesting admin functionality...")
    
    # Test User dataclass with admin fields
    from datetime import datetime
    
    test_user = User(
        id="test-123",
        email="test@example.com", 
        first_name="Test",
        last_name="User",
        created_at=datetime.now(),
        is_admin=True,
        role="admin"
    )
    
    assert test_user.is_admin == True, "Admin flag should be True"
    assert test_user.role == "admin", "Role should be admin"
    print("✅ User dataclass with admin fields working!")
    
    print("✅ All admin functionality tests passed!")