from app.agents.base_agent import BaseAgent
from app.services.feedback_analyzer import FeedbackAnalyzer
from sqlalchemy.orm import Session
from typing import Dict, Set, List, Any, Optional
import asyncio

class FeedbackAnalyzerAgent(BaseAgent):
    """Agent for analyzing customer feedback and product reviews"""
    
    def __init__(self, db: Session):
        super().__init__()
        # Wrap the original FeedbackAnalyzer service
        self.service = FeedbackAnalyzer(db)
    
    @property
    def agent_name(self) -> str:
        return "Feedback Analyzer Agent"
    
    @property
    def agent_role(self) -> str:
        return "I analyze customer feedback and product reviews to extract insights, identify trends, and provide product satisfaction metrics."
    
    async def extract_rating(self, feedback: str) -> Dict[str, Any]:
        """Extract rating value from feedback text"""
        try:
            # Validate input
            if not feedback or not isinstance(feedback, str):
                return {
                    "agent": self.agent_name,
                    "error": "Invalid feedback text",
                    "rating": 0
                }
                
            # Call the service method asynchronously
            loop = asyncio.get_event_loop()
            rating = await loop.run_in_executor(None, self.service.extract_rating, feedback)
            
            # Log the activity
            self.log_activity("Extracted rating from feedback", {
                "feedback_length": len(feedback),
                "rating": rating
            })
            
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "rating": rating
            }
        except Exception as e:
            self.log_activity("Error extracting rating", {"error": str(e)})
            return {
                "agent": self.agent_name,
                "error": f"Failed to extract rating: {str(e)}",
                "rating": 0
            }
    
    async def get_user_feedback_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics about a user's feedback history"""
        try:
            # Validate input
            if not user_id or not isinstance(user_id, str):
                return {
                    "agent": self.agent_name,
                    "error": "Invalid user ID",
                    "feedback_stats": {}
                }
                
            # Call the service method asynchronously
            loop = asyncio.get_event_loop()
            stats = await loop.run_in_executor(None, self.service.get_user_feedback_stats, user_id)
            
            # Log the activity
            self.log_activity("Retrieved user feedback statistics", {
                "user_id": user_id
            })
            
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "user_id": user_id,
                "feedback_stats": stats
            }
        except Exception as e:
            self.log_activity("Error getting user feedback stats", {
                "user_id": user_id,
                "error": str(e)
            })
            return {
                "agent": self.agent_name,
                "user_id": user_id,
                "error": f"Failed to get user feedback stats: {str(e)}",
                "feedback_stats": {}
            }
    
    async def get_low_rated_products(self, user_id: str, threshold: int = 3) -> Dict[str, Any]:
        """Get products that the user rated below threshold"""
        try:
            # Validate input
            if not user_id or not isinstance(user_id, str):
                return {
                    "agent": self.agent_name,
                    "error": "Invalid user ID",
                    "low_rated_products": []
                }
                
            if not isinstance(threshold, int) or threshold < 1 or threshold > 5:
                threshold = 3  # Reset to default if invalid
                
            # Call the service method asynchronously
            loop = asyncio.get_event_loop()
            low_rated = await loop.run_in_executor(
                None, 
                lambda: self.service.get_low_rated_products(user_id, threshold)
            )
            
            # Log the activity
            self.log_activity("Identified low-rated products", {
                "user_id": user_id,
                "threshold": threshold,
                "count": len(low_rated)
            })
            
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "user_id": user_id,
                "threshold": threshold,
                "low_rated_products": list(low_rated)
            }
        except Exception as e:
            self.log_activity("Error getting low rated products", {
                "user_id": user_id,
                "threshold": threshold,
                "error": str(e)
            })
            return {
                "agent": self.agent_name,
                "user_id": user_id,
                "threshold": threshold,
                "error": f"Failed to get low rated products: {str(e)}",
                "low_rated_products": []
            }
    
    async def get_product_feedback_stats(self, product_id: str) -> Dict[str, Any]:
        """Get feedback statistics for a specific product"""
        try:
            # Validate input
            if not product_id or not isinstance(product_id, str):
                return {
                    "agent": self.agent_name,
                    "error": "Invalid product ID",
                    "feedback_stats": {}
                }
                
            # Call the service method asynchronously
            loop = asyncio.get_event_loop()
            stats = await loop.run_in_executor(None, self.service.get_product_feedback_stats, product_id)
            
            # Log the activity
            self.log_activity("Retrieved product feedback statistics", {
                "product_id": product_id
            })
            
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "product_id": product_id,
                "feedback_stats": stats
            }
        except Exception as e:
            self.log_activity("Error getting product feedback stats", {
                "product_id": product_id,
                "error": str(e)
            })
            return {
                "agent": self.agent_name,
                "product_id": product_id,
                "error": f"Failed to get product feedback stats: {str(e)}",
                "feedback_stats": {}
            }
    
    async def get_global_feedback_stats(self) -> Dict[str, Any]:
        """Get overall feedback statistics across all products"""
        try:
            # Call the service method asynchronously
            loop = asyncio.get_event_loop()
            stats = await loop.run_in_executor(None, self.service.get_global_feedback_stats)
            
            # Log the activity
            self.log_activity("Retrieved global feedback statistics")
            
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "global_stats": stats
            }
        except Exception as e:
            self.log_activity("Error getting global feedback stats", {"error": str(e)})
            return {
                "agent": self.agent_name,
                "error": f"Failed to get global feedback stats: {str(e)}",
                "global_stats": {}
            }