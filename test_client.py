import asyncio
import aiohttp
import json

async def test_rest_api():
    """Test the REST API endpoints"""
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        # Test health endpoint
        print("1. Testing health endpoint...")
        async with session.get(f"{base_url}/health") as resp:
            result = await resp.json()
            print(f"   Health: {result}")
        
        # Test tools endpoint
        print("\n2. Testing tools endpoint...")
        async with session.get(f"{base_url}/tools") as resp:
            tools = await resp.json()
            print(f"   Available tools: {tools}")
        
        # Test chat endpoint
        print("\n3. Testing chat endpoint...")
        test_messages = [
            "Hello, AI!",
            "Can you calculate 42 + 58?",
            "What's 150 divided by 3?"
        ]
        
        for msg in test_messages:
            print(f"\n   User: {msg}")
            async with session.post(
                f"{base_url}/chat",
                json={
                    "user_id": "test_user",
                    "message": msg
                }
            ) as resp:
                result = await resp.json()
                print(f"   AI: {result['response']}")

async def test_websocket():
    """Test the WebSocket endpoint"""
    print("\n4. Testing WebSocket connection...")
    
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://localhost:8000/ws/test_user") as ws:
            # Send a message
            test_message = {
                "message": "Tell me a joke about programming",
                "context": {}
            }
            
            print(f"   Sending: {test_message['message']}")
            await ws.send_str(json.dumps(test_message))
            
            # Receive streaming response
            print("   AI: ", end="")
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    
                    if data["type"] == "chunk":
                        print(data["content"], end="", flush=True)
                    elif data["type"] == "complete":
                        print("\n   [Streaming complete]")
                        break
                    elif data["type"] == "error":
                        print(f"\n   Error: {data['message']}")
                        break

async def main():
    print("=== Universal AI Core Test Client ===\n")
    
    # Wait a bit for server to be ready
    print("Waiting for server to start...")
    await asyncio.sleep(2)
    
    try:
        await test_rest_api()
        await test_websocket()
        print("\n✅ All tests completed!")
        
    except aiohttp.ClientError as e:
        print(f"\n❌ Error: Could not connect to server. Is it running?")
        print(f"   Details: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
