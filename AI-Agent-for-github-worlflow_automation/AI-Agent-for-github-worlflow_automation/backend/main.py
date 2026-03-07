from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from agent import GitHubAIAgent
from user_management import UserManager
from database import db_service
import os
from dotenv import load_dotenv
from typing import Dict, List
import uuid
from dotenv import load_dotenv
import os
from nlp.bug_classifier import classify_issue
from nlp.summarizer import summarize_issue
from analytics.bug_stats import get_bug_stats # type: ignore
from analytics import get_bug_stats, get_workflow_stats
import os



load_dotenv()

github_token= os.getenv("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")

load_dotenv()

app = FastAPI(title="GitHub AI Agent", description="AI-powered GitHub workflow automation agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize user manager and database service
user_manager = UserManager()

@app.post("/register")
async def register_user(request: Request):
    """Register a new user account"""
    data = await request.json()
    
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    github_url = data.get("github_url", "").strip()

    
@app.post("/analyze_issue")
def analyze_issue(text: str):

    result = classify_issue(text)

    return result



@app.post("/summarize_issue")
def summarize(text: str):

    summary = summarize_issue(text)

    return {"summary": summary}
    
    # Validate required fields
    if not all([username, email, password, github_url]):
        raise HTTPException(status_code=400, detail="All fields are required")
    
    # Create user account
    result = user_manager.create_user(username, email, password, github_url)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "success": True,
        "message": result["message"],
        "user_id": result["user_id"],
        "github_repo": result["github_repo"]
    }

@app.post("/login")
async def login_user(request: Request):
    """Authenticate user login"""
    data = await request.json()
    
    username = data.get("username", "").strip()
    password = data.get("password", "")
    
    if not username or not password:
        raise HTTPException(status_code=401, detail="Username and password are required")
    
    # Authenticate user
    result = user_manager.authenticate_user(username, password)
    
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])
    
    # Create session for the user
    session_id = str(uuid.uuid4())
    
    # Store session in database
    session_data = {
        "session_id": session_id,
        "user_id": result["user_id"],
        "username": result["username"],
        "github_repo": result["github_repo"],
        "is_active": True
    }
    db_service.create_user_session(session_data)
    
    # Create chat session
    chat_session_data = {
        "session_id": session_id,
        "user_id": result["user_id"],
        "github_repo": result["github_repo"],
        "is_active": True
    }
    db_service.create_chat_session(chat_session_data)
    
    return {
        "success": True,
        "message": result["message"],
        "session_id": session_id,
        "user_id": result["user_id"],
        "username": result["username"],
        "github_repo": result["github_repo"]
    }

@app.post("/chat")
async def chat(request: Request):
    """Main chat endpoint for conversational AI agent"""
    data = await request.json()
    user_message = data.get("message", "")
    session_id = data.get("session_id")
    
    # Validate session
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID is required")
    
    # Get session from database
    session = db_service.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please login again.")
    
    user_id = session["user_id"]
    github_repo = session["github_repo"]
    
    # Create AI agent for this user's repository
    agent = GitHubAIAgent()
    
    # Process the message
    response = agent.process_chat_message(user_message, user_id, session_id, github_repo)
    
    # Save user message to database
    user_message_data = {
        "session_id": session_id,
        "user_id": user_id,
        "message_type": "user",
        "content": user_message,
        "timestamp": None  # Will be set by database service
    }
    db_service.save_message(user_message_data)
    
    # Save AI response to database
    ai_message_data = {
        "session_id": session_id,
        "user_id": user_id,
        "message_type": "agent",
        "content": response["response"],
        "data": response.get("data"),
        "suggestions": response.get("suggestions", []),
        "timestamp": None  # Will be set by database service
    }
    db_service.save_message(ai_message_data)
    
    # Update chat session
    db_service.update_chat_session(session_id, {
        "last_message_at": None,  # Will be set by database service
        "message_count": db_service.messages.count_documents({"session_id": session_id})
    })
    
    return {
        "session_id": session_id,
        "response": response["response"],
        "data": response.get("data"),
        "suggestions": response.get("suggestions", []),
        "bug_created": response.get("bug_created", False),
        "bug_data": response.get("bug_data")
    }

@app.post("/update-github-repo")
async def update_github_repository(request: Request):
    """Update user's GitHub repository"""
    data = await request.json()
    session_id = data.get("session_id")
    github_url = data.get("github_url", "").strip()
    
    # Validate session
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID is required")
    
    session = db_service.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please login again.")
    
    if not github_url:
        raise HTTPException(status_code=400, detail="GitHub URL is required")
    
    # Get user ID and update repository
    user_id = session["user_id"]
    result = user_manager.update_user_github_repo(user_id, github_url)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Update session with new repository
    db_service.update_chat_session(session_id, {
        "github_repo": result["github_repo"]
    })
    
    return {
        "success": True,
        "message": result["message"],
        "github_repo": result["github_repo"]
    }

