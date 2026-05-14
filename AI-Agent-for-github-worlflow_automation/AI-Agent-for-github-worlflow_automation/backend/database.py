import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
import json

class MongoDBService:
    def __init__(self):
        # Get MongoDB connection string from environment or use default configs
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.client = MongoClient(mongo_uri)
        self.db: Database = self.client.github_ai_agent
        
        # Collections
        self.users: Collection = self.db.users
        self.repositories: Collection = self.db.repositories
        self.chat_sessions: Collection = self.db.chat_sessions
        self.messages: Collection = self.db.messages
        self.user_sessions: Collection = self.db.user_sessions
        self.bugs: Collection = self.db.bugs  # New collection for bug tracking
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for better query performance"""
        # Users collection indexes
        self.users.create_index("username", unique=True)
        self.users.create_index("email", unique=True)
        self.users.create_index("created_at")
        
        # Repositories collection indexes
        self.repositories.create_index("user_id")
        self.repositories.create_index("github_repo", unique=True)
        self.repositories.create_index("created_at")
        
        # Chat sessions collection indexes
        self.chat_sessions.create_index("user_id")
        self.chat_sessions.create_index("session_id", unique=True)
        self.chat_sessions.create_index("created_at")
        
        # Messages collection indexes
        self.messages.create_index("session_id")
        self.messages.create_index("user_id")
        self.messages.create_index("timestamp")
        
        # User sessions collection indexes
        self.user_sessions.create_index("session_id", unique=True)
        self.user_sessions.create_index("user_id")
        self.user_sessions.create_index("created_at")
        
        # Bugs collection indexes
        self.bugs.create_index("user_id")
        self.bugs.create_index("session_id")
        self.bugs.create_index("github_repo")
        self.bugs.create_index("bug_type")
        self.bugs.create_index("status")
        self.bugs.create_index("created_at")
        self.bugs.create_index("priority")
    
    # User Management Methods
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        user_data["created_at"] = datetime.now()
        user_data["updated_at"] = datetime.now()
        user_data["is_active"] = True
        
        result = self.users.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        
        return user_data
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        user = self.users.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
        return user
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        user = self.users.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            user = self.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except:
            return None
    
    def update_user_last_login(self, user_id: str):
        """Update user's last login time"""
        self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_login": datetime.now(), "updated_at": datetime.now()}}
        )
    
    def update_user_github_repo(self, user_id: str, github_url: str, github_username: str, github_repo: str):
        """Update user's GitHub repository information"""
        self.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "github_url": github_url,
                    "github_username": github_username,
                    "github_repo": github_repo,
                    "updated_at": datetime.now()
                }
            }
        )
    
    def deactivate_user(self, user_id: str):
        """Deactivate user account"""
        self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": False, "updated_at": datetime.now()}}
        )
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (for admin purposes)"""
        users = list(self.users.find({}, {"password": 0}))  # Exclude password
        for user in users:
            user["_id"] = str(user["_id"])
        return users
    
    # Repository Management Methods
    def create_repository(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new repository record"""
        repo_data["created_at"] = datetime.now()
        repo_data["updated_at"] = datetime.now()
        
        result = self.repositories.insert_one(repo_data)
        repo_data["_id"] = str(result.inserted_id)
        
        return repo_data
    
    def get_repositories_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all repositories for a user"""
        repos = list(self.repositories.find({"user_id": user_id}))
        for repo in repos:
            repo["_id"] = str(repo["_id"])
        return repos
    
    def get_repository_by_github_repo(self, github_repo: str) -> Optional[Dict[str, Any]]:
        """Get repository by GitHub repo name (e.g., 'username/repo')"""
        repo = self.repositories.find_one({"github_repo": github_repo})
        if repo:
            repo["_id"] = str(repo["_id"])
        return repo

    def update_repository(self, repo_id: str, update_data: Dict[str, Any]):
        """Update repository information"""
        update_data["updated_at"] = datetime.now()
        self.repositories.update_one(
            {"_id": ObjectId(repo_id)},
            {"$set": update_data}
        )
    
    # Session Management Methods
    def create_user_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user session"""
        session_data["created_at"] = datetime.now()
        session_data["updated_at"] = datetime.now()
        session_data["is_active"] = True
        
        result = self.user_sessions.insert_one(session_data)
        session_data["_id"] = str(result.inserted_id)
        
        return session_data
    
    def get_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by session ID"""
        session = self.user_sessions.find_one({"session_id": session_id, "is_active": True})
        if session:
            session["_id"] = str(session["_id"])
        return session
    
    def get_user_id_by_session(self, session_id: str) -> Optional[str]:
        """Get user ID from session ID"""
        session = self.get_session_by_id(session_id)
        return session.get("user_id") if session else None
    
    def deactivate_session(self, session_id: str):
        """Deactivate a session"""
        self.user_sessions.update_one(
            {"session_id": session_id},
            {"$set": {"is_active": False, "updated_at": datetime.now()}}
        )
    
    def deactivate_user_sessions(self, user_id: str):
        """Deactivate all sessions for a user"""
        self.user_sessions.update_many(
            {"user_id": user_id},
            {"$set": {"is_active": False, "updated_at": datetime.now()}}
        )
    
    # Chat Session Management Methods
    def create_chat_session(self, chat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new chat session"""
        chat_data["created_at"] = datetime.now()
        chat_data["updated_at"] = datetime.now()
        chat_data["is_active"] = True
        
        result = self.chat_sessions.insert_one(chat_data)
        chat_data["_id"] = str(result.inserted_id)
        
        return chat_data
    
    def get_chat_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get chat session by session ID"""
        session = self.chat_sessions.find_one({"session_id": session_id, "is_active": True})
        if session:
            session["_id"] = str(session["_id"])
        return session
    
    def update_chat_session(self, session_id: str, update_data: Dict[str, Any]):
        """Update chat session"""
        update_data["updated_at"] = datetime.now()
        self.chat_sessions.update_one(
            {"session_id": session_id},
            {"$set": update_data}
        )
    
    def get_user_chat_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all chat sessions for a user"""
        sessions = list(self.chat_sessions.find({"user_id": user_id, "is_active": True}))
        for session in sessions:
            session["_id"] = str(session["_id"])
        return sessions
    
    # Message Management Methods
    def save_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a chat message"""
        message_data["timestamp"] = datetime.now()
        
        result = self.messages.insert_one(message_data)
        message_data["_id"] = str(result.inserted_id)
        
        return message_data
    
    def get_session_messages(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get messages for a specific session"""
        messages = list(self.messages.find(
            {"session_id": session_id}
        ).sort("timestamp", 1).limit(limit))
        
        for message in messages:
            message["_id"] = str(message["_id"])
        return messages
    
    def get_user_messages(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all messages for a user"""
        messages = list(self.messages.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit))
        
        for message in messages:
            message["_id"] = str(message["_id"])
        return messages
    
    # Bug Tracking Methods
    def create_bug(self, bug_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new bug/issue record"""
        bug_data["created_at"] = datetime.now()
        bug_data["updated_at"] = datetime.now()
        bug_data["status"] = bug_data.get("status", "open")
        
        result = self.bugs.insert_one(bug_data)
        bug_data["_id"] = str(result.inserted_id)
        
        return bug_data
    
    def get_bugs_by_user(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all bugs created by a user"""
        bugs = list(self.bugs.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit))
        
        for bug in bugs:
            bug["_id"] = str(bug["_id"])
        return bugs
    
    def get_bugs_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all bugs from a specific session"""
        bugs = list(self.bugs.find({"session_id": session_id}).sort("created_at", -1))
        
        for bug in bugs:
            bug["_id"] = str(bug["_id"])
        return bugs
    
    def get_bugs_by_repository(self, github_repo: str) -> List[Dict[str, Any]]:
        """Get all bugs for a specific repository"""
        bugs = list(self.bugs.find({"github_repo": github_repo}).sort("created_at", -1))
        
        for bug in bugs:
            bug["_id"] = str(bug["_id"])
        return bugs
    
    def update_bug_status(self, bug_id: str, status: str, notes: str = None):
        """Update bug status"""
        update_data = {
            "status": status,
            "updated_at": datetime.now()
        }
        if notes:
            update_data["notes"] = notes
        
        self.bugs.update_one(
            {"_id": ObjectId(bug_id)},
            {"$set": update_data}
        )
    
    def get_bug_statistics(self, user_id: str = None) -> Dict[str, Any]:
        """Get bug statistics"""
        match_filter = {}
        if user_id:
            match_filter["user_id"] = user_id
        
        pipeline = [
            {"$match": match_filter},
            {"$group": {
                "_id": "$bug_type",
                "count": {"$sum": 1},
                "avg_priority": {"$avg": "$priority"}
            }},
            {"$sort": {"count": -1}}
        ]
        
        type_stats = list(self.bugs.aggregate(pipeline))
        
        # Get status distribution
        status_pipeline = [
            {"$match": match_filter},
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        
        status_stats = list(self.bugs.aggregate(status_pipeline))
        
        # Get total counts
        total_bugs = self.bugs.count_documents(match_filter)
        open_bugs = self.bugs.count_documents({**match_filter, "status": "open"})
        closed_bugs = self.bugs.count_documents({**match_filter, "status": "closed"})
        
        return {
            "total_bugs": total_bugs,
            "open_bugs": open_bugs,
            "closed_bugs": closed_bugs,
            "by_type": type_stats,
            "by_status": status_stats
        }
    
    # Analytics and Reporting Methods
    def get_user_activity_summary(self, user_id: str) -> Dict[str, Any]:
        """Get user activity summary"""
        # Get user info
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Get chat sessions count
        sessions_count = self.chat_sessions.count_documents({"user_id": user_id, "is_active": True})
        
        # Get messages count
        messages_count = self.messages.count_documents({"user_id": user_id})
        
        # Get repositories count
        repos_count = self.repositories.count_documents({"user_id": user_id})
        
        # Get bugs count
        bugs_count = self.bugs.count_documents({"user_id": user_id})
        
        # Get last activity
        last_message = self.messages.find_one(
            {"user_id": user_id},
            sort=[("timestamp", -1)]
        )
        
        # Get bug statistics
        bug_stats = self.get_bug_statistics(user_id)
        
        return {
            "user": user,
            "sessions_count": sessions_count,
            "messages_count": messages_count,
            "repositories_count": repos_count,
            "bugs_count": bugs_count,
            "last_activity": last_message["timestamp"] if last_message else None,
            "bug_statistics": bug_stats
        }
    
    def get_system_analytics(self) -> Dict[str, Any]:
        """Get system-wide analytics"""
        total_users = self.users.count_documents({"is_active": True})
        total_sessions = self.chat_sessions.count_documents({"is_active": True})
        total_messages = self.messages.count_documents({})
        total_repositories = self.repositories.count_documents({})
        total_bugs = self.bugs.count_documents({})
        
        # Get recent activity (last 24 hours)
        yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        recent_users = self.users.count_documents({"created_at": {"$gte": yesterday}})
        recent_messages = self.messages.count_documents({"timestamp": {"$gte": yesterday}})
        recent_bugs = self.bugs.count_documents({"created_at": {"$gte": yesterday}})
        
        # Get bug statistics
        bug_stats = self.get_bug_statistics()
        
        return {
            "total_users": total_users,
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "total_repositories": total_repositories,
            "total_bugs": total_bugs,
            "recent_users": recent_users,
            "recent_messages": recent_messages,
            "recent_bugs": recent_bugs,
            "bug_statistics": bug_stats
        }
    
    # Database Health and Maintenance
    def health_check(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            # Test connection
            self.client.admin.command('ping')
            
            # Get database stats
            stats = self.db.command("dbStats")
            
            return {
                "status": "healthy",
                "database": self.db.name,
                "collections": stats["collections"],
                "data_size": stats["dataSize"],
                "storage_size": stats["storageSize"]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def close_connection(self):
        """Close database connection"""
        self.client.close()

    def get_bugs(self, user_id: str = None, github_repo: str = None, status: str = None) -> List[Dict[str, Any]]:
        """Get bugs with optional filters"""
        try:
            query = {}
            
            if user_id:
                query["user_id"] = user_id
            if github_repo:
                query["github_repo"] = github_repo
            if status:
                query["status"] = status
            
            bugs = list(self.bugs.find(query).sort("created_at", -1))
            
            # Convert ObjectId to string
            for bug in bugs:
                bug["_id"] = str(bug["_id"])
            
            return bugs
        except Exception as e:
            print(f"Error getting bugs: {e}")
            return []
    
    def update_bug(self, bug_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a bug"""
        try:
            from bson import ObjectId
            
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.now().isoformat()
            
            result = self.bugs.update_one(
                {"_id": ObjectId(bug_id)},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating bug: {e}")
            return False
    
    def get_bug_analytics(self, user_id: str = None, github_repo: str = None, 
                         time_period: str = "all_time", analysis_type: str = "open_bugs") -> Dict[str, Any]:
        """Get bug analytics and statistics"""
        try:
            from datetime import datetime, timedelta
            
            # Calculate date range
            end_date = datetime.now()
            if time_period == "last_week":
                start_date = end_date - timedelta(days=7)
            elif time_period == "last_2_weeks":
                start_date = end_date - timedelta(days=14)
            elif time_period == "last_month":
                start_date = end_date - timedelta(days=30)
            elif time_period == "last_3_months":
                start_date = end_date - timedelta(days=90)
            elif time_period == "last_year":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = datetime(2020, 1, 1)  # Default to all time
            
            # Build query filter
            query_filter = {
                "created_at": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
            
            # Add user filter if specific user
            if user_id:
                query_filter["user_id"] = user_id
            
            # Add repository filter if specific repo
            if github_repo:
                query_filter["github_repo"] = github_repo
            
            # Get bugs from database
            bugs = list(self.bugs.find(query_filter).sort("created_at", -1))
            
            # Convert ObjectId to string
            for bug in bugs:
                bug["_id"] = str(bug["_id"])
            
            # Perform analysis
            analysis_result = self._perform_bug_analysis(bugs, time_period, analysis_type)
            
            # Generate trend report
            trend_report = self._generate_trend_report(bugs, time_period)
            
            return {
                "time_period": time_period,
                "analysis_type": analysis_type,
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "total_bugs": len(bugs),
                "analysis": analysis_result,
                "trend_report": trend_report
            }
            
        except Exception as e:
            print(f"Error in bug analytics: {e}")
            return {"error": str(e)}
    
    def _perform_bug_analysis(self, bugs: List[Dict[str, Any]], time_period: str, analysis_type: str) -> Dict[str, Any]:
        """Perform detailed bug analysis"""
        if not bugs:
            return {
                "message": f"No bugs found for {time_period}",
                "summary": {}
            }
        
        # Basic statistics
        total_bugs = len(bugs)
        open_bugs = len([b for b in bugs if b.get("status") == "open"])
        closed_bugs = len([b for b in bugs if b.get("status") in ["closed", "resolved"]])
        
        # Priority distribution
        priority_distribution = {}
        for bug in bugs:
            priority = bug.get("priority", 1)
            priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
        
        # Bug type distribution
        type_distribution = {}
        for bug in bugs:
            bug_type = bug.get("bug_type", "general_issue")
            type_distribution[bug_type] = type_distribution.get(bug_type, 0) + 1
        
        # Status distribution
        status_distribution = {}
        for bug in bugs:
            status = bug.get("status", "open")
            status_distribution[status] = status_distribution.get(status, 0) + 1
        
        # Daily trend (last 7 days)
        daily_trend = {}
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_bugs = [b for b in bugs if b.get("created_at", "").startswith(date)]
            daily_trend[date] = len(daily_bugs)
        
        # Average resolution time (for closed bugs)
        resolution_times = []
        for bug in bugs:
            if bug.get("status") in ["closed", "resolved"] and bug.get("created_at") and bug.get("updated_at"):
                try:
                    created = datetime.fromisoformat(bug["created_at"].replace("Z", "+00:00"))
                    updated = datetime.fromisoformat(bug["updated_at"].replace("Z", "+00:00"))
                    resolution_time = (updated - created).days
                    resolution_times.append(resolution_time)
                except:
                    pass
        
        avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0
        
        return {
            "summary": {
                "total_bugs": total_bugs,
                "open_bugs": open_bugs,
                "closed_bugs": closed_bugs,
                "resolution_rate": (closed_bugs / total_bugs * 100) if total_bugs > 0 else 0,
                "avg_resolution_time_days": round(avg_resolution_time, 1)
            },
            "priority_distribution": priority_distribution,
            "type_distribution": type_distribution,
            "status_distribution": status_distribution,
            "daily_trend": daily_trend,
            "time_period": time_period
        }
    
    def _generate_trend_report(self, bugs: List[Dict[str, Any]], time_period: str) -> Dict[str, Any]:
        """Generate comprehensive trend report based on bug data"""
        if not bugs:
            return {
                "message": f"No bugs found for {time_period} trend analysis",
                "trends": {}
            }
        
        from datetime import datetime, timedelta
        
        # Calculate trend periods
        end_date = datetime.now()
        if time_period == "last_week":
            period_days = 7
            interval = "daily"
        elif time_period == "last_2_weeks":
            period_days = 14
            interval = "daily"
        elif time_period == "last_month":
            period_days = 30
            interval = "weekly"
        elif time_period == "last_3_months":
            period_days = 90
            interval = "weekly"
        elif time_period == "last_year":
            period_days = 365
            interval = "monthly"
        else:
            period_days = 30
            interval = "weekly"
        
        # Generate time series data
        time_series = self._generate_time_series(bugs, end_date, period_days, interval)
        
        # Calculate trend metrics
        trend_metrics = self._calculate_trend_metrics(time_series)
        
        # Generate insights
        insights = self._generate_trend_insights(trend_metrics, bugs, time_period)
        
        # Performance indicators
        performance_indicators = self._calculate_performance_indicators(bugs, time_period)
        
        return {
            "time_period": time_period,
            "interval": interval,
            "time_series": time_series,
            "trend_metrics": trend_metrics,
            "insights": insights,
            "performance_indicators": performance_indicators,
            "recommendations": self._generate_recommendations(trend_metrics, insights)
        }
    
    def _generate_time_series(self, bugs: List[Dict[str, Any]], end_date: datetime, 
                            period_days: int, interval: str) -> Dict[str, Any]:
        """Generate time series data for trend analysis"""
        time_series = {
            "bug_creation": {},
            "bug_resolution": {},
            "priority_distribution": {},
            "type_distribution": {},
            "status_distribution": {}
        }
        
        if interval == "daily":
            for i in range(period_days):
                date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
                time_series["bug_creation"][date] = 0
                time_series["bug_resolution"][date] = 0
                time_series["priority_distribution"][date] = {"1": 0, "2": 0, "3": 0, "4": 0}
                time_series["type_distribution"][date] = {}
                time_series["status_distribution"][date] = {"open": 0, "closed": 0, "resolved": 0}
        
        elif interval == "weekly":
            for i in range(period_days // 7):
                week_start = (end_date - timedelta(weeks=i+1)).strftime("%Y-W%U")
                week_end = (end_date - timedelta(weeks=i)).strftime("%Y-W%U")
                week_key = f"{week_start} to {week_end}"
                time_series["bug_creation"][week_key] = 0
                time_series["bug_resolution"][week_key] = 0
                time_series["priority_distribution"][week_key] = {"1": 0, "2": 0, "3": 0, "4": 0}
                time_series["type_distribution"][week_key] = {}
                time_series["status_distribution"][week_key] = {"open": 0, "closed": 0, "resolved": 0}
        
        elif interval == "monthly":
            for i in range(period_days // 30):
                month = (end_date - timedelta(days=30*(i+1))).strftime("%Y-%m")
                time_series["bug_creation"][month] = 0
                time_series["bug_resolution"][month] = 0
                time_series["priority_distribution"][month] = {"1": 0, "2": 0, "3": 0, "4": 0}
                time_series["type_distribution"][month] = {}
                time_series["status_distribution"][month] = {"open": 0, "closed": 0, "resolved": 0}
        
        # Populate time series with actual data
        for bug in bugs:
            created_date = bug.get("created_at")
            if created_date:
                if isinstance(created_date, str):
                    created_date = datetime.fromisoformat(created_date.replace("Z", "+00:00"))
                
                if interval == "daily":
                    date_key = created_date.strftime("%Y-%m-%d")
                elif interval == "weekly":
                    week_num = created_date.isocalendar()[1]
                    date_key = f"{created_date.year}-W{week_num:02d}"
                else:  # monthly
                    date_key = created_date.strftime("%Y-%m")
                
                if date_key in time_series["bug_creation"]:
                    time_series["bug_creation"][date_key] += 1
                    
                    # Priority distribution
                    priority = str(bug.get("priority", 1))
                    if priority in time_series["priority_distribution"][date_key]:
                        time_series["priority_distribution"][date_key][priority] += 1
                    
                    # Type distribution
                    bug_type = bug.get("bug_type", "general_issue")
                    if bug_type not in time_series["type_distribution"][date_key]:
                        time_series["type_distribution"][date_key][bug_type] = 0
                    time_series["type_distribution"][date_key][bug_type] += 1
                    
                    # Status distribution
                    status = bug.get("status", "open")
                    if status in time_series["status_distribution"][date_key]:
                        time_series["status_distribution"][date_key][status] += 1
        
        return time_series
    
    def _calculate_trend_metrics(self, time_series: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate trend metrics from time series data"""
        bug_creation = time_series["bug_creation"]
        creation_values = list(bug_creation.values())
        
        if not creation_values:
            return {"error": "No data available for trend calculation"}
        
        # Basic statistics
        total_bugs = sum(creation_values)
        avg_bugs_per_period = total_bugs / len(creation_values) if creation_values else 0
        max_bugs_period = max(creation_values)
        min_bugs_period = min(creation_values)
        
        # Trend direction
        if len(creation_values) >= 2:
            recent_avg = sum(creation_values[:len(creation_values)//2]) / (len(creation_values)//2)
            older_avg = sum(creation_values[len(creation_values)//2:]) / (len(creation_values)//2)
            
            if recent_avg > older_avg * 1.1:
                trend_direction = "increasing"
                trend_strength = "strong" if recent_avg > older_avg * 1.5 else "moderate"
            elif recent_avg < older_avg * 0.9:
                trend_direction = "decreasing"
                trend_strength = "strong" if recent_avg < older_avg * 0.5 else "moderate"
            else:
                trend_direction = "stable"
                trend_strength = "weak"
        else:
            trend_direction = "insufficient_data"
            trend_strength = "unknown"
        
        # Volatility
        if len(creation_values) > 1:
            mean = sum(creation_values) / len(creation_values)
            variance = sum((x - mean) ** 2 for x in creation_values) / len(creation_values)
            volatility = variance ** 0.5
        else:
            volatility = 0
        
        return {
            "total_bugs": total_bugs,
            "avg_bugs_per_period": round(avg_bugs_per_period, 2),
            "max_bugs_period": max_bugs_period,
            "min_bugs_period": min_bugs_period,
            "trend_direction": trend_direction,
            "trend_strength": trend_strength,
            "volatility": round(volatility, 2),
            "periods_analyzed": len(creation_values)
        }
    
    def _generate_trend_insights(self, trend_metrics: Dict[str, Any], bugs: List[Dict[str, Any]], 
                               time_period: str) -> List[str]:
        """Generate insights from trend analysis"""
        insights = []
        
        # Trend direction insights
        if trend_metrics.get("trend_direction") == "increasing":
            insights.append(f"Bug creation is trending upward over the {time_period}, indicating potential quality issues or increased development activity.")
        elif trend_metrics.get("trend_direction") == "decreasing":
            insights.append(f"Bug creation is trending downward over the {time_period}, suggesting improved code quality or reduced development activity.")
        else:
            insights.append(f"Bug creation remains stable over the {time_period}.")
        
        # Volatility insights
        volatility = trend_metrics.get("volatility", 0)
        if volatility > trend_metrics.get("avg_bugs_per_period", 0) * 0.5:
            insights.append("High volatility in bug creation suggests inconsistent development patterns or varying project phases.")
        
        # Priority insights
        priority_counts = {}
        for bug in bugs:
            priority = bug.get("priority", 1)
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        if priority_counts.get(4, 0) > 0:
            insights.append(f"Critical bugs detected: {priority_counts[4]} critical issues require immediate attention.")
        
        if priority_counts.get(3, 0) > priority_counts.get(1, 0):
            insights.append("High-priority bugs outnumber low-priority ones, indicating significant quality concerns.")
        
        # Type insights
        type_counts = {}
        for bug in bugs:
            bug_type = bug.get("bug_type", "general_issue")
            type_counts[bug_type] = type_counts.get(bug_type, 0) + 1
        
        most_common_type = max(type_counts.items(), key=lambda x: x[1]) if type_counts else None
        if most_common_type:
            insights.append(f"Most common bug type: {most_common_type[0]} ({most_common_type[1]} instances)")
        
        return insights
    
    def _calculate_performance_indicators(self, bugs: List[Dict[str, Any]], time_period: str) -> Dict[str, Any]:
        """Calculate performance indicators"""
        if not bugs:
            return {"error": "No bugs available for performance analysis"}
        
        # Resolution time analysis
        resolution_times = []
        for bug in bugs:
            if bug.get("status") in ["closed", "resolved"] and bug.get("created_at") and bug.get("updated_at"):
                try:
                    created = datetime.fromisoformat(bug["created_at"].replace("Z", "+00:00"))
                    updated = datetime.fromisoformat(bug["updated_at"].replace("Z", "+00:00"))
                    resolution_time = (updated - created).days
                    resolution_times.append(resolution_time)
                except:
                    pass
        
        avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0
        
        # Status distribution
        status_counts = {}
        for bug in bugs:
            status = bug.get("status", "open")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total_bugs = len(bugs)
        open_bugs = status_counts.get("open", 0)
        closed_bugs = status_counts.get("closed", 0) + status_counts.get("resolved", 0)
        
        resolution_rate = (closed_bugs / total_bugs * 100) if total_bugs > 0 else 0
        
        return {
            "avg_resolution_time_days": round(avg_resolution_time, 1),
            "resolution_rate_percent": round(resolution_rate, 2),
            "open_bugs_count": open_bugs,
            "closed_bugs_count": closed_bugs,
            "total_bugs_count": total_bugs,
            "status_distribution": status_counts
        }
    
    def _generate_recommendations(self, trend_metrics: Dict[str, Any], insights: List[str]) -> List[str]:
        """Generate actionable recommendations based on trends"""
        recommendations = []
        
        trend_direction = trend_metrics.get("trend_direction")
        trend_strength = trend_metrics.get("trend_strength")
        
        if trend_direction == "increasing" and trend_strength in ["strong", "moderate"]:
            recommendations.append("Consider implementing additional code review processes to catch issues earlier.")
            recommendations.append("Review recent changes that may have introduced quality issues.")
            recommendations.append("Consider increasing testing coverage for new features.")
        
        elif trend_direction == "decreasing" and trend_strength in ["strong", "moderate"]:
            recommendations.append("Maintain current quality practices as they appear effective.")
            recommendations.append("Consider documenting successful practices for team knowledge sharing.")
        
        volatility = trend_metrics.get("volatility", 0)
        if volatility > trend_metrics.get("avg_bugs_per_period", 0) * 0.5:
            recommendations.append("Implement consistent development practices to reduce volatility.")
            recommendations.append("Consider establishing regular code quality checkpoints.")
        
        return recommendations

# Global database instance
db_service = MongoDBService()
