import asyncio
from core.config import settings
from core.brain import AIBrain, BrainConfig
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def example_conversation():
    """Example of using the AI Brain"""
    
    # Configure the brain
    config = BrainConfig(
        app_name=settings.app_name,
        version=settings.app_version,
        db_url=settings.database_url,
        model_provider=settings.model_provider,
        model_name=settings.model_name,
        temperature=settings.model_temperature,
    )
    
    # Initialize brain
    logger.info("Initializing AI Brain...")
    brain = AIBrain(config)
    await brain.initialize()
    logger.info("Brain initialized successfully!")
    
    # Example: Register a simple tool
    from domain.example.tools.calculator import CalculatorTool
    brain.components['tools'].register_tool(CalculatorTool())
    
    # Example conversation
    user_id = "example_user_123"
    
    # Test messages
    test_messages = [
        "Hello! How are you?",
        "Can you calculate 15 + 27 for me?",
        "What's 100 divided by 4?",
        "Thanks for your help!"
    ]
    
    print("\n=== AI Conversation Demo ===\n")
    
    try:
        for message in test_messages:
            print(f"👤 User: {message}")
            print("🤖 AI: ", end="")
            
            # Get streaming response
            async for chunk in brain.process(user_id, message):
                print(chunk, end="", flush=True)
            
            print("\n")  # New line after response
            await asyncio.sleep(0.5)  # Small delay between messages
            
    except KeyboardInterrupt:
        print("\n\nConversation interrupted by user")
    except Exception as e:
        logger.error(f"Error during conversation: {e}")
    finally:
        # Cleanup
        logger.info("Shutting down...")
        await brain.shutdown()
        logger.info("Shutdown complete")

if __name__ == "__main__":
    print("Starting Universal AI Core Demo...")
    print("Press Ctrl+C to exit\n")
    
    try:
        asyncio.run(example_conversation())
    except KeyboardInterrupt:
        print("\nGoodbye!")
