"""
AI Expert Knowledge Base
Strukturerad kunskapsbas för att göra AI-Coachen till en AI-expert
Används av RAG-systemet för att berika coaching med AI-expertis
"""

from typing import Dict, List

class AIExpertKnowledge:
    """Strukturerad AI-kunskapsbas organiserad för optimal RAG-sökning"""
    
    def __init__(self):
        self.knowledge_base = {
            "grundlaggande_ai": self._get_grundlaggande_ai(),
            "ai_modeller": self._get_ai_modeller(),
            "implementation": self._get_implementation(),
            "affars_ai": self._get_affars_ai(), 
            "teknisk": self._get_teknisk(),
            "framtid": self._get_framtid(),
            "sakerhet": self._get_sakerhet(),
            "universitet": self._get_universitet()
        }
    
    def get_all_knowledge(self) -> List[Dict[str, str]]:
        """Hämta all kunskap som strukturerade dokument för RAG"""
        documents = []
        
        for category, knowledge_items in self.knowledge_base.items():
            for item in knowledge_items:
                document = {
                    "content": item["content"],
                    "category": category,
                    "title": item["title"],
                    "keywords": item["keywords"],
                    "coaching_context": item.get("coaching_context", "")
                }
                documents.append(document)
        
        return documents
    
    def _get_grundlaggande_ai(self) -> List[Dict]:
        """Grundläggande AI-koncept för coaching"""
        return [
            {
                "title": "Machine Learning Fundamentals",
                "content": """Machine Learning (ML) är en gren av AI där system lär sig från data utan att vara explicit programmerade. Det finns tre huvudtyper: Supervised Learning (med labels), Unsupervised Learning (utan labels) och Reinforcement Learning (belöningsbaserat). För att lyckas med ML krävs kvalitetsdata, rätt problemformulering och kontinuerlig evaluation. Som coach hjälper jag dig förstå vilken ML-approach som passar ditt specifika problem och hur du kan bygga kompetens steg för steg.""",
                "keywords": ["machine learning", "supervised", "unsupervised", "reinforcement", "data"],
                "coaching_context": "Hjälper användare förstå ML-grunder och välja rätt approach för sina projekt"
            },
            {
                "title": "Deep Learning Essentials", 
                "content": """Deep Learning använder neurala nätverk med flera lager för att lösa komplexa problem. Det är särskilt kraftfullt för bild-, text- och talbehandling. Vanliga arkitekturer inkluderar CNN (bilder), RNN/LSTM (sekvenser) och Transformers (språk). Deep Learning kräver stora datamängder och beräkningsresurser, men ger ofta överlägsna resultat. Som din coach guidar jag dig genom när deep learning är rätt val och hur du kan börja med ramverk som TensorFlow eller PyTorch.""",
                "keywords": ["deep learning", "neural networks", "CNN", "RNN", "LSTM", "transformers"],
                "coaching_context": "Hjälper bedöma när deep learning är lämpligt och planera implementering"
            },
            {
                "title": "Natural Language Processing (NLP)",
                "content": """NLP fokuserar på att få datorer att förstå och generera mänskligt språk. Moderna NLP bygger på Transformers och stora språkmodeller som GPT och BERT. Vanliga tillämpningar inkluderar textanalys, översättning, chatbots och dokumentsammanfattning. För att lyckas med NLP behöver du förstå tokenisering, embeddings och fine-tuning. Som coach hjälper jag dig identifiera NLP-möjligheter i din verksamhet och planera praktisk implementering.""",
                "keywords": ["NLP", "natural language", "transformers", "GPT", "BERT", "tokenisering"],
                "coaching_context": "Guidar genom NLP-projekt från idé till implementation"
            },
            {
                "title": "Computer Vision Basics",
                "content": """Computer Vision låter datorer 'se' och förstå bilder och video. Huvudtekniker inkluderar bildigenkänning, objektdetektering, segmentering och generativ AI för bilder. Moderna system använder Convolutional Neural Networks (CNN) och Vision Transformers. Tillämpningar sträcker sig från medicinsk bildanalys till autonom körning. Som coach hjälper jag dig utvärdera computer vision-möjligheter och planera pilotprojekt som skapar verkligt värde.""",
                "keywords": ["computer vision", "CNN", "bildigenkänning", "objektdetektering", "medicinsk bildanalys"],
                "coaching_context": "Stöttar identifiering och planning av computer vision-tillämpningar"
            }
        ]
    
    def _get_ai_modeller(self) -> List[Dict]:
        """AI-modeller och arkitekturer"""
        return [
            {
                "title": "Transformer Architecture Deep Dive",
                "content": """Transformers revolutionerade AI genom attention-mekanismen som låter modeller fokusera på relevanta delar av input. Nyckelkomponenter är self-attention, multi-head attention och positionell encoding. Transformers är grunden för moderna språkmodeller som GPT, BERT och T5. De har också visat framgång inom computer vision (Vision Transformers). Som coach hjälper jag dig förstå när och hur du kan använda Transformers för dina specifika behov.""",
                "keywords": ["transformers", "attention", "self-attention", "GPT", "BERT", "vision transformers"],
                "coaching_context": "Förklarar Transformer-teknologi och dess praktiska tillämpningar"
            },
            {
                "title": "Large Language Models (LLMs)",
                "content": """LLMs som GPT-4, Claude och Llama är tränade på enorma textmängder och kan generera, analysera och resonera kring text. De möjliggör nya tillämpningar som intelligenta chatbots, kodgenerering och innehållsskapande. Viktiga överväganden inkluderar prompt engineering, fine-tuning, RAG (Retrieval-Augmented Generation) och hallucination management. Som coach guidar jag dig genom LLM-strategier som passar din organisation och budget.""",
                "keywords": ["LLM", "GPT", "Claude", "Llama", "prompt engineering", "fine-tuning", "RAG"],
                "coaching_context": "Strategisk rådgivning för LLM-adoption och implementation"
            },
            {
                "title": "Generative AI Models",
                "content": """Generativ AI skapar nytt innehåll - text, bilder, kod, musik och mer. Huvudkategorier inkluderar språkmodeller (GPT), bildgeneratorer (DALL-E, Midjourney, Stable Diffusion), kodgeneratorer (GitHub Copilot) och multimodala system. Generativ AI transformerar kreativa processer och produktivitet. Som coach hjälper jag dig identifiera värdefulla use cases och implementera generativ AI på ett ansvarsfullt sätt.""",
                "keywords": ["generativ AI", "DALL-E", "Midjourney", "Stable Diffusion", "GitHub Copilot", "multimodal"],
                "coaching_context": "Guidar implementation av generativ AI för produktivitet och kreativitet"
            }
        ]
    
    def _get_implementation(self) -> List[Dict]:
        """AI Implementation och MLOps"""
        return [
            {
                "title": "MLOps Best Practices", 
                "content": """MLOps är DevOps för machine learning - det standardiserar ML-utveckling från experiment till production. Nyckelelement inkluderar versionshantring av data och modeller, automatiserad training/testing, kontinuerlig monitoring och CI/CD pipelines. Populära verktyg är MLflow, Kubeflow, DVC och Weights & Biases. Framgångsrik MLOps kräver samarbete mellan data scientists och DevOps-team. Som coach hjälper jag dig bygga MLOps-kapacitet och välja rätt verktyg.""",
                "keywords": ["MLOps", "CI/CD", "MLflow", "Kubeflow", "DVC", "model monitoring"],
                "coaching_context": "Stöttar MLOps-transformation och verktygsval"
            },
            {
                "title": "Data Quality for AI Success",
                "content": """Kvalitetsdata är grunden för framgångsrik AI. Vanliga utmaningar inkluderar saknad data, bias, inkonsistens och datadrift. Best practices inkluderar dataprofiling, validation pipelines, bias testing och kontinuerlig monitoring. Data governance säkerställer ansvarsfull AI-användning. Modern AI kräver också experiment med synthetic data och data augmentation. Som coach guidar jag dig genom datastrategier som säkerställer robust AI-prestanda.""",
                "keywords": ["data quality", "bias", "datadrift", "data governance", "synthetic data"],
                "coaching_context": "Hjälper utveckla datakvalitetsstrategi för AI-projekt"
            },
            {
                "title": "AI Model Deployment Strategies",
                "content": """Att deploiera AI-modeller i production kräver överväganden av skalbarhet, latency, säkerhet och kostnader. Vanliga patterns inkluderar batch prediction, real-time serving, edge deployment och hybrid approaches. Containerisering med Docker/Kubernetes är standard, medan cloud platforms erbjuder managed services. A/B testing och gradual rollouts minimerar risker. Som coach hjälper jag dig välja deployment-strategi som matchar dina tekniska och affärsmässiga krav.""",
                "keywords": ["model deployment", "Docker", "Kubernetes", "cloud", "A/B testing", "edge deployment"],
                "coaching_context": "Planerar säker och skalbar modell-deployment"
            }
        ]
    
    def _get_affars_ai(self) -> List[Dict]:
        """Affärs-AI och strategi"""
        return [
            {
                "title": "AI ROI and Business Case Development",
                "content": """Att byggja business case för AI kräver tydlig koppling mellan tekniska möjligheter och affärsvärde. Fokusera på mätbara outcomes som kostnadsbesparing, intäktsökning eller effektivitetsförbättringar. Börja med pilotprojekt som har tydlig ROI och skalbarhetspotential. Inkludera kostnader för data, infrastruktur, talang och change management. Som coach hjälper jag dig identifiera high-impact AI use cases och bygga övertygande business cases.""",
                "keywords": ["AI ROI", "business case", "pilotprojekt", "kostnadsbesparing", "effektivitet"],
                "coaching_context": "Stöttar utveckling av övertygande AI business cases"
            },
            {
                "title": "AI Transformation Roadmap",
                "content": """Framgångsrik AI-transformation följer en strukturerad roadmap med fem faser: Assessment (nuläge), Strategy (vision och mål), Foundation (data och infrastruktur), Pilot (första projekt) och Scale (organisationsgemensam adoption). Varje fas har specifika milstones och success criteria. Critical success factors inkluderar ledarskapsstöd, rätt talang och change management. Som coach guidar jag dig genom att skapa en realistisk AI roadmap anpassad för din organisation.""",
                "keywords": ["AI transformation", "roadmap", "assessment", "pilot", "scaling", "change management"],
                "coaching_context": "Utvecklar strukturerad AI-transformationsplan"
            },
            {
                "title": "AI Maturity Assessment",
                "content": """AI-mognad mäts över flera dimensioner: Data (kvalitet, tillgänglighet, governance), Technology (infrastruktur, tools, integration), People (kompetens, roller, kultur), Process (metodiker, governance, säkerhet) och Strategy (vision, leadership, investment). Mognadsnivåer sträcker sig från Ad-hoc till Optimized. Regular assessment hjälper identifiera gaps och prioritera investeringar. Som coach hjälper jag dig bedöma nuvarande AI-mognad och planera targeted förbättringar.""",
                "keywords": ["AI maturity", "assessment", "data governance", "infrastruktur", "kompetens"],
                "coaching_context": "Utvärderar och förbättrar organisationens AI-mognad"
            }
        ]
    
    def _get_teknisk(self) -> List[Dict]:
        """Teknisk AI-implementation"""
        return [
            {
                "title": "Python for AI/ML Development",
                "content": """Python dominerar AI-utveckling tack vare kraftfulla bibliotek: NumPy/Pandas (databehandling), Scikit-learn (traditionell ML), TensorFlow/PyTorch (deep learning), Transformers (NLP) och OpenCV (computer vision). Utvecklingsmiljöer som Jupyter notebooks underlättar experimentation. Best practices inkluderar virtual environments, testing, dokumentation och kodkvalitet. Som coach hjälper jag dig bygga Python-kompetens strukturerat från grunderna till avancerade AI-tillämpningar.""",
                "keywords": ["Python", "NumPy", "Pandas", "Scikit-learn", "TensorFlow", "PyTorch", "Jupyter"],
                "coaching_context": "Guidar Python-learning för AI-utveckling"
            },
            {
                "title": "Cloud AI Services Strategy",
                "content": """Molnleverantörer erbjuder managed AI-tjänster som accelererar implementation: AWS (SageMaker, Bedrock), Azure (Cognitive Services, ML Studio), GCP (Vertex AI, AutoML). Fördelar inkluderar reduced infrastructure management, pre-trained models och auto-scaling. Överväganden inkluderar vendor lock-in, kostnader och data sovereignty. Hybrid approaches kombinerar cloud services med on-premise deployment. Som coach hjälper jag dig välja optimal cloud AI-strategi.""",
                "keywords": ["cloud AI", "AWS SageMaker", "Azure", "GCP", "managed services", "hybrid"],
                "coaching_context": "Planerar cloud AI-strategi baserat på organisationens behov"
            },
            {
                "title": "Vector Databases and Embeddings",
                "content": """Vector databases lagrar och söker i high-dimensional embeddings som representerar text, bilder eller andra data. Populära lösningar inkluderar Pinecone, Weaviate, ChromaDB och Milvus. De möjliggör semantic search, recommendation systems och RAG (Retrieval-Augmented Generation). Viktiga överväganden är embedding-kvalitet, index-performance och skalbarhet. Som coach hjälper jag dig förstå när vector databases är värdefulla och implementera dem effektivt.""",
                "keywords": ["vector database", "embeddings", "Pinecone", "Weaviate", "ChromaDB", "semantic search", "RAG"],
                "coaching_context": "Implementerar vector search för AI-tillämpningar"
            }
        ]
    
    def _get_framtid(self) -> List[Dict]:
        """AI-framtid och trender"""
        return [
            {
                "title": "Multimodal AI Revolution",
                "content": """Multimodal AI kombinerar text, bilder, ljud och video i en enda modell, möjliggörandes mer naturliga interaktioner och rikare förståelse. GPT-4V, DALL-E 3 och kommande system visar potentialen. Tillämpningar inkluderar avancerade assistenter, kreativa verktyg och automatiserad innehållsanalys. Utmaningar inkluderar computational complexity och training data requirements. Som coach hjälper jag dig förstå multimodal möjligheter och planera för denna teknologiska shift.""",
                "keywords": ["multimodal AI", "GPT-4V", "DALL-E", "text och bilder", "naturliga interaktioner"],
                "coaching_context": "Förbereder för multimodal AI-adoption"
            },
            {
                "title": "Edge AI and On-Device Intelligence",
                "content": """Edge AI flyttar AI-processing närmare användare genom on-device eller edge computing, vilket minskar latency, förbättrar privacy och reducerar bandwidthskrav. Möjliggörs av specialized chips (NPUs, TPUs) och model optimization techniques (quantization, pruning). Viktiga use cases inkluderar autonomous vehicles, smart cameras och IoT applications. Som coach guidar jag dig genom edge AI-strategier som balanserar performance, cost och privacy.""",
                "keywords": ["edge AI", "on-device", "NPU", "TPU", "quantization", "IoT", "autonomous vehicles"],
                "coaching_context": "Planerar edge AI för decentraliserade tillämpningar"
            },
            {
                "title": "AutoML and No-Code AI Platforms",
                "content": """AutoML demokratiserar AI genom att automatisera model selection, hyperparameter tuning och architecture search. No-code platforms låter business users bygga AI-lösningar utan programmering. Exempel inkluderar Google AutoML, H2O.ai och Microsoft Power Platform AI Builder. Medan dessa verktyg ökar AI-tillgänglighet behövs fortfarande expertis för komplex problemlösning. Som coach hjälper jag dig avgöra när AutoML är lämpligt och hur det kompletterar traditional AI-utveckling.""",
                "keywords": ["AutoML", "no-code AI", "Google AutoML", "H2O.ai", "Power Platform", "demokratisering"],
                "coaching_context": "Vägleder när och hur AutoML kan accelerera AI-adoption"
            }
        ]
    
    def _get_sakerhet(self) -> List[Dict]:
        """AI-säkerhet och governance"""
        return [
            {
                "title": "AI Security Best Practices",
                "content": """AI-säkerhet omfattar flera dimensioner: Model security (adversarial attacks, model stealing), Data security (privacy, encryption), Infrastructure security (secure deployment) och Operational security (monitoring, incident response). Vanliga hot inkluderar data poisoning, prompt injection och model inversion attacks. Best practices inkluderar robust training data validation, secure model serving, regular security audits och incident response plans. Som coach hjälper jag dig utveckla comprehensive AI security strategies.""",
                "keywords": ["AI security", "adversarial attacks", "data poisoning", "prompt injection", "model serving"],
                "coaching_context": "Utvecklar robusta AI-säkerhetsstrategier"
            },
            {
                "title": "GDPR and AI Compliance",
                "content": """GDPR påverkar AI-system genom krav på transparency, user consent, data minimization och 'right to explanation'. AI-specifika utmaningar inkluderar automated decision-making, profiling och cross-border data transfers. Compliance strategies inkluderar privacy by design, impact assessments, clear consent mechanisms och audit trails. Emerging regulations som EU AI Act kräver additional considerations. Som coach guidar jag dig genom AI compliance-krav och praktisk implementering.""",
                "keywords": ["GDPR", "AI compliance", "privacy by design", "automated decisions", "EU AI Act"],
                "coaching_context": "Säkerställer AI-compliance med dataskyddsregleringar"
            },
            {
                "title": "Ethical AI and Bias Mitigation",
                "content": """Ethical AI säkerställer fair, transparent och accountable AI-system. Vanliga bias-källor inkluderar training data, algorithm design och deployment context. Mitigation strategies inkluderar diverse teams, bias testing, fairness metrics och continuous monitoring. Frameworks som IEEE Ethical AI och Partnership on AI ger vägledning. Organisationer behöver clear AI ethics policies och governance structures. Som coach hjälper jag dig bygga ethical AI practices in i utvecklingsprocesser.""",
                "keywords": ["ethical AI", "bias mitigation", "fairness metrics", "IEEE Ethical AI", "governance"],
                "coaching_context": "Implementerar ethical AI practices och bias mitigation"
            }
        ]
    
    def _get_universitet(self) -> List[Dict]:
        """Universitets-specifik AI"""
        return [
            {
                "title": "AI in Academic Research",
                "content": """AI transformerar akademisk forskning genom automated literature reviews, hypothesis generation, experiment design och data analysis. Forskare använder AI för pattern discovery, simulation och predictive modeling. Interdisciplinary AI research växer inom områden som computational biology, digital humanities och climate science. Utmaningar inkluderar reproducibility, ethical considerations och researcher training. Som coach hjälper jag forskare integrera AI i sina forskningsprojekt på ett metodiskt och ansvarsfullt sätt.""",
                "keywords": ["akademisk forskning", "literature reviews", "hypothesis generation", "reproducibility", "interdisciplinary"],
                "coaching_context": "Stöttar forskare i AI-integration för forskningsprojekt"
            },
            {
                "title": "Learning Analytics and Educational AI",
                "content": """Learning Analytics använder AI för att förstå och förbättra lärande genom analys av studentdata, learning patterns och educational outcomes. Tillämpningar inkluderar adaptive learning systems, automated assessment, early warning systems och personalized learning paths. Privacy och ethics är kritiska considerations när man arbetar med studentdata. Modern EdTech integrerar AI för enhanced learning experiences. Som coach guidar jag universitet genom responsible implementation av learning analytics.""",
                "keywords": ["learning analytics", "studentdata", "adaptive learning", "automated assessment", "EdTech"],
                "coaching_context": "Implementerar learning analytics med fokus på student privacy"
            },
            {
                "title": "University AI Governance Framework",
                "content": """Universitet behöver comprehensive AI governance för att säkerställa responsible AI adoption. Framework inkluderar AI ethics committee, clear policies för AI use i forskning och undervisning, risk assessment procedures och stakeholder engagement processes. Viktiga områden är research integrity, student privacy, faculty training och vendor management. International collaboration och knowledge sharing accelererar best practice development. Som coach hjälper jag universitet utveckla robusta AI governance structures.""",
                "keywords": ["AI governance", "ethics committee", "research integrity", "faculty training", "vendor management"],
                "coaching_context": "Utvecklar university-wide AI governance och policies"
            },
            {
                "title": "Faculty AI Training and Support",
                "content": """Framgångsrik universitets-AI kräver structured faculty development programs som bygger AI literacy och practical skills. Training ska täcka AI fundamentals, discipline-specific applications, ethical considerations och hands-on workshops. Support inkluderar AI champions network, regular seminars, access till AI tools och collaboration opportunities. Change management är critical för widespread adoption. Som coach designar jag comprehensive faculty AI training programs som accelererar adoption.""",
                "keywords": ["faculty training", "AI literacy", "discipline-specific", "AI champions", "change management"],
                "coaching_context": "Designar effektiva faculty AI training program"
            }
        ]

# Globalt instance för enkel access
ai_expert_knowledge = AIExpertKnowledge()