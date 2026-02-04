"""
Agent system for chronic disease knowledge base
Implements QueryAgent, RetrievalAgent, and RecommendationAgent
"""

import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx

from config import settings
from kb.knowledge_base import knowledge_base
from models.query import QueryRequest, QueryResponse, KnowledgeResult, RecommendationRequest, RecommendationResponse
from models.patient import Patient


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.llm_provider = settings.DEFAULT_LLM_PROVIDER
        self.model = settings.DEFAULT_MODEL
    
    def _call_llm(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Call LLM API based on configured provider
        """
        if self.llm_provider == "openai":
            return self._call_openai(prompt, temperature, max_tokens)
        elif self.llm_provider == "anthropic":
            return self._call_anthropic(prompt, temperature, max_tokens)
        elif self.llm_provider == "google":
            return self._call_google(prompt, temperature, max_tokens)
        else:
            # Fallback to simple response for demo
            return f"[Demo Mode] LLM response for: {prompt[:100]}..."
    
    def _call_openai(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call OpenAI API"""
        api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "[Error: OpenAI API key not configured]"
        
        try:
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"[Error: {response.status_code}]"
        except Exception as e:
            return f"[Error calling OpenAI: {str(e)}]"
    
    def _call_anthropic(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call Anthropic Claude API"""
        api_key = settings.ANTHROPIC_API_KEY or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return "[Error: Anthropic API key not configured]"
        
        try:
            response = httpx.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            else:
                return f"[Error: {response.status_code}]"
        except Exception as e:
            return f"[Error calling Anthropic: {str(e)}]"
    
    def _call_google(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call Google Gemini API"""
        api_key = settings.GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "[Error: Google API key not configured]"
        
        try:
            response = httpx.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": max_tokens
                    }
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return f"[Error: {response.status_code}]"
        except Exception as e:
            return f"[Error calling Google: {str(e)}]"
    
    @abstractmethod
    def process(self, *args, **kwargs) -> Any:
        """Process input and return result"""
        pass


class QueryAgent(BaseAgent):
    """
    Query Understanding Agent
    
    Analyzes user queries to:
    - Determine query type (symptoms, treatment, general, emergency)
    - Extract disease entities
    - Understand patient context
    - Route to appropriate specialized agent
    """
    
    def __init__(self):
        super().__init__("QueryAgent")
    
    def process(self, query: str) -> Dict[str, Any]:
        """
        Analyze and classify the query
        
        Args:
            query: User's natural language query
            
        Returns:
            Dict with query classification and metadata
        """
        # Build analysis prompt
        prompt = f"""Analyze this medical query and extract key information:

Query: {query}

Provide analysis in this format:
1. Query Type: [symptoms | treatment | diagnosis | prevention | lifestyle | emergency | general]
2. Disease Mentioned: [disease name or "none"]
3. Urgency Level: [low | medium | high | emergency]
4. Key Entities: [list important medical terms]
5. Intent: [what the user wants to know]

Analysis:"""
        
        analysis = self._call_llm(prompt, temperature=0.3)
        
        # Parse analysis
        result = {
            'query': query,
            'query_type': self._extract_field(analysis, 'Query Type'),
            'disease': self._extract_field(analysis, 'Disease Mentioned'),
            'urgency': self._extract_field(analysis, 'Urgency Level'),
            'entities': self._extract_list(analysis, 'Key Entities'),
            'intent': self._extract_field(analysis, 'Intent'),
            'analysis_raw': analysis
        }
        
        return result
    
    def _extract_field(self, text: str, field: str) -> str:
        """Extract a field value from analysis text"""
        for line in text.split('\n'):
            if field.lower() in line.lower():
                parts = line.split(':')
                if len(parts) > 1:
                    return parts[1].strip().strip('[]')
        return "unknown"
    
    def _extract_list(self, text: str, field: str) -> List[str]:
        """Extract a list from analysis text"""
        for line in text.split('\n'):
            if field.lower() in line.lower():
                parts = line.split(':')
                if len(parts) > 1:
                    items = parts[1].strip()
                    # Remove brackets and split
                    items = items.strip('[]')
                    return [item.strip() for item in items.split(',') if item.strip()]
        return []


class RetrievalAgent(BaseAgent):
    """
    Knowledge Retrieval Agent
    
    Uses RAG (Retrieval Augmented Generation) to:
    - Search knowledge base for relevant documents
    - Re-rank results by relevance
    - Synthesize comprehensive answers
    """
    
    def __init__(self):
        super().__init__("RetrievalAgent")
        self.kb = knowledge_base
    
    def process(
        self,
        query: str,
        query_analysis: Optional[Dict[str, Any]] = None,
        patient_context: Optional[Dict[str, Any]] = None,
        n_results: int = 5
    ) -> QueryResponse:
        """
        Retrieve and synthesize knowledge
        
        Args:
            query: Original user query
            query_analysis: Query classification from QueryAgent
            patient_context: Patient profile information
            n_results: Number of knowledge documents to retrieve
            
        Returns:
            QueryResponse with synthesized answer
        """
        start_time = datetime.now()
        
        # Build enhanced query
        enhanced_query = query
        if query_analysis:
            disease = query_analysis.get('disease')
            if disease and disease != 'none':
                enhanced_query += f" {disease}"
        
        # Search knowledge base
        search_results = self.kb.search(
            query=enhanced_query,
            n_results=n_results * 2  # Get more for re-ranking
        )
        
        # Format knowledge results
        knowledge_results = []
        for result in search_results[:n_results]:
            knowledge_results.append(
                KnowledgeResult(
                    content=result['content'],
                    source=result['metadata'].get('source', 'medical_knowledge_base'),
                    disease=result['metadata'].get('disease'),
                    category=result['metadata'].get('category'),
                    relevance_score=1.0 - result['distance']  # Convert distance to similarity
                )
            )
        
        # Build context for answer generation
        context = self._build_context(knowledge_results, patient_context)
        
        # Generate answer
        answer_prompt = f"""Based on the following medical knowledge, answer the user's question accurately and concisely.

User Question: {query}

Medical Knowledge:
{context}

Guidelines:
- Provide accurate medical information
- Be clear and easy to understand
- Include relevant warnings if applicable
- Suggest consulting a healthcare provider for personalized advice

Answer:"""
        
        answer = self._call_llm(answer_prompt, temperature=0.5)
        
        # Calculate confidence based on relevance scores
        confidence = sum(r.relevance_score for r in knowledge_results) / len(knowledge_results) if knowledge_results else 0.0
        
        # Extract sources
        sources = list(set(r.source for r in knowledge_results))
        
        # Generate related questions
        related_questions = self._generate_related_questions(query, knowledge_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(query, query_analysis, knowledge_results)
        
        # Check for warnings
        warnings = self._check_warnings(query, knowledge_results)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return QueryResponse(
            query_id=f"query_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            query=query,
            answer=answer,
            confidence=confidence,
            results=knowledge_results,
            sources=sources,
            related_questions=related_questions,
            recommendations=recommendations,
            warnings=warnings,
            processing_time_ms=int(processing_time),
            timestamp=datetime.now(),
            patient_context_applied=patient_context is not None
        )
    
    def _build_context(
        self,
        results: List[KnowledgeResult],
        patient_context: Optional[Dict[str, Any]]
    ) -> str:
        """Build context from search results"""
        context_parts = []
        
        for i, result in enumerate(results, 1):
            context_parts.append(f"[{i}] {result.content}")
        
        if patient_context:
            context_parts.append(f"\nPatient Context: {patient_context}")
        
        return "\n\n".join(context_parts)
    
    def _generate_related_questions(
        self,
        query: str,
        results: List[KnowledgeResult]
    ) -> List[str]:
        """Generate related questions based on results"""
        prompt = f"""Given this medical query and related information, suggest 3 related questions the user might want to ask:

Original Query: {query}

Related Information:
{chr(10).join([r.content[:100] for r in results[:3]])}

Generate 3 related questions:
1.
2.
3."""
        
        response = self._call_llm(prompt, temperature=0.7, max_tokens=200)
        
        # Parse questions
        questions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove number/bullet and clean
                question = line.lstrip('0123456789.- ')
                if question:
                    questions.append(question)
        
        return questions[:3]
    
    def _generate_recommendations(
        self,
        query: str,
        query_analysis: Optional[Dict[str, Any]],
        results: List[KnowledgeResult]
    ) -> List[str]:
        """Generate recommendations based on query and results"""
        recommendations = []
        
        query_type = query_analysis.get('query_type', '') if query_analysis else ''
        
        if 'symptom' in query_type.lower():
            recommendations.append("如果症状持续或加重，请及时就医")
            recommendations.append("记录症状的出现时间和严重程度")
        
        if 'treatment' in query_type.lower():
            recommendations.append("遵循医生的治疗方案，不要自行调整药物")
            recommendations.append("定期复查监测治疗效果")
        
        if 'lifestyle' in query_type.lower():
            recommendations.append("逐步改变生活习惯，建立可持续的健康行为")
            recommendations.append("咨询营养师制定个性化饮食计划")
        
        if not recommendations:
            recommendations.append("如有疑问，请咨询专业医疗人员")
        
        return recommendations
    
    def _check_warnings(
        self,
        query: str,
        results: List[KnowledgeResult]
    ) -> List[str]:
        """Check for important warnings"""
        warnings = []
        
        # Check for emergency keywords
        emergency_keywords = ['胸痛', '呼吸困难', '昏迷', '严重出血', '中风', '心脏病']
        if any(keyword in query for keyword in emergency_keywords):
            warnings.append("⚠️ 出现这些症状可能表示紧急情况，请立即拨打急救电话或前往急诊科")
        
        # General medical disclaimer
        warnings.append("本回答仅供参考，不能替代专业医疗建议")
        
        return warnings


class RecommendationAgent(BaseAgent):
    """
    Personalized Recommendation Agent
    
    Provides personalized health recommendations based on:
    - Patient profile and medical history
    - Current health metrics
    - Evidence-based medical guidelines
    """
    
    def __init__(self):
        super().__init__("RecommendationAgent")
    
    def process(
        self,
        request: RecommendationRequest,
        patient: Optional[Patient] = None,
        recent_metrics: Optional[List[Dict[str, Any]]] = None
    ) -> RecommendationResponse:
        """
        Generate personalized recommendations
        
        Args:
            request: Recommendation request with type and constraints
            patient: Patient profile
            recent_metrics: Recent health measurements
            
        Returns:
            RecommendationResponse with personalized advice
        """
        # Build patient context
        patient_context = self._build_patient_context(patient, recent_metrics)
        
        # Get relevant knowledge
        kb_results = knowledge_base.search(
            query=f"{request.recommendation_type} recommendations {request.context or ''}",
            n_results=3
        )
        
        medical_knowledge = "\n".join([r['content'] for r in kb_results])
        
        # Build recommendation prompt
        prompt = f"""Generate personalized health recommendations based on patient profile.

Patient Information:
{patient_context}

Recommendation Type: {request.recommendation_type}
Context: {request.context or 'General'}
Constraints: {', '.join(request.constraints) if request.constraints else 'None'}

Medical Guidelines:
{medical_knowledge}

Provide recommendations in this format:
1. Recommendation: [specific actionable advice]
   Rationale: [why this helps]
   Priority: [high/medium/low]

Generate 3-5 personalized recommendations:"""
        
        response = self._call_llm(prompt, temperature=0.4)
        
        # Parse recommendations
        recommendations = self._parse_recommendations(response)
        
        # Determine priority
        priority = self._determine_priority(patient, recent_metrics)
        
        # Generate rationale
        rationale = self._generate_rationale(recommendations, patient)
        
        # Identify cautions
        cautions = self._identify_cautions(patient, request)
        
        return RecommendationResponse(
            patient_id=request.patient_id,
            recommendations=recommendations,
            priority_level=priority,
            rationale=rationale,
            cautions=cautions,
            timestamp=datetime.now()
        )
    
    def _build_patient_context(
        self,
        patient: Optional[Patient],
        metrics: Optional[List[Dict[str, Any]]]
    ) -> str:
        """Build patient context string"""
        context_parts = []
        
        if patient:
            context_parts.append(f"Age: {patient.age}, Gender: {patient.gender}")
            if patient.chronic_conditions:
                context_parts.append(f"Conditions: {', '.join(patient.chronic_conditions)}")
            if patient.allergies:
                context_parts.append(f"Allergies: {', '.join(patient.allergies)}")
        
        if metrics:
            context_parts.append("Recent Health Metrics:")
            for metric in metrics[-3:]:  # Last 3 metrics
                context_parts.append(f"  - {metric}")
        
        return "\n".join(context_parts) if context_parts else "No patient information available"
    
    def _parse_recommendations(self, response: str) -> List[Dict[str, Any]]:
        """Parse recommendations from LLM response"""
        recommendations = []
        
        lines = response.split('\n')
        current_rec = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line[0].isdigit() or line.startswith('-'):
                # Save previous recommendation
                if current_rec:
                    recommendations.append(current_rec)
                
                # Start new recommendation
                content = line.lstrip('0123456789.- ')
                if 'Recommendation:' in content:
                    content = content.split('Recommendation:')[1].strip()
                current_rec = {'recommendation': content, 'rationale': '', 'priority': 'medium'}
            
            elif 'Rationale:' in line:
                if current_rec:
                    current_rec['rationale'] = line.split('Rationale:')[1].strip()
            
            elif 'Priority:' in line:
                if current_rec:
                    current_rec['priority'] = line.split('Priority:')[1].strip().lower()
        
        # Add last recommendation
        if current_rec:
            recommendations.append(current_rec)
        
        return recommendations
    
    def _determine_priority(
        self,
        patient: Optional[Patient],
        metrics: Optional[List[Dict[str, Any]]]
    ) -> str:
        """Determine recommendation priority level"""
        # Simple logic - can be enhanced
        if patient and patient.chronic_conditions:
            high_risk_conditions = ['heart disease', 'diabetes type 1', 'severe hypertension']
            if any(condition in patient.chronic_conditions for condition in high_risk_conditions):
                return "high"
        
        return "medium"
    
    def _generate_rationale(
        self,
        recommendations: List[Dict[str, Any]],
        patient: Optional[Patient]
    ) -> str:
        """Generate overall rationale for recommendations"""
        if patient and patient.chronic_conditions:
            return f"这些建议基于您的健康状况（{', '.join(patient.chronic_conditions)}）和循证医学指南制定。"
        return "这些建议基于一般健康原则制定。请咨询医生以获得个性化建议。"
    
    def _identify_cautions(
        self,
        patient: Optional[Patient],
        request: RecommendationRequest
    ) -> List[str]:
        """Identify cautions and contraindications"""
        cautions = []
        
        if patient and patient.allergies:
            cautions.append(f"注意过敏史：{', '.join(patient.allergies)}")
        
        if request.recommendation_type == "medication":
            cautions.append("所有药物调整必须在医生指导下进行")
        
        if patient and patient.current_medications:
            cautions.append("注意与现有药物的相互作用")
        
        return cautions


class AgentOrchestrator:
    """
    Orchestrator that coordinates all agents
    """
    
    def __init__(self):
        self.query_agent = QueryAgent()
        self.retrieval_agent = RetrievalAgent()
        self.recommendation_agent = RecommendationAgent()
    
    def process_query(
        self,
        request: QueryRequest,
        patient: Optional[Patient] = None
    ) -> QueryResponse:
        """
        Process a user query through the full agent pipeline
        
        Args:
            request: Query request with user question
            patient: Optional patient context
            
        Returns:
            QueryResponse with answer and metadata
        """
        # Step 1: Query Understanding
        query_analysis = self.query_agent.process(request.query)
        
        # Step 2: Build patient context
        patient_context = None
        if patient:
            patient_context = {
                'age': patient.age,
                'gender': patient.gender.value if hasattr(patient.gender, 'value') else patient.gender,
                'conditions': patient.chronic_conditions,
                'allergies': patient.allergies
            }
        
        # Step 3: Knowledge Retrieval and Answer Generation
        response = self.retrieval_agent.process(
            query=request.query,
            query_analysis=query_analysis,
            patient_context=patient_context,
            n_results=request.max_results
        )
        
        return response
    
    def get_recommendations(
        self,
        request: RecommendationRequest,
        patient: Optional[Patient] = None,
        metrics: Optional[List[Dict[str, Any]]] = None
    ) -> RecommendationResponse:
        """Get personalized recommendations"""
        return self.recommendation_agent.process(request, patient, metrics)


# Global orchestrator instance
agent_orchestrator = AgentOrchestrator()