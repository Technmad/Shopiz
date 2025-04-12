from abc import ABC, abstractmethod
import os
import logging
from typing import Dict, Any

class BaseAgent(ABC):
    """Simple wrapper to convert existing services into agents"""
    
    def __init__(self):
        # Keep using your existing environment setup
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
        self.logger = logging.getLogger(f"agent.{self.__class__.__name__}")
    
    
    @property
    @abstractmethod
    def agent_name(self):
        """Return the name of this agent"""
        pass
    
    @property
    @abstractmethod
    def agent_role(self):
        """Return the role description for this agent"""
        pass
    
    def log_activity(self, activity_type: str, details: Dict[str, Any]) -> None:
        """Log agent activity with structured data"""
        self.logger.info(f"{self.agent_name}: {activity_type}", extra={"details": details})