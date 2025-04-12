from app.agents.base_agent import BaseAgent
from app.services.vector_store import VectorStore
from typing import Dict, List, Any
import asyncio

class VectorAgent(BaseAgent):
    """Agent for semantic search and vector operations"""
    
    def __init__(self):
        super().__init__()
        # Wrap the original service
        self.service = VectorStore()
    
    @property
    def agent_name(self) -> str:
        return "Vector Intelligence Agent"
    
    @property
    def agent_role(self) -> str:
        return "I perform semantic search and help find products similar to what users are looking for."
    
    async def search_similar_products(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Search for products similar to the query"""
        try:
            # Validate input
            if not query or not isinstance(query, str):
                return {
                    "agent": self.agent_name,
                    "error": "Invalid query",
                    "results": []
                }
                

            loop = asyncio.get_event_loop()
            # Call the service method asynchronously
            results = await loop.run_in_executor(
                None, 
                lambda: self.service.search_similar_products(query, n_results)
            )
            
            # Log the activity
            self.log_activity("Performed semantic search", {
                "query": query,
                "n_results": n_results
            })
            
            # Process results to make them more useful
            processed_results = []
            if "ids" in results and results["ids"]:
                for i in range(len(results["ids"])):
                    product_id = results["ids"][i]
                    metadata = results["metadatas"][i] if "metadatas" in results and i < len(results["metadatas"]) else {}
                    document = results["documents"][i] if "documents" in results and i < len(results["documents"]) else ""
                    distance = results["distances"][i] if "distances" in results and results["distances"] and i < len(results["distances"]) else None
                    
                    # Calculate relevance score (1.0 is exact match, 0.0 is completely unrelated)
                    relevance = 1.0 - (distance / 2.0) if distance is not None else 1.0
                    relevance = max(0.0, min(1.0, relevance))  # Clamp to 0-1 range
                    
                    processed_results.append({
                        "id": product_id,
                        "document": document,
                        "metadata": metadata,
                        "relevance": round(relevance, 2),
                        "distance": distance
                    })
            
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "query": query,
                "results": processed_results
            }
        except Exception as e:
            self.log_activity("Error performing semantic search", {
                "query": query,
                "error": str(e)
            })
            return {
                "agent": self.agent_name,
                "query": query,
                "error": f"Failed to perform semantic search: {str(e)}",
                "results": []
            }
    
    async def add_products(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add products to the vector store"""
        try:
            # Validate input
            if not products or not isinstance(products, list):
                return {
                    "agent": self.agent_name,
                    "error": "Invalid products data",
                    "count": 0
                }
                
            loop = asyncio.get_event_loop()
            # Call the service method asynchronously
            await loop.run_in_executor(None, self.service.add_products, products)
            
            # Log the activity
            self.log_activity("Added products to vector store", {
                "count": len(products)
            })
            
            # Return with agent metadata
            return {
                "agent": self.agent_name,
                "status": "Products added to vector store successfully",
                "count": len(products)
            }
        except Exception as e:
            self.log_activity("Error adding products", {
                "count": len(products) if products else 0,
                "error": str(e)
            })
            return {
                "agent": self.agent_name,
                "error": f"Failed to add products: {str(e)}",
                "count": 0
            }