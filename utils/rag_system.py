"""
RAG System for AI Expert Integration
Retrieval-Augmented Generation system som integrerar AI-expertis utan extra API-kostnader
Använder lokala embeddings och intelligent kontext-sökning
"""

import json
import os
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass
import re

# Försök importera sentence-transformers, använd fallback om det inte finns
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers inte installerat - använder enkel text-matching som fallback")

from .ai_expert_knowledge import ai_expert_knowledge

@dataclass
class RetrievedContext:
    """Struktur för hämtat kontext från kunskapsbasen"""
    content: str
    category: str
    title: str
    relevance_score: float
    coaching_context: str

class SimpleRAGSystem:
    """Enkel RAG-implementation som fungerar utan externa beroenden"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.knowledge_docs = ai_expert_knowledge.get_all_knowledge()
        
        # AI-relaterade keywords för att identifiera AI-frågor
        self.ai_keywords = {
            'grundlaggande': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'neural network', 'algoritm'],
            'modeller': ['gpt', 'transformer', 'bert', 'llm', 'language model', 'generativ', 'diffusion'],
            'teknisk': ['python', 'tensorflow', 'pytorch', 'api', 'deployment', 'mlops', 'cloud'],
            'affar': ['roi', 'business case', 'transformation', 'strategi', 'implementation', 'pilot'],
            'sakerhet': ['gdpr', 'bias', 'ethical', 'security', 'privacy', 'compliance'],
            'universitet': ['forskn', 'academ', 'student', 'learning analytics', 'universitet', 'högskola']
        }
        
        self.logger.info(f"RAG System initialiserad med {len(self.knowledge_docs)} kunskapsdokument")
    
    def is_ai_related_query(self, query: str) -> bool:
        """Kontrollera om frågan är AI-relaterad"""
        query_lower = query.lower()
        
        # Kolla efter AI-keywords
        for category, keywords in self.ai_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return True
        
        # Kolla efter explicita AI-frågor
        ai_patterns = [
            r'\bai\b', r'artificial intelligence', r'machine learning', r'deep learning',
            r'neural network', r'algoritm', r'modell', r'träning', r'deployment'
        ]
        
        for pattern in ai_patterns:
            if re.search(pattern, query_lower):
                return True
        
        return False
    
    def simple_text_similarity(self, query: str, document: str) -> float:
        """Enkel textlikhet baserad på gemensamma ord"""
        query_words = set(query.lower().split())
        doc_words = set(document.lower().split())
        
        if len(doc_words) == 0:
            return 0.0
        
        # Jaccard similarity
        intersection = len(query_words & doc_words)
        union = len(query_words | doc_words)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> List[RetrievedContext]:
        """Hämta relevant kontext för en fråga"""
        
        # Kontrollera om det är en AI-relaterad fråga
        if not self.is_ai_related_query(query):
            return []
        
        scored_docs = []
        
        for doc in self.knowledge_docs:
            # Beräkna relevance score
            content_score = self.simple_text_similarity(query, doc['content'])
            title_score = self.simple_text_similarity(query, doc['title']) * 2  # Viktning för titel
            keyword_score = 0
            
            # Bonus för matchande keywords
            for keyword in doc['keywords']:
                if keyword.lower() in query.lower():
                    keyword_score += 0.3
            
            total_score = content_score + title_score + keyword_score
            
            if total_score > 0.1:  # Threshold för relevans
                scored_docs.append((doc, total_score))
        
        # Sortera efter score och ta top_k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for doc, score in scored_docs[:top_k]:
            context = RetrievedContext(
                content=doc['content'],
                category=doc['category'],
                title=doc['title'],
                relevance_score=score,
                coaching_context=doc['coaching_context']
            )
            results.append(context)
        
        self.logger.info(f"Hämtade {len(results)} relevanta kontexter för AI-fråga")
        return results
    
    def enhance_prompt_with_context(self, original_prompt: str, user_query: str) -> str:
        """Förbättra prompt med relevant AI-expertis kontext"""
        
        relevant_contexts = self.retrieve_relevant_context(user_query)
        
        if not relevant_contexts:
            # Ingen AI-kontext behövs
            return original_prompt
        
        # Bygg AI-expertis kontext
        ai_context = "## AI-Expertis Kontext\n"
        ai_context += "Som AI-expert har du tillgång till följande relevanta kunskap:\n\n"
        
        for i, context in enumerate(relevant_contexts, 1):
            ai_context += f"### {i}. {context.title} (Kategori: {context.category})\n"
            ai_context += f"{context.content}\n\n"
            if context.coaching_context:
                ai_context += f"**Coaching-perspektiv**: {context.coaching_context}\n\n"
        
        # Integrera AI-kontext med coaching-persona
        enhanced_prompt = f"""{original_prompt}

