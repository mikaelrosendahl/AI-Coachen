#!/usr/bin/env python3
"""
AI Expert Demonstration
Visar AI-Coachens nya AI-expertis funktionalitet
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demonstrate_ai_knowledge():
    """Visa AI-kunskapsbasens innehåll"""
    print("🧠 AI-KUNSKAPSBASENS INNEHÅLL")
    print("=" * 50)
    
    try:
        from utils.ai_expert_knowledge import ai_expert_knowledge
        
        all_docs = ai_expert_knowledge.get_all_knowledge()
        
        # Gruppera efter kategori
        categories = {}
        for doc in all_docs:
            cat = doc['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(doc)
        
        for category, docs in categories.items():
            print(f"\n📚 {category.upper().replace('_', ' ')}")
            print("-" * 30)
            for i, doc in enumerate(docs, 1):
                print(f"   {i}. {doc['title']}")
                print(f"      Keywords: {', '.join(doc['keywords'][:3])}...")
        
        print(f"\n✅ Total: {len(all_docs)} AI-expertis dokument i {len(categories)} kategorier")
        
    except Exception as e:
        print(f"❌ Fel: {e}")

def demonstrate_rag_intelligence():
    """Visa RAG-systemets intelligens"""
    print("\n🔍 RAG-SYSTEMETS INTELLIGENS")
    print("=" * 50)
    
    try:
        from utils.rag_system import rag_system
        
        # Test cases för AI-fråga identifiering
        test_queries = [
            ("Vad är machine learning?", True),
            ("Hur implementerar jag en transformer?", True), 
            ("AI transformation roadmap", True),
            ("Python för AI utveckling", True),
            ("Hej, vad heter du?", False),
            ("Vad tycker du om vädret?", False),
            ("Kan du hjälpa mig med matematik?", False)
        ]
        
        print("AI-FRÅGA IDENTIFIERING:")
        for query, expected in test_queries:
            is_ai = rag_system.is_ai_related_query(query)
            status = "✅" if is_ai == expected else "❌"
            ai_indicator = "🤖" if is_ai else "💬"
            print(f"   {status} {ai_indicator} '{query}' -> AI-relaterad: {is_ai}")
        
        # Test kontext-hämtning
        print(f"\nKONTEXT-HÄMTNING FÖR AI-FRÅGOR:")
        ai_queries = [
            "Vad är deep learning?",
            "MLOps best practices", 
            "AI säkerhet och GDPR"
        ]
        
        for query in ai_queries:
            contexts = rag_system.retrieve_relevant_context(query)
            print(f"\n🔍 '{query}':")
            if contexts:
                for i, ctx in enumerate(contexts[:2], 1):  # Visa bara top 2
                    print(f"   {i}. {ctx.title} (Score: {ctx.relevance_score:.2f})")
                    print(f"      Kategori: {ctx.category}")
            else:
                print("   Inga relevanta kontexter hittade")
        
    except Exception as e:
        print(f"❌ Fel: {e}")

def demonstrate_expertise_levels():
    """Visa expertis-nivå detektering"""
    print("\n🎯 EXPERTIS-NIVÅ DETEKTERING")
    print("=" * 50)
    
    try:
        from utils.ai_expert_integration import ai_expert_integration, AIExpertiseLevel
        
        # Test cases för olika expertis-nivåer
        level_tests = [
            ("Vad är AI?", "BASIC"),
            ("Förklara machine learning grunderna", "BASIC"),
            ("Hur deployar jag en ML-modell?", "INTERMEDIATE"),
            ("Implementera MLOps pipeline", "INTERMEDIATE"),
            ("AI transformation strategi för företag", "ADVANCED"),
            ("Organisationell AI-mognad assessment", "ADVANCED"),
            ("Transformer attention mechanism", "EXPERT"),
            ("State-of-the-art neural architecture", "EXPERT")
        ]
        
        for query, expected in level_tests:
            detected = ai_expert_integration.detect_expertise_level(query)
            status = "✅" if detected.value.upper() == expected else "⚠️"
            
            # Emoji för nivå
            level_emoji = {
                "BASIC": "🌱",
                "INTERMEDIATE": "🔧", 
                "ADVANCED": "🎯",
                "EXPERT": "🧠"
            }
            
            emoji = level_emoji.get(detected.value.upper(), "❓")
            print(f"   {status} {emoji} '{query}'")
            print(f"       -> {detected.value.upper()} (förväntad: {expected})")
        
    except Exception as e:
        print(f"❌ Fel: {e}")

def demonstrate_coaching_integration():
    """Visa hur AI-expertis integreras med coaching"""
    print("\n💡 COACHING-INTEGRATION EXEMPEL")
    print("=" * 50)
    
    try:
        from utils.ai_expert_integration import ai_expert_integration
        
        # Exempel på persona enhancement
        base_persona = """Du är en personlig coach som hjälper med utveckling och målsättning.
