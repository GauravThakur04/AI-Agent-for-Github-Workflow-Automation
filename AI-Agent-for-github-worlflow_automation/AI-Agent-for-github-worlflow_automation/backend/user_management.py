import os
import re
from datetime import datetime
from typing import Dict, Optional, List
from database import db_service

class UserManager:
    def __init__(self):
        self.db = db_service
    
    def _validate_github_url(self, github_url: str) -> tuple[bool, str, str]:
        """Validate GitHub URL and extract username/repo"""
        # Regex Patterns for GitHub URLs
        patterns = [
            r'https?://github\.com/([^/]+)/([^/]+)',
            r'https?://www\.github\.com/([^/]+)/([^/]+)',
            r'github\.com/([^/]+)/([^/]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, github_url)
            if match:
                username = match.group(1)
                repo_name = match.group(2).split('?')[0].split('#')[0]  # Remove query params
                return True, username, repo_name
        
        return False, "", ""
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def create_user(self, username: str, email: str, password: str, github_url: str) -> Dict:
        """Create a new user account"""
        # Validate inputs
        if not username or len(username) < 3:
            return {"success": False, "error": "Username must be at least 3 characters long"}
        
        if not self._validate_email(email):
            return {"success": False, "error": "Invalid email format"}
        
        if len(password) < 6:
            return {"success": False, "error": "Password must be at least 6 characters long"}
        
        # Validate GitHub URL
        is_valid, github_username, repo_name = self._validate_github_url(github_url)
        if not is_valid:
            return {"success": False, "error": "Invalid GitHub repository URL. Please provide a valid GitHub repository URL (e.g., https://github.com/username/repository)"}
        
        # Check if username or email already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            return {"success": False, "error": "Username already exists"}
        
        existing_email = self.db.get_user_by_email(email)
        if existing_email:
            return {"success": False, "error": "Email already registered"}

        # Check if GitHub repository is already registered
        github_repo_name = f"{github_username}/{repo_name}"
        existing_repo = self.db.get_repository_by_github_repo(github_repo_name)
        if existing_repo:
            return {"success": False, "error": f"GitHub repository '{github_repo_name}' is already registered by another user"}
        
        # Create new user
        user_data = {
            "username": username,
            "email": email,
            "password": password,  # In production, hash this password
            "github_url": github_url,
            "github_username": github_username,
            "github_repo": f"{github_username}/{repo_name}",
            "is_active": True
        }
        
        created_user = self.db.create_user(user_data)
        
        # Create repository record
        repo_data = {
            "user_id": created_user["_id"],
            "github_url": github_url,
            "github_username": github_username,
            "github_repo": f"{github_username}/{repo_name}",
            "is_primary": True
        }
        
        try:
            self.db.create_repository(repo_data)
        except Exception as e:
            # If repository creation fails (e.g. race condition), we should probably rollback user creation
            # or at least log it. For now, we'll return an error but the user is created.
            # Ideally we would delete the user here.
            self.db.users.delete_one({"_id": created_user["_id"]}) # Rollback
            return {"success": False, "error": f"Failed to register repository: {str(e)}"}
        
        return {
            "success": True,
            "user_id": created_user["_id"],
            "message": "Account created successfully!",
            "github_repo": created_user["github_repo"]
        }
    
    def authenticate_user(self, username: str, password: str) -> Dict:
        """Authenticate user login"""
        user = self.db.get_user_by_username(username)
        
        if user and user["password"] == password:
            if not user["is_active"]:
                return {"success": False, "error": "Account is deactivated"}
            
            # Update last login
            self.db.update_user_last_login(user["_id"])
            
            return {
                "success": True,
                "user_id": user["_id"],
                "username": user["username"],
                "github_repo": user["github_repo"],
                "message": "Login successful!"
            }
        
        return {"success": False, "error": "Invalid username or password"}
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user data by user ID"""
        return self.db.get_user_by_id(user_id)
    
    def update_user_github_repo(self, user_id: str, github_url: str) -> Dict:
        """Update user's GitHub repository"""
        user = self.db.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        # Validate GitHub URL
        is_valid, github_username, repo_name = self._validate_github_url(github_url)
        if not is_valid:
            return {"success": False, "error": "Invalid GitHub repository URL"}
        
        # Update user data
        self.db.update_user_github_repo(user_id, github_url, github_username, f"{github_username}/{repo_name}")
        
        # Update or create repository record
        repo_data = {
            "user_id": user_id,
            "github_url": github_url,
            "github_username": github_username,
            "github_repo": f"{github_username}/{repo_name}",
            "is_primary": True
        }
        
        # Check if user already has a primary repository
        existing_repos = self.db.get_repositories_by_user(user_id)
        primary_repo = next((repo for repo in existing_repos if repo.get("is_primary")), None)
        
        if primary_repo:
            # Update existing primary repository
            self.db.update_repository(primary_repo["_id"], repo_data)
        else:
            # Create new repository record
            self.db.create_repository(repo_data)
        
        return {
            "success": True,
            "message": "GitHub repository updated successfully!",
            "github_repo": f"{github_username}/{repo_name}"
        }
    
    def deactivate_user(self, user_id: str) -> Dict:
        """Deactivate user account"""
        user = self.db.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        self.db.deactivate_user(user_id)
        self.db.deactivate_user_sessions(user_id)
        
        return {"success": True, "message": "Account deactivated successfully"}
    
    def get_all_users(self) -> List[Dict]:
        """Get all users (for admin purposes)"""
        return self.db.get_all_users()
    
    def get_user_activity(self, user_id: str) -> Dict:
        """Get user activity summary"""
        return self.db.get_user_activity_summary(user_id)