@app.get("/user/profile")
async def get_user_profile(session_id: str):
    """Get user profile information"""
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID is required")
    
    session = db_service.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please login again.")
    
    user_id = session["user_id"]
    user = db_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove sensitive information
    user.pop("password", None)
    
    return {
        "success": True,
        "user": user,
        "github_repo": session["github_repo"]
    }

@app.get("/user/activity")
async def get_user_activity(session_id: str):
    """Get user activity summary"""
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID is required")
    
    session = db_service.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please login again.")
    
    user_id = session["user_id"]
    activity_summary = db_service.get_user_activity_summary(user_id)
    
    if not activity_summary:
        raise HTTPException(status_code=404, detail="User activity not found")
    
    return {
        "success": True,
        "activity": activity_summary
    }

@app.get("/chat/history")
async def get_chat_history(session_id: str, limit: int = 50):
    """Get chat history for a session"""
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID is required")
    
    session = db_service.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please login again.")
    
    messages = db_service.get_session_messages(session_id, limit)
    
    return {
        "success": True,
        "messages": messages,
        "session_id": session_id
    }

@app.post("/logout")
async def logout_user(request: Request):
    """Logout user and deactivate session"""
    data = await request.json()
    session_id = data.get("session_id")
    
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")
    
    # Deactivate session
    db_service.deactivate_session(session_id)
    
    return {
        "success": True,
        "message": "Successfully logged out"
    }

