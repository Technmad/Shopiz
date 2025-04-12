from sqlalchemy.orm import Session
from app.agents.ai_agent import AIAgent
from app.agents.feedback_agent import FeedbackAnalyzerAgent
from app.agents.vector_agent import VectorAgent
from app.agents.recommendation_agent import RecommendationAgent
from typing import Dict, List, Any, Optional
import asyncio

class AgentCoordinator:
    """Coordinates multiple agents to create a cohesive multi-agent system"""
    
    def __init__(self, db: Session):
        # Initialize all agents
        self.ai_agent = AIAgent()
        self.feedback_agent = FeedbackAnalyzerAgent(db)
        self.vector_agent = VectorAgent()
        self.recommendation_agent = RecommendationAgent(db)
    
    async def get_smart_recommendations(
        self, 
        user_id: str, 
        query: Optional[str] = None, 
        limit: int = 5
    ) -> Dict[str, Any]:
        """Get enhanced recommendations using multiple agents"""
        
        # Step 1: Get basic recommendations using recommendation agent
        recommendation_result = await self.recommendation_agent.get_recommendations(
            user_id=user_id,
            query=query,
            limit=limit
        )
        
        # Handle possible error in recommendation agent
        if "error" in recommendation_result:
            return {
                "status": "error",
                "message": recommendation_result["error"],
                "recommendations": []
            }
        
        # Step 2: If user provided a specific query, enhance with vector search
        if query:
            vector_result = await self.vector_agent.search_similar_products(
                query=query,
                n_results=limit
            )
            
            # If vector search was successful
            if "results" in vector_result and not "error" in vector_result:
                # Get recommended products from recommendation agent
                recommended_products = recommendation_result.get("products", {}).get("ids", [])
                
                # Get vector search products
                vector_products = [item.get("id") for item in vector_result.get("results", [])]
                
                # Combine results (priority to recommendation agent results)
                combined_products = []
                product_ids_seen = set()
                
                # First add recommendation agent results
                for product_id in recommended_products:
                    if product_id not in product_ids_seen:
                        product_ids_seen.add(product_id)
                        combined_products.append(product_id)
                
                # Then add vector agent results not already included
                for product_id in vector_products:
                    if product_id not in product_ids_seen:
                        product_ids_seen.add(product_id)
                        combined_products.append(product_id)
                
                # Limit to requested number
                combined_products = combined_products[:limit]
        
        # Step 3: Return the enhanced results
        return {
            "status": "success",
            "user_id": user_id,
            "query": query if query else None,
            "recommendations_text": recommendation_result.get("recommendations_text", ""),
            "products": recommendation_result.get("products", {}),
            "agents_used": [
                self.recommendation_agent.agent_name,
                self.vector_agent.agent_name if query else None
            ]
        }
    
    async def analyze_product_feedback(self, product_id: str) -> Dict[str, Any]:
        """Analyze product feedback using multiple agents"""
        
        # Step 1: Get product feedback statistics
        feedback_result = await self.feedback_agent.get_product_feedback_stats(product_id)
        
        # Handle possible error
        if "error" in feedback_result:
            return {
                "status": "error",
                "message": feedback_result["error"],
                "product_id": product_id
            }
        
        # Step 2: Generate insights from the AI agent
        feedback_stats = feedback_result.get("feedback_stats", {})
        
        insight_prompt = f"""
        Analyze this product feedback statistics:
        
        Product ID: {product_id}
        
        Feedback Statistics:
        - Average Rating: {feedback_stats.get('average_rating', 'N/A')}
        - Total Reviews: {feedback_stats.get('total_feedbacks', 0)}
        
        Based on this data, please provide:
        1. A summary of what this rating suggests about the product
        2. Key insights that would be valuable for shoppers
        3. Suggestions for the types of customers this product might be good for
        """
        
        insight_result = await self.ai_agent.generate_content(insight_prompt)
        
        # Step 3: Return combined insights
        return {
            "status": "success",
            "product_id": product_id,
            "feedback_statistics": feedback_stats,
            "ai_insights": insight_result.get("content", ""),
            "agents_used": [
                self.feedback_agent.agent_name,
                self.ai_agent.agent_name
            ]
        }