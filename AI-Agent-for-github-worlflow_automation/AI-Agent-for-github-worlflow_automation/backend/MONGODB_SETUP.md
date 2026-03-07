# MongoDB Integration for GitHub AI Agent

This document explains the MongoDB integration for the GitHub AI Agent, including database schema, setup instructions, and usage examples.

## 🗄️ Database Schema

The application uses MongoDB with the following collections:

### 1. **users** Collection
Stores user account information and authentication data.

```javascript
{
  "_id": ObjectId,
  "username": "string",           // Unique username
  "email": "string",              // Unique email address
  "password": "string",           // Hashed password (in production)
  "github_url": "string",         // GitHub repository URL
  "github_username": "string",    // GitHub username
  "github_repo": "string",        // Repository name (username/repo)
  "created_at": "datetime",       // Account creation timestamp
  "updated_at": "datetime",       // Last update timestamp
  "last_login": "datetime",       // Last login timestamp
  "is_active": "boolean"          // Account status
}
```

### 2. **repositories** Collection
Stores GitHub repository configurations for each user.

```javascript
{
  "_id": ObjectId,
  "user_id": "ObjectId",          // Reference to users collection
  "github_url": "string",         // GitHub repository URL
  "github_username": "string",    // GitHub username
  "github_repo": "string",        // Repository name
  "is_primary": "boolean",        // Primary repository flag
  "created_at": "datetime",       // Creation timestamp
  "updated_at": "datetime"        // Last update timestamp
}
```

### 3. **user_sessions** Collection
Manages user authentication sessions.

```javascript
{
  "_id": ObjectId,
  "session_id": "string",         // Unique session identifier
  "user_id": "ObjectId",          // Reference to users collection
  "username": "string",           // Username for quick access
  "github_repo": "string",        // Current repository
  "created_at": "datetime",       // Session creation timestamp
  "updated_at": "datetime",       // Last activity timestamp
  "is_active": "boolean"          // Session status
}
```

### 4. **chat_sessions** Collection
Tracks chat conversation sessions.

```javascript
{
  "_id": ObjectId,
  "session_id": "string",         // Unique session identifier
  "user_id": "ObjectId",          // Reference to users collection
  "github_repo": "string",        // Repository being worked on
  "message_count": "number",      // Total messages in session
  "last_message_at": "datetime",  // Last message timestamp
  "created_at": "datetime",       // Session creation timestamp
  "updated_at": "datetime",       // Last update timestamp
  "is_active": "boolean"          // Session status
}
```

### 5. **messages** Collection
Stores individual chat messages with AI responses.

```javascript
{
  "_id": ObjectId,
  "session_id": "string",         // Reference to chat_sessions
  "user_id": "ObjectId",          // Reference to users collection
  "message_type": "string",       // "user" or "agent"
  "content": "string",            // Message content
  "data": "object",               // Additional data (AI responses)
  "suggestions": ["string"],      // AI suggestions
  "timestamp": "datetime"         // Message timestamp
}
```

## 🔧 Setup Instructions

### 1. Install MongoDB

#### Option A: Local MongoDB Installation
```bash
# Windows (using Chocolatey)
choco install mongodb

# macOS (using Homebrew)
brew install mongodb-community

# Ubuntu/Debian
sudo apt-get install mongodb
```

#### Option B: Docker
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### Option C: MongoDB Atlas (Cloud)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get connection string

### 2. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create or update your `.env` file:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017

# GitHub API
GITHUB_TOKEN=your_github_token

# Hugging Face API
HF_TOKEN=your_huggingface_token

# Default Repository (for demo mode)
GITHUB_REPO=octocat/Hello-World
```

### 4. Run Setup Script
```bash
cd backend
python setup_mongodb.py
```

### 5. Start the Server
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Database Indexes

The following indexes are automatically created for optimal performance:

### users Collection
- `username` (unique)
- `email` (unique)
- `created_at`

### repositories Collection
- `user_id`
- `github_repo` (unique)
- `created_at`

### user_sessions Collection
- `user_id`
- `session_id` (unique)
- `created_at`

### chat_sessions Collection
- `user_id`
- `session_id` (unique)
- `created_at`

### messages Collection
- `session_id`
- `user_id`
- `timestamp`

## 🔌 API Endpoints

### Authentication
- `POST /register` - Create new user account
- `POST /login` - Authenticate user
- `POST /logout` - Logout user

### Chat & Messaging
- `POST /chat` - Send message (saves to MongoDB)
- `GET /chat/history` - Get chat history
- `POST /query` - Legacy endpoint (no auth)

### User Management
- `GET /user/profile` - Get user profile
- `GET /user/activity` - Get user activity summary
- `POST /update-github-repo` - Update repository

### Session Management
- `DELETE /session/{session_id}` - Delete session

### System & Health
- `GET /health` - Health check with DB status

### Admin Endpoints
- `GET /admin/users` - Get all users
- `GET /admin/analytics` - System analytics
- `GET /admin/db/health` - Database health

## 📈 Analytics & Reporting

The system provides comprehensive analytics:

### User Activity Summary
```json
{
  "user": {
    "username": "testuser",
    "email": "test@example.com",
    "github_repo": "octocat/Hello-World"
  },
  "sessions_count": 5,
  "messages_count": 25,
  "repositories_count": 1,
  "last_activity": "2024-01-15T10:30:00Z"
}
```

### System Analytics
```json
{
  "total_users": 10,
  "total_sessions": 25,
  "total_messages": 150,
  "total_repositories": 10,
  "recent_users": 2,
  "recent_messages": 15
}
```

## 🧪 Testing

Use the provided Postman collection: `github-ai-agent-mongodb.postman_collection.json`

### Test Flow:
1. Register a new user
2. Login and get session ID
3. Send chat messages
4. Retrieve chat history
5. Check user activity
6. Update repository
7. Logout

## 🔒 Security Considerations

### Production Recommendations:
1. **Password Hashing**: Use bcrypt or similar for password hashing
2. **MongoDB Authentication**: Enable MongoDB authentication
3. **Connection Security**: Use SSL/TLS for MongoDB connections
4. **Session Management**: Implement session expiration
5. **Input Validation**: Validate all user inputs
6. **Rate Limiting**: Implement API rate limiting

### Environment Variables for Production:
```env
MONGODB_URI=mongodb://username:password@host:port/database?authSource=admin&ssl=true
MONGODB_SSL_CERT_REQS=CERT_REQUIRED
```

## 🐛 Troubleshooting

### Common Issues:

1. **Connection Refused**
   - Ensure MongoDB is running
   - Check port 27017 is accessible
   - Verify firewall settings

2. **Authentication Failed**
   - Check MongoDB credentials
   - Verify database permissions
   - Ensure auth database is correct

3. **Index Creation Failed**
   - Check MongoDB user permissions
   - Ensure sufficient disk space
   - Verify MongoDB version compatibility

### Debug Commands:
```bash
# Test MongoDB connection
python -c "from database import db_service; print(db_service.health_check())"

# Check collections
python -c "from database import db_service; print(list(db_service.db.list_collection_names()))"

# View indexes
python -c "from database import db_service; print(db_service.users.index_information())"
```

## 📚 Additional Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Atlas](https://www.mongodb.com/atlas)

## 🤝 Contributing

When adding new features:
1. Update the database schema documentation
2. Add appropriate indexes
3. Include database migration scripts if needed
4. Update the Postman collection
5. Add tests for new endpoints 