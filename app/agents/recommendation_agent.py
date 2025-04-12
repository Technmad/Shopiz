from app.agents.base_agent import BaseAgent
from app.services.recommendation_service import RecommendationService
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
import asyncio

class RecommendationAgent(BaseAgent):
    """Agent for generating product recommendations"""
    
    def __init__(self, db: Session):
        super().__init__()
        # Wrap the original service
        self.service = RecommendationService(db)
    
    @property
    def agent_name(self) -> str:
        return "Recommendation Agent"
    
    @property
    def agent_role(self) -> str:
        return "I generate personalized product recommendations based on user preferences, history, and behavior patterns."
    
    async def get_recommendations(
        self, 
        user_id: str, 
        query: Optional[str] = None, 
        limit: int = 5
    ) -> Dict[str, Any]:
        """Get personalized recommendations for a user"""
        try:
            # Validate input
            if not user_id or not isinstance(user_id, str):
                return {
                    "agent": self.agent_name,
                    "error": "Invalid user ID",
                    "recommendations": {}
                }
                
            if limit < 1 or limit > 20:
                limit = 5  # Reset to default if invalid
            
            # Call the service method (which is already async)
            recommendations = await self.service.get_recommendations(user_id, query)
            
            # If we need to limit results, do it here after receiving them
            if recommendations and "similar_products" in recommendations and limit != 5:
                for key in recommendations["similar_products"]:
                    recommendations["similar_products"][key] = recommendations["similar_products"][key][:limit]
            
            # Log the activity
            self.log_activity("Generated recommendations", {
                "user_id": user_id,
                "query": query if query else "None",
                "limit": limit,
                "count": len(recommendations.get("similar_products", {}).get("ids", []))
            })
            
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "user_id": user_id,
                "query": query if query else "None",
                "recommendations_text": recommendations.get("recommendations", ""),
                "products": recommendations.get("similar_products", {}),
                "user_profile": recommendations.get("user_profile", {})
            }
        except Exception as e:
            self.log_activity("Error generating recommendations", {
                "user_id": user_id,
                "error": str(e)
            })
            return {
                "agent": self.agent_name,
                "user_id": user_id,
                "error": f"Failed to generate recommendations: {str(e)}",
                "recommendations_text": "",
                "products": {}
            }
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile information"""
        try:
            if not user_id or not isinstance(user_id, str):
                return {
                    "agent": self.agent_name,
                    "error": "Invalid user ID",
                    "user_profile": {}
                }
            
            # Call the service method
            user_profile = await self.service._get_user_profile_async(user_id)
            
            # Log the activity
            self.log_activity("Retrieved user profile", {
                "user_id": user_id
            })
            
            return {
                "agent": self.agent_name,
                "user_id": user_id,
                "user_profile": user_profile
            }
        except Exception as e:
            self.log_activity("Error retrieving user profile", {
                "user_id": user_id,
                "error": str(e)
            })
            return {
                "agent": self.agent_name,
                "user_id": user_id,
                "error": f"Failed to retrieve user profile: {str(e)}",
                "user_profile": {}
            }