@app.post("/query")
async def query(request: Request):
    """Legacy query endpoint for backward compatibility"""
    data = await request.json()
    user_query = data.get("query", "")
    github_token = data.get("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", "")
    openai_key = data.get("openai_key", "")
    
    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    # Use the new agent system
    agent = GitHubAIAgent()
    response = agent.process_chat_message(user_query, "", "", "")
    
    return {
        "response": response["response"],
        "data": response.get("data", {})
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GitHub AI Agent",
        "version": "1.0.0"
    }

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a specific session"""
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")
    
    db_service.deactivate_session(session_id)
    
    return {
        "success": True,
        "message": "Session deleted successfully"
    }

@app.get("/admin/users")
async def get_all_users():
    """Get all users (admin only)"""
    users = db_service.get_all_users()
    return {
        "success": True,
        "users": users,
        "count": len(users)
    }

@app.get("/admin/analytics")
async def get_system_analytics():
    """Get system-wide analytics"""
    analytics = db_service.get_system_analytics()
    return {
        "success": True,
        "analytics": analytics
    }

@app.get("/admin/db/health")
async def get_database_health():
    """Get database health status"""
    health = db_service.health_check()
    return {
        "success": True,
        "health": health
    }

# Bug Tracking Endpoints
@app.get("/bugs/user")
async def get_user_bugs(session_id: str, limit: int = 50):
    """Get all bugs created by the current user"""
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID is required")
    
    session = db_service.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please login again.")
    
    user_id = session["user_id"]
    bugs = db_service.get_bugs_by_user(user_id, limit)
    
    return {
        "success": True,
        "bugs": bugs,
        "count": len(bugs)
    }

@app.get("/bugs/session/{session_id}")
async def get_session_bugs(session_id: str):
    """Get all bugs from a specific session"""
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")
    
    bugs = db_service.get_bugs_by_session(session_id)
    
    return {
        "success": True,
        "bugs": bugs,
        "count": len(bugs)
    }

@app.get("/bugs/repository/{github_repo}")
async def get_repository_bugs(github_repo: str):
    """Get all bugs for a specific repository"""
    if not github_repo:
        raise HTTPException(status_code=400, detail="GitHub repository is required")
    
    bugs = db_service.get_bugs_by_repository(github_repo)
    
    return {
        "success": True,
        "bugs": bugs,
        "count": len(bugs)
    }
@app.get("/bug_stats")
def bug_stats():

    owner = "GauravThakur04"
    repo = "Complaint-Management-System"

    token = os.getenv("GITHUB_TOKEN")

    stats = get_bug_stats(owner, repo, token)

    return stats

@app.get("/bugs/statistics")
async def get_bug_statistics(session_id: str = None):
    """Get bug statistics for a user or system-wide"""
    if session_id:
        # Get user-specific statistics
        session = db_service.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid or expired session. Please login again.")
        
        user_id = session["user_id"]
        stats = db_service.get_bug_statistics(user_id)
    else:
        # Get system-wide statistics
        stats = db_service.get_bug_statistics()
    
    return {
        "success": True,
        "statistics": stats
    }

@app.get("/bugs/types")
async def get_bug_types():
    """Get available bug types and their descriptions"""
    bug_types = {
        "syntax_error": "Code syntax errors, parsing issues, invalid syntax",
        "runtime_error": "Runtime exceptions, type errors, attribute errors",
        "logic_error": "Incorrect logic, wrong calculations, unexpected behavior",
        "performance_issue": "Slow performance, memory leaks, optimization needed",
        "security_vulnerability": "Security issues, authentication problems, data breaches",
        "ui_ux_issue": "User interface problems, display errors, UX issues",
        "integration_issue": "API integration problems, external service issues",
        "deployment_issue": "Build errors, deployment failures, environment issues",
        "general_issue": "General bugs that don't fit other categories"
    }
    
    return {
        "success": True,
        "bug_types": bug_types
    }

@app.get("/bugs/priorities")
async def get_bug_priorities():
    """Get bug priority levels and their descriptions"""
    priorities = {
        1: "Low - Minor issues, cosmetic problems, nice-to-have features",
        2: "Medium - Moderate issues, some impact on functionality",
        3: "High - Important issues, significant impact on functionality",
        4: "Critical - Urgent issues, security vulnerabilities, system crashes"
    }
    
    return {
        "success": True,
        "priorities": priorities
    }

@app.put("/bugs/{bug_id}/status")
async def update_bug_status(bug_id: str, request: Request):
    """Update bug status"""
    data = await request.json()
    status = data.get("status")
    notes = data.get("notes")
    
    if not status:
        raise HTTPException(status_code=400, detail="Status is required")
    
    if status not in ["open", "in_progress", "resolved", "closed", "wont_fix"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be one of: open, in_progress, resolved, closed, wont_fix")
    
    db_service.update_bug_status(bug_id, status, notes)
    
    return {
        "success": True,
        "message": f"Bug status updated to {status}",
        "bug_id": bug_id,
        "status": status
    }

@app.get("/bugs/{bug_id}")
async def get_bug_details(bug_id: str):
    """Get detailed information about a specific bug"""
    # This would need to be implemented in the database service
    # For now, we'll return a placeholder
    return {
        "success": True,
        "message": "Bug details endpoint - to be implemented",
        "bug_id": bug_id
    }

@app.post("/bugs/create")
async def create_bug(bug_data: dict, session_id: str = Query(...)):
    """Create a new bug"""
    try:
        # Validate session
        session = db_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        user_id = session.get("user_id")
        github_repo = session.get("github_repo")
        
        if not github_repo:
            raise HTTPException(status_code=400, detail="GitHub repository not configured")
        
        # Create bug
        bug_id = db_service.create_bug(
            user_id=user_id,
            github_repo=github_repo,
            title=bug_data.get("title"),
            description=bug_data.get("description"),
            bug_type=bug_data.get("bug_type", "general_issue"),
            priority=bug_data.get("priority", 1),
            assignees=bug_data.get("assignees", [])
        )
        
        return {"message": "Bug created successfully", "bug_id": str(bug_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bugs/list")
async def list_bugs(session_id: str = Query(...), status: str = Query(None)):
    """List bugs for a user"""
    try:
        # Validate session
        session = db_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        user_id = session.get("user_id")
        github_repo = session.get("github_repo")
        
        # Get bugs
        bugs = db_service.get_bugs(user_id=user_id, github_repo=github_repo, status=status)
        return {"bugs": bugs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/bugs/{bug_id}")
async def update_bug(bug_id: str, update_data: dict, session_id: str = Query(...)):
    """Update a bug"""
    try:
        # Validate session
        session = db_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        # Update bug
        success = db_service.update_bug(bug_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail="Bug not found")
        
        return {"message": "Bug updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bugs/analytics")
async def get_bug_analytics(
    session_id: str = Query(...),
    time_period: str = Query("all_time"),
    analysis_type: str = Query("open_bugs")
):
 
    """Get bug analytics and statistics"""
    try:
        # Validate session
        session = db_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        user_id = session.get("user_id")
        github_repo = session.get("github_repo")
        
        # Get analytics
        analytics = db_service.get_bug_analytics(
            user_id=user_id,
            github_repo=github_repo,
            time_period=time_period,
            analysis_type=analysis_type
        )
        
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bugs/assignment-analytics")
async def get_assignment_analytics(session_id: str = Query(...)):
    """Get assignment analytics and statistics"""
    try:
        # Validate session
        session = db_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        user_id = session.get("user_id")
        github_repo = session.get("github_repo")
        
        # Get assignment analytics
        analytics = db_service.get_assignment_analytics(
            user_id=user_id,
            github_repo=github_repo
        )
        
        return analytics
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
    @app.get("/")
    async def home():
        return {"message": "AI Agent Backend Running"}

    
    
    @app.get("/bugs/types")
    async def get_bug_types():
        """Get available bug types"""
    return {
        "bug_types": [
            "general_issue",
            "bug",
            "feature_request", 
            "enhancement",
            "documentation",
            "performance",
            "security",
            "ui_ux",
            "backend",
            "frontend",
            "database",
            "api",
            "testing",
            "deployment"
        ]
        
    } 