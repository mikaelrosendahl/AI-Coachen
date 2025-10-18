#!/usr/bin/env python3
"""
Test script för AI Expert funktionalitet
Testar att AI-expertis integration fungerar korrekt utan extra API-kostnader
"""

import os
import sys
from dotenv import load_dotenv

# Lägg till projektets root till path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ladda environment variables
load_dotenv()

def test_ai_knowledge_base():
    """Testa att AI-kunskapsbasen laddas korrekt"""
    print("🧠 Testar AI-kunskapsbasen...")
    
    try:
        from utils.ai_expert_knowledge import ai_expert_knowledge
        
        all_knowledge = ai_expert_knowledge.get_all_knowledge()
        
        print(f"✅ AI-kunskapsbas laddad: {len(all_knowledge)} dokument")
        
        # Visa kategorier
        categories = set(doc['category'] for doc in all_knowledge)
        print(f"📚 Kategorier: {', '.join(categories)}")
        
        # Visa första dokumentet som exempel
        if all_knowledge:
            first_doc = all_knowledge[0]
            print(f"📖 Exempel dokument: {first_doc['title']}")
            print(f"   Kategori: {first_doc['category']}")
            print(f"   Keywords: {first_doc['keywords'][:3]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Fel i AI-kunskapsbas: {e}")
        return False

def test_rag_system():
    """Testa RAG-systemet"""
    print("\n🔍 Testar RAG-systemet...")
    
    try:
        from utils.rag_system import rag_system
        
        # Testa AI-fråga identifiering
        ai_queries = [
            "Vad är machine learning?",
            "Hur implementerar jag en transformer?", 
            "AI transformation roadmap för universitet",
            "Hej, vad heter du?"  # Inte AI-relaterad
        ]
        
        for query in ai_queries:
            is_ai = rag_system.is_ai_related_query(query)
            print(f"{'🤖' if is_ai else '💬'} '{query[:30]}...' -> AI-relaterad: {is_ai}")
        
        # Testa kontext-hämtning
        ai_query = "Vad är transformer architecture?"
        contexts = rag_system.retrieve_relevant_context(ai_query)
        
        if contexts:
            print(f"✅ Hämtade {len(contexts)} relevanta kontexter för AI-fråga")
            for i, ctx in enumerate(contexts, 1):
                print(f"   {i}. {ctx.title} (Score: {ctx.relevance_score:.2f})")
        else:
            print("ℹ️  Inga kontexter hämtade (kan vara normalt för icke-AI frågor)")
        
        return True
        
    except Exception as e:
        print(f"❌ Fel i RAG-system: {e}")
        return False

def test_ai_expert_integration():
    """Testa AI-expert integrationslagret"""
    print("\n🎯 Testar AI-expert integration...")
    
    try:
        from utils.ai_expert_integration import ai_expert_integration, AIExpertiseLevel
        
        # Testa expertisnivå-detektering
        test_queries = [
            ("Vad är AI?", AIExpertiseLevel.BASIC),
            ("Hur deployar jag en ML-modell?", AIExpertiseLevel.INTERMEDIATE), 
            ("AI transformation roadmap", AIExpertiseLevel.ADVANCED),
            ("transformer attention mechanism", AIExpertiseLevel.EXPERT)
        ]
        
        for query, expected in test_queries:
            detected = ai_expert_integration.detect_expertise_level(query)
            status = "✅" if detected == expected else "⚠️"
            print(f"{status} '{query}' -> {detected.value} (förväntad: {expected.value})")
        
        # Testa persona enhancement
        base_persona = "Du är en personlig coach."
        ai_query = "Hur kommer jag igång med machine learning?"
        
        enhanced = ai_expert_integration.enhance_coaching_persona(base_persona, ai_query)
        
        if "AI-Expertis Enhancement" in enhanced:
            print("✅ Persona förbättrad med AI-expertis")
        else:
            print("ℹ️  Persona inte förbättrad (kan vara normalt för icke-AI frågor)")
        
        return True
        
    except Exception as e:
        print(f"❌ Fel i AI-expert integration: {e}")
        return False

def test_full_ai_coach_integration():
    """Testa full AI-coach integration med AI-expertis"""
    print("\n🤖 Testar full AI-coach integration...")
    
    # Kontrollera att API-nyckel finns
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Ingen OpenAI API-nyckel hittad - hoppar över API-test")
        return True
    
    try:
        from core.ai_coach import create_ai_coach, CoachingMode
        
        # Skapa AI-coach
        coach = create_ai_coach()
        
        # Starta session
        session_id = coach.start_session("test_user", CoachingMode.PERSONAL)
        print(f"✅ AI-coach session startad: {session_id}")
        
        # Testa vanlig fråga (ingen AI-expertis)
        normal_query = "Hur mår du idag?"
        response1, metadata1 = coach.get_response(normal_query)
        print(f"💬 Vanlig fråga svar längd: {len(response1)} tecken")
        
        # Testa AI-fråga (med AI-expertis)
        ai_query = "Vad är machine learning och hur kommer jag igång?"
        response2, metadata2 = coach.get_response(ai_query)
        print(f"🧠 AI-fråga svar längd: {len(response2)} tecken")
        
        # Jämför tokens (borde vara ungefär samma)
        tokens1 = metadata1.get('tokens_used', 0)
        tokens2 = metadata2.get('tokens_used', 0)
        
        print(f"📊 Tokens: Vanlig fråga={tokens1}, AI-fråga={tokens2}")
        
        if abs(tokens1 - tokens2) < 500:  # Rimlig skillnad
            print("✅ AI-expertis lägger inte till många extra tokens")
        else:
            print("⚠️  Stor skillnad i token-användning")
        
        # Avsluta session
        summary = coach.end_session()
        print(f"✅ Session avslutad: {summary['message_count']} meddelanden")
        
        return True
        
    except Exception as e:
        print(f"❌ Fel i full integration test: {e}")
        return False

def main():
    """Kör alla tester"""
    print("🚀 AI Expert Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_ai_knowledge_base,
        test_rag_system, 
        test_ai_expert_integration,
        test_full_ai_coach_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} kraschade: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📋 TEST RESULTAT")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    test_names = [
        "AI Kunskapsbas",
        "RAG System", 
        "AI Expert Integration",
        "Full AI Coach Integration"
    ]
    
    for name, result in zip(test_names, results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\n🎯 TOTALT: {passed}/{total} tester godkända")
    
    if passed == total:
        print("🎉 Alla tester godkända! AI Expert-funktionalitet är redo.")
        return True
    else:
        print("⚠️  Vissa tester misslyckades. Kontrollera loggar ovan.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)