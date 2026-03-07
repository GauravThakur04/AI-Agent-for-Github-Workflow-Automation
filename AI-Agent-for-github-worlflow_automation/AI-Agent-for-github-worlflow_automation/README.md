#  AI Agent for GitHub Workflow Automation

An intelligent conversational AI agent that enables natural language interaction with GitHub repositories. Built with React/TypeScript frontend and FastAPI backend, this project allows users to manage GitHub issues, pull requests, and repository workflows through simple conversational commands.

##  Features

### Core Capabilities
- **Conversational AI Interface**: ChatGPT-like interface for GitHub operations
- **Natural Language Processing**: Understand and execute GitHub workflows in plain English
- **Bug Analytics & Tracking**: Comprehensive bug detection, classification, and analytics
- **User Management**: Multi-user support with session management
- **Advanced Analytics**: Bug trends, assignment analysis, and team workload distribution
- **MongoDB Integration**: Persistent data storage for users, sessions, and analytics
- **Smart Suggestions**: Context-aware action suggestions based on conversation history
- **Multi-Repository Support**: Work with different GitHub repositories seamlessly

### GitHub Operations Supported
- ✅ **Fetch Issues**: Get all issues from repository with filtering
- ✅ **Create Issues**: Create new issues with automatic bug classification
- ✅ **Update Issues**: Modify existing issues
- ✅ **Fetch Pull Requests**: Get all pull requests
- ✅ **Add Comments**: Add comments to existing issues
- ✅ **Assign Users**: Assign users to issues
- ✅ **Bug Classification**: Automatic categorization by type (syntax, runtime, logic, performance, security, UI/UX, integration)
- ✅ **Priority Assignment**: Intelligent priority level assignment (1-4 scale)

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │   Backend API   │    │   GitHub API    │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│   Integration   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   AI Agent      │
                       │   Core Engine   │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Intent Analysis │
                       │ & NLP Pipeline  │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   MongoDB       │
                       │   Database      │
                       └─────────────────┘
```

## Tech Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI GPT** - AI language model for natural language understanding
- **GitHub REST API** - Repository operations
- **MongoDB** - Database for user data, sessions, and analytics
- **AutoGen** - Agentic framework
- **Python 3.8+** - Programming language

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) and **npm**
- **Python** (3.8 or higher)
- **MongoDB** (local installation or MongoDB Atlas account)
- **Git**
- **OpenAI API Key** - Get one from [OpenAI](https://platform.openai.com/)
- **GitHub Personal Access Token** - Create one at [GitHub Settings](https://github.com/settings/tokens) with `repo` scope

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Agent-for-github-worlflow_automation
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to project root
cd ..

# Install dependencies
npm install
```

### 4. MongoDB Setup

Choose one of the following options:

#### Option A: Local MongoDB
```bash
# Install MongoDB locally
# Windows: Download from mongodb.com
# Mac: brew install mongodb
# Linux: sudo apt-get install mongodb
```

#### Option B: Docker
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### Option C: MongoDB Atlas (Cloud)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get connection string

See [MONGODB_SETUP.md](./backend/MONGODB_SETUP.md) for detailed instructions.

### 5. Run MongoDB Setup Script

```bash
cd backend
python setup_mongodb.py
```

## Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# GitHub Configuration
GITHUB_TOKEN=ghp-your-github-personal-access-token-here
GITHUB_REPO=your-username/your-repository-name

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017

# Hugging Face API (Optional)
HUGGINGFACE_API_KEY=your-huggingface-token-here
```

**Note**: Copy `backend/.env.example` to `backend/.env` and fill in your values.

### Frontend Configuration

The frontend automatically connects to `http://localhost:8000` by default. To change this, modify the API base URL in `src/hooks/useAIAgent.ts`.

## 🎯 Usage

### Starting the Application

#### 1. Start MongoDB (if using local installation)
```bash
# Windows: Start MongoDB service
# Mac/Linux: mongod
```

#### 2. Start Backend Server

```bash
cd backend
# Activate virtual environment first
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

#### 3. Start Frontend Development Server

```bash
# From project root
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Using the Application

1. **Open the Application**: Navigate to `http://localhost:5173` in your browser
2. **Register/Login**: Create an account or login with existing credentials
3. **Connect GitHub**: Provide your GitHub Personal Access Token and repository
4. **Start Chatting**: Use natural language to interact with your GitHub repository

### Example Queries

- "Show me all open issues"
- "Create a bug issue for the login page not working"
- "What pull requests are pending review?"
- "Add a comment to issue #5 saying 'Working on it'"
- "Show me bug statistics for the last month"
- "Who is assigned to the most bugs?"

## API Documentation

### Main Endpoints

#### POST `/chat`
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

#### POST `/register`
Register a new user.

**Request:**
```json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password",
  "github_url": "https://github.com/owner/repo"
}
```

#### POST `/login`
Authenticate user.

**Request:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

#### GET `/health`
Health check endpoint with database status.

#### GET `/bugs/list`
List bugs with optional filtering.

**Query Parameters:**
- `session_id` (required)
- `status` (optional): `open`, `closed`, `in_progress`, etc.
- `priority` (optional): `1`, `2`, `3`, `4`
- `bug_type` (optional): `syntax_error`, `runtime_error`, etc.

#### POST `/bugs/create`
Create a new bug issue.

**Request:**
```json
{
  "title": "Bug Title",
  "description": "Bug Description",
  "bug_type": "ui_ux",
  "priority": 2,
  "assignees": ["username"]
}
```

