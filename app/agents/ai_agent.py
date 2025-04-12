from app.agents.base_agent import BaseAgent
from app.services.gemini_service import GeminiService
from typing import Dict, List, Any
import asyncio

class AIAgent(BaseAgent):
    """Agent providing AI text generation and reasoning capabilities using Gemini"""
    
    def __init__(self):
        super().__init__()
        # Wrap the original GeminiService
        self.service = GeminiService()
    
    @property
    def agent_name(self):
        return "AI Intelligence Agent"
    
    @property
    def agent_role(self):
        return "I provide intelligent text generation, reasoning, and personalized recommendations using Google's Gemini model."
    
    async def generate_recommendation(self, user_profile: Dict, products: List, feedback_stats: Dict) -> Dict:
        """Generate personalized recommendation text based on user profile and available products"""
        # Call the original service method
        result = await self.service.generate_recommendation(user_profile, products, feedback_stats)
        
        # Log the activity
        self.log_activity("Generated recommendation", {
            "user_id": user_profile.get("id", "unknown"),
            "num_products": len(products)
        })
        
        # Return with agent metadata
        return {
            "agent": self.agent_name,
            "recommendations": result
        }
    
    async def generate_content(self, prompt: str) -> Dict[str, Any]:
        """Generate text content based on prompt using Gemini model"""
        # Create custom prompt with agent context
        enhanced_prompt = f"As an {self.agent_name}, {self.agent_role}\n\n{prompt}"
        
        try:
            # Call Gemini model directly (similar to how the service does it)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.service.model.generate_content(enhanced_prompt)
            )
        
            # Log the activity
            self.log_activity("Generated content", {
                "prompt_length": len(prompt)
            })
        
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "content": response.text
            }
            
        except Exception as e:
            self.logger.error(f"Error generating content: {str(e)}")
            return {
                "agent": self.agent_name,
                "error": str(e),
                "content": "Sorry, I couldn't generate content at this time."
            }