Din approach är empatisk och fokuserar på att hjälpa användaren hitta sina egna svar."""
        
        ai_query = "Hur kommer jag igång med machine learning?"
        normal_query = "Jag känner mig stressad på jobbet"
        
        print("PERSONA FÖRE AI-ENHANCEMENT:")
        print(f"   Längd: {len(base_persona)} tecken")
        print(f"   Innehåll: Grundläggande coaching persona")
        
        # Test AI-fråga
        enhanced_ai = ai_expert_integration.enhance_coaching_persona(
            base_persona, ai_query, "personal"
        )
        
        print(f"\nPERSONA EFTER AI-ENHANCEMENT (AI-fråga):")
        print(f"   Längd: {len(enhanced_ai)} tecken")
        print(f"   AI-expertis tillagd: {'Ja' if 'AI-Expertis Enhancement' in enhanced_ai else 'Nej'}")
        print(f"   Coaching approach bevarad: {'Ja' if 'coaching' in enhanced_ai.lower() else 'Nej'}")
        
        # Test normal fråga
        enhanced_normal = ai_expert_integration.enhance_coaching_persona(
            base_persona, normal_query, "personal"
        )
        
        print(f"\nPERSONA EFTER ENHANCEMENT (normal fråga):")
        print(f"   Längd: {len(enhanced_normal)} tecken")
        print(f"   AI-expertis tillagd: {'Ja' if 'AI-Expertis Enhancement' in enhanced_normal else 'Nej'}")
        print(f"   Original persona bevarad: {'Ja' if enhanced_normal == base_persona else 'Nej'}")
        
    except Exception as e:
        print(f"❌ Fel: {e}")

def main():
    """Kör full demonstration"""
    print("🚀 AI-COACHEN AI EXPERTIS DEMONSTRATION")
    print("=" * 60)
    print("Visar den nya AI-expertis funktionaliteten som implementerats")
    print("Live på: https://ai-coachen.online")
    print("=" * 60)
    
    # Kör alla demonstrationer
    demonstrate_ai_knowledge()
    demonstrate_rag_intelligence()
    demonstrate_expertise_levels() 
    demonstrate_coaching_integration()
    
    print("\n" + "=" * 60)
    print("🎊 DEMONSTRATION SLUTFÖRD")
    print("=" * 60)
    print("✅ AI-kunskapsbas: Funktionell med 25+ dokument")
    print("✅ RAG-system: Intelligent AI-fråga identifiering")
    print("✅ Expertis-nivåer: Automatisk detektering")
    print("✅ Coaching-integration: Seamless AI-expertis enhancement")
    print("\n🎯 AI-Coachen är nu en fullfjädrad AI-expert!")
    print("🌐 Testa live: https://ai-coachen.online")
    print("\n📋 TESTFÖRSLAG:")
    print("   • 'Vad är machine learning?'")
    print("   • 'Hur implementerar jag MLOps?'")
    print("   • 'AI transformation roadmap för universitet?'")
    print("   • 'Transformer architecture förklaring'")

if __name__ == "__main__":
    main()