{ai_context}

**Viktigt**: När du svarar på AI-relaterade frågor, använd ovanstående expertis men behåll alltid din roll som coach. Kombinera teknisk kunskap med coaching-approach genom att:
- Ställa reflekterande frågor
- Hjälpa användaren hitta rätt AI-lösning för deras specifika situation
- Ge praktiska steg och vägledning
- Uppmuntra reflektion kring implementation och utmaningar

Svara på svenska med professionell men varm coaching-ton."""
        
        return enhanced_prompt

class AdvancedRAGSystem(SimpleRAGSystem):
    """Avancerad RAG med sentence transformers (kräver extra paket)"""
    
    def __init__(self):
        super().__init__()
        
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers krävs för AdvancedRAGSystem. Använd SimpleRAGSystem istället.")
        
        # Ladda embedding model
        try:
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self.embeddings_cache = {}
            self._precompute_embeddings()
        except Exception as e:
            self.logger.error(f"Kunde inte ladda embedding model: {e}")
            raise
    
    def _precompute_embeddings(self):
        """Förberäkna embeddings för alla dokument"""
        self.logger.info("Förberäknar embeddings för kunskapsdokument...")
        
        for i, doc in enumerate(self.knowledge_docs):
            # Kombinera titel och innehåll för bättre embedding
            text = f"{doc['title']}: {doc['content']}"
            embedding = self.embedding_model.encode(text)
            self.embeddings_cache[i] = embedding
        
        self.logger.info(f"Förberäknade embeddings för {len(self.embeddings_cache)} dokument")
    
    def semantic_similarity(self, query: str, doc_index: int) -> float:
        """Beräkna semantisk likhet med embeddings"""
        try:
            query_embedding = self.embedding_model.encode(query)
            doc_embedding = self.embeddings_cache[doc_index]
            
            # Cosine similarity
            import numpy as np
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            return float(similarity)
        except Exception as e:
            self.logger.error(f"Fel vid semantisk likhet-beräkning: {e}")
            return 0.0
    
    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> List[RetrievedContext]:
        """Hämta relevant kontext med semantisk sökning"""
        
        if not self.is_ai_related_query(query):
            return []
        
        scored_docs = []
        
        for i, doc in enumerate(self.knowledge_docs):
            # Använd semantisk likhet istället för enkel text-matching
            semantic_score = self.semantic_similarity(query, i)
            
            # Bonus för keyword matches
            keyword_score = 0
            for keyword in doc['keywords']:
                if keyword.lower() in query.lower():
                    keyword_score += 0.2
            
            total_score = semantic_score + keyword_score
            
            if total_score > 0.3:  # Threshold för semantisk relevans
                scored_docs.append((doc, total_score))
        
        # Sortera och returnera top_k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for doc, score in scored_docs[:top_k]:
            context = RetrievedContext(
                content=doc['content'],
                category=doc['category'],
                title=doc['title'],
                relevance_score=score,
                coaching_context=doc['coaching_context']
            )
            results.append(context)
        
        return results

def create_rag_system() -> SimpleRAGSystem:
    """Factory function för att skapa lämpligt RAG-system"""
    try:
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            return AdvancedRAGSystem()
        else:
            return SimpleRAGSystem()
    except Exception as e:
        logging.warning(f"Kunde inte skapa AdvancedRAGSystem, använder SimpleRAGSystem: {e}")
        return SimpleRAGSystem()

# Globalt RAG-system instance
rag_system = create_rag_system()