For complete API documentation, see:
- [Backend README](./backend/README.md)
- [Postman Setup Guide](./postman_setup_guide.md)
- [Bug Analytics Features](./BUG_ANALYTICS_FEATURES.md)

##  Project Structure

```
AI-Agent-for-github-worlflow_automation/
├── backend/                    # Backend API (FastAPI)
│   ├── __pycache__/           # Python cache
│   ├── agent.py               # AI Agent core logic
│   ├── database.py            # MongoDB database service
│   ├── github_api.py          # GitHub API integration
│   ├── main.py                # FastAPI application entry point
│   ├── user_management.py     # User authentication & management
│   ├── setup_mongodb.py       # MongoDB setup script
│   ├── project_documentation.py
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── users.json.example     # User data template
│   ├── README.md              # Backend documentation
│   └── MONGODB_SETUP.md       # MongoDB setup guide
│
├── src/                        # Frontend source (React/TypeScript)
│   ├── components/            # React components
│   │   ├── AuthModal.tsx     # Authentication modal
│   │   ├── ChatInterface.tsx  # Main chat interface
│   │   ├── ConnectionModal.tsx # GitHub connection modal
│   │   ├── Header.tsx         # Application header
│   │   └── MessageBubble.tsx # Chat message component
│   ├── hooks/                 # Custom React hooks
│   │   ├── useAIAgent.ts     # AI agent hook
│   │   └── useGitHubAPI.ts   # GitHub API hook
│   ├── types/                 # TypeScript type definitions
│   │   └── index.ts
│   ├── App.tsx               # Main application component
│   ├── main.tsx              # Application entry point
│   └── index.css             # Global styles
│
├── .gitignore                 # Git ignore rules
├── package.json              # Frontend dependencies
├── vite.config.ts            # Vite configuration
├── tailwind.config.js        # Tailwind CSS configuration
├── tsconfig.json             # TypeScript configuration
│
├── README.md                  # This file
├── Agent_Architecture_Design_Report.md
├── BUG_ANALYTICS_FEATURES.md
├── BUG_TRACKING_DOCUMENTATION.md
├── postman_setup_guide.md
├── TREND_REPORT_TESTING_GUIDE.md
│
└── *.postman_collection.json  # Postman API collections
```

##  Features in Detail

### Bug Analytics & Tracking

The system includes comprehensive bug analytics features:

- **Time-based Analytics**: Analyze bugs by time periods (last week, month, 3 months, year)
- **Trend Analysis**: Daily bug creation trends and patterns
- **Priority Distribution**: Visual breakdown of bugs by priority level
- **Type Classification**: Automatic categorization of bug types
- **Assignment Analytics**: Team workload distribution and assignment analysis
- **Resolution Metrics**: Average resolution time and resolution rates

See [BUG_ANALYTICS_FEATURES.md](./BUG_ANALYTICS_FEATURES.md) for detailed documentation.

### Bug Classification Types

- **Syntax Error**: Code syntax issues
- **Runtime Error**: Execution-time errors
- **Logic Error**: Incorrect program logic
- **Performance Issue**: Speed and optimization problems
- **Security Vulnerability**: Security-related issues
- **UI/UX Issue**: User interface problems
- **Integration Issue**: Third-party integration problems

### Session Management

- Persistent conversation history
- Multi-session support per user
- Context preservation across requests
- Session cleanup and management

##  Testing

### Using Postman

Import the provided Postman collections:
- `github-ai-agent-postman-collection.json`
- `github-ai-agent-bug-analytics.postman_collection.json`
- `github-ai-agent-user-management.postman_collection.json`
- `github-ai-agent-mongodb.postman_collection.json`

See [postman_setup_guide.md](./postman_setup_guide.md) for detailed instructions.

### Manual Testing

1. Test health endpoint: `GET http://localhost:8000/health`
2. Register a new user
3. Login and get session ID
4. Test chat endpoint with various queries
5. Verify bug creation and analytics

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write clear commit messages
- Add documentation for new features
- Test your changes before submitting

##  License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Additional Resources

- [Backend Documentation](./backend/README.md)
- [MongoDB Setup Guide](./backend/MONGODB_SETUP.md)
- [Agent Architecture Design](./Agent_Architecture_Design_Report.md)
- [Bug Tracking Documentation](./BUG_TRACKING_DOCUMENTATION.md)
- [Postman Setup Guide](./postman_setup_guide.md)

##  Important Notes

### Security

- **Never commit sensitive files**: The `.gitignore` is configured to exclude:
  - `.env` files
  - Service account keys (`*-*-*.json`)
  - User data files (`users.json`)
  - Python cache files (`__pycache__/`)

- **Rotate exposed credentials**: If any credentials were accidentally committed, rotate them immediately.

- **Use environment variables**: Always use `.env` files for configuration, never hardcode secrets.

### Environment Variables

Always use the `.env.example` template and never commit actual `.env` files to version control.

##  Troubleshooting

### Backend Issues

- **Connection Refused**: Ensure MongoDB is running and `MONGODB_URI` is correct
- **401 Unauthorized**: Verify your GitHub token has proper scopes
- **OpenAI API Errors**: Check your API key and account credits

### Frontend Issues

- **Cannot connect to backend**: Verify backend is running on port 8000
- **Build errors**: Run `npm install` to ensure all dependencies are installed

### MongoDB Issues

- **Connection timeout**: Check MongoDB service status
- **Authentication failed**: Verify connection string credentials

##  Support

For issues, questions, or contributions, please open an issue on GitHub.

---


