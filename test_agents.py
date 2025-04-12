import asyncio
import json
from dotenv import load_dotenv
import os
import sys
from sqlalchemy import text
from app.database import create_tables

# Make sure Python can find your app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.agents.coordinator import AgentCoordinator

async def test_coordinator():
    """Test the agent coordinator"""
    db = SessionLocal()
    
    try:
        print("\n=== Testing Agent System ===\n")
        
        #create_tables()
        
        # Initialize the coordinator
        coordinator = AgentCoordinator(db)
        
        # Get a test user from the database
        test_user = db.execute(text("SELECT id FROM users LIMIT 1")).fetchone()
        if not test_user:
            print("No test user found in database! Please ensure you have at least one user.")
            return
            
        user_id = test_user[0]
        print(f"Using test user ID: {user_id}")
        
        # Get a test product from the database
        test_product = db.execute(text("SELECT id FROM products LIMIT 1")).fetchone()
        if not test_product:
            print("No test product found in database! Please ensure you have at least one product.")
            return
            
        product_id = test_product[0]
        print(f"Using test product ID: {product_id}")
        
        # Test smart recommendations
        print("\nTesting smart recommendations...")
        recommendations = await coordinator.get_smart_recommendations(
            user_id=user_id,
            query="summer clothes"
        )
        
        print(f"Recommendations status: {recommendations.get('status', 'unknown')}")
        print(f"Agents used: {', '.join(filter(None, recommendations.get('agents_used', [])))}") 
        
        # Test product feedback analysis
        print("\nTesting product feedback analysis...")
        feedback_analysis = await coordinator.analyze_product_feedback(product_id)
        
        print(f"Product analysis status: {feedback_analysis.get('status', 'unknown')}")
        print(f"Agents used: {', '.join(filter(None, feedback_analysis.get('agents_used', [])))}") 
        
        print("\n=== Test completed successfully! ===")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    asyncio.run(test_coordinator())