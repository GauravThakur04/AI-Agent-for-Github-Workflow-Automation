#!/usr/bin/env python3
"""
MongoDB Setup Script for GitHub AI Agent
This script helps initialize the MongoDB database and test the connection.
"""

import os
from dotenv import load_dotenv
from database import db_service

def setup_mongodb():
    """Setup and test MongoDB connection"""
    print("🔧 Setting up MongoDB for GitHub AI Agent...")
    
    # Load environment variables
    load_dotenv()
    
    # Test database connection
    print("\n📊 Testing database connection...")
    health = db_service.health_check()
    
    if health["status"] == "healthy":
        print("✅ Database connection successful!")
        print(f"   Database: {health['database']}")
        print(f"   Collections: {health['collections']}")
        print(f"   Data Size: {health['data_size']} bytes")
        print(f"   Storage Size: {health['storage_size']} bytes")
    else:
        print("❌ Database connection failed!")
        print(f"   Error: {health.get('error', 'Unknown error')}")
        print("\n💡 Make sure MongoDB is running and accessible.")
        print("   You can install MongoDB locally or use MongoDB Atlas.")
        return False
    
    # Test creating a sample user
    print("\n👤 Testing user creation...")
    try:
        # This is just a test - we'll clean it up
        test_user_data = {
            "username": "test_setup_user",
            "email": "test@setup.com",
            "password": "test123",
            "github_url": "https://github.com/octocat/Hello-World",
            "github_username": "octocat",
            "github_repo": "octocat/Hello-World",
            "is_active": True
        }
        
        created_user = db_service.create_user(test_user_data)
        print(f"✅ Test user created: {created_user['username']}")
        
        # Clean up test user
        db_service.users.delete_one({"_id": created_user["_id"]})
        print("🧹 Test user cleaned up")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False
    
    print("\n🎉 MongoDB setup completed successfully!")
    print("\n📋 Database Collections Created:")
    print("   • users - User accounts and profiles")
    print("   • repositories - GitHub repository configurations")
    print("   • user_sessions - User authentication sessions")
    print("   • chat_sessions - Chat conversation sessions")
    print("   • messages - Individual chat messages")
    
    print("\n🔗 Connection Details:")
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    print(f"   URI: {mongo_uri}")
    print(f"   Database: github_ai_agent")
    
    return True

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📖 Usage Instructions:")
    print("1. Make sure MongoDB is running")
    print("2. Set MONGODB_URI in your .env file (optional, defaults to localhost)")
    print("3. Run the backend server: python -m uvicorn main:app --reload")
    print("4. Use the Postman collection to test the API")
    
    print("\n🔧 Environment Variables:")
    print("   MONGODB_URI=mongodb://localhost:27017  # MongoDB connection string")
    print("   GITHUB_TOKEN=your_github_token         # GitHub API token")
    print("   HF_TOKEN=your_huggingface_token        # Hugging Face API token")

if __name__ == "__main__":
    print("🚀 GitHub AI Agent - MongoDB Setup")
    print("=" * 50)
    
    success = setup_mongodb()
    
    if success:
        show_usage_instructions()
    else:
        print("\n❌ Setup failed. Please check your MongoDB configuration.")
        print("💡 For local development, you can:")
        print("   1. Install MongoDB Community Server")
        print("   2. Use Docker: docker run -d -p 27017:27017 mongo:latest")
        print("   3. Use MongoDB Atlas (cloud service)") 