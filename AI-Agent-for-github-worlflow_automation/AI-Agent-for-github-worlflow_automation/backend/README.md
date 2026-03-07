# GitHub AI Agent Backend

A conversational AI agent that helps manage GitHub repositories using natural language.

## Features

- **Conversational AI**: ChatGPT-like interface for GitHub operations
- **Session Management**: Remember conversation context across requests
- **Multi-Repository Support**: Work with different GitHub repositories
- **Natural Language Processing**: Understand and execute GitHub workflows
- **Smart Suggestions**: Context-aware action suggestions

## Setup

### 1. Environment Variables

Create a `.env` file in the backend directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# GitHub Configuration
GITHUB_TOKEN=ghp-your-github-personal-access-token-here
GITHUB_REPO=your-username/your-repository-name
```

### 2. Install Dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### 3. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST `/chat`
Main conversational endpoint for the AI agent.

**Request:**
```json
{
  "message": "Show me all open issues",
  "session_id": "optional-session-id",
  "github_repo": "owner/repo"
}
```

**Response:**
```json
{
  "session_id": "generated-session-id",
  "response": "I found 5 open issues in the repository...",
  "data": {...},
  "suggestions": ["Create a new issue", "Show pull requests"]
}
```

### POST `/query`
Legacy endpoint for backward compatibility.

**Request:**
```json
{
  "query": "Create a bug issue for login failure",
  "github_repo": "owner/repo"
}
```

### GET `/health`
Health check endpoint.

### DELETE `/session/{session_id}`
Delete a chat session.

## GitHub Operations Supported

- **Fetch Issues**: Get all issues from repository
- **Create Issues**: Create new issues with title and description
- **Fetch Pull Requests**: Get all pull requests
- **Add Comments**: Add comments to existing issues
- **Assign Users**: Assign users to issues
- **Update Issues**: Modify existing issues

## Example Usage

### Using Postman:

1. **Start a conversation:**
   ```
   POST http://localhost:8000/chat
   {
     "message": "Hello! Can you help me manage my GitHub repository?",
     "github_repo": "your-username/your-repo"
   }
   ```

2. **Ask about issues:**
   ```
   POST http://localhost:8000/chat
   {
     "message": "Show me all open issues",
     "session_id": "session-id-from-previous-response"
   }
   ```

3. **Create an issue:**
   ```
   POST http://localhost:8000/chat
   {
     "message": "Create a bug issue for the login page not working",
     "session_id": "session-id"
   }
   ```

## Error Handling

The agent handles errors gracefully and provides helpful suggestions for next actions. Common error scenarios:

- Missing environment variables
- Invalid GitHub tokens
- Repository access issues
- OpenAI API errors

## Development

The backend uses:
- **FastAPI**: Modern Python web framework
- **OpenAI GPT-3.5**: AI language model
- **GitHub REST API**: Repository operations
- **Session Management**: In-memory storage (use Redis for production) 