import requests
import re
from github_api import GitHubAPI
from typing import List, Dict, Any, Optional
import os
import json
from datetime import datetime
from database import db_service

class GitHubAIAgent:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = "https://api.github.com"
        
        # Bug type patterns for classification
        self.bug_patterns = {
            "syntax_error": [
                r"syntax error", r"SyntaxError", r"parsing error", r"invalid syntax",
                r"unexpected token", r"missing semicolon", r"unclosed bracket"
            ],
            "runtime_error": [
                r"runtime error", r"RuntimeError", r"TypeError", r"ValueError",
                r"IndexError", r"KeyError", r"AttributeError", r"NameError"
            ],
            "logic_error": [
                r"logic error", r"incorrect output", r"wrong result", r"unexpected behavior",
                r"not working as expected", r"bug in logic", r"calculation error"
            ],
            "performance_issue": [
                r"performance issue", r"slow", r"timeout", r"memory leak",
                r"high cpu usage", r"slow response", r"optimization needed"
            ],
            "security_vulnerability": [
                r"security", r"vulnerability", r"sql injection", r"xss",
                r"authentication", r"authorization", r"data breach"
            ],
            "ui_ux_issue": [
                r"ui issue", r"ux issue", r"interface problem", r"display error",
                r"layout issue", r"responsive design", r"user experience"
            ],
            "integration_issue": [
                r"integration", r"api error", r"connection failed", r"external service",
                r"third party", r"webhook", r"authentication failed"
            ],
            "deployment_issue": [
                r"deployment", r"build error", r"deploy failed", r"environment",
                r"configuration", r"server error", r"production issue"
            ]
        }
    
    def classify_bug_type(self, description: str, title: str = "") -> str:
        """Classify bug type based on description and title"""
        text = f"{title} {description}".lower()
        
        for bug_type, patterns in self.bug_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return bug_type
        
        return "general_issue"
    
    def determine_priority(self, description: str, title: str = "", labels: List[str] = None) -> int:
        """Determine bug priority (1=low, 2=medium, 3=high, 4=critical)"""
        text = f"{title} {description}".lower()
        labels = labels or []
        
        # Critical keywords
        critical_keywords = ["critical", "urgent", "security", "vulnerability", "data loss", "crash", "production down"]
        if any(keyword in text for keyword in critical_keywords) or "critical" in labels:
            return 4
        
        # High priority keywords
        high_keywords = ["high priority", "important", "blocking", "major", "severe", "broken"]
        if any(keyword in text for keyword in high_keywords) or "high" in labels:
            return 3
        
        # Medium priority keywords
        medium_keywords = ["medium", "moderate", "minor", "enhancement", "feature request"]
        if any(keyword in text for keyword in medium_keywords) or "medium" in labels:
            return 2
        
        return 1  # Default to low priority
    
    def extract_affected_components(self, description: str, title: str = "") -> List[str]:
        """Extract affected components from bug description"""
        text = f"{title} {description}"
        components = []
        
        # Common component regex patterns
        component_patterns = [
            r"in (\w+\.py|\w+\.js|\w+\.ts|\w+\.jsx|\w+\.tsx)",
            r"file (\w+\.\w+)",
            r"component (\w+)",
            r"module (\w+)",
            r"function (\w+)",
            r"class (\w+)",
            r"endpoint (\w+)",
            r"route (\w+)"
        ]
        
        for pattern in component_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            components.extend(matches)
        
        return list(set(components))  # Remove duplicates
    
    def create_github_issue(self, repo_owner: str, repo_name: str, title: str, description: str, 
                           labels: List[str] = None, assignees: List[str] = None) -> Dict[str, Any]:
        """Create a GitHub issue and track it in the database"""
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "title": title,
            "body": description,
            "labels": labels or []
        }
        
        if assignees:
            data["assignees"] = assignees
        
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues"
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            issue_data = response.json()
            
            # Track the bug in our database
            bug_data = {
                "github_issue_id": issue_data["id"],
                "github_issue_number": issue_data["number"],
                "github_url": issue_data["html_url"],
                "title": title,
                "description": description,
                "bug_type": self.classify_bug_type(description, title),
                "priority": self.determine_priority(description, title, labels),
                "affected_components": self.extract_affected_components(description, title),
                "labels": labels or [],
                "assignees": assignees or [],
                "status": "open",
                "github_repo": f"{repo_owner}/{repo_name}",
                "repo_owner": repo_owner,
                "repo_name": repo_name,
                "created_by_ai": True
            }
            
            return {
                "success": True,
                "issue": issue_data,
                "bug_data": bug_data
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def process_chat_message(self, message: str, user_id: str, session_id: str, github_repo: str = None) -> Dict[str, Any]:
        """Process chat message with GitHub operations first, AI for general conversation"""
        # First, check if this is a GitHub operation
        github_result = self._process_github_operations(message, user_id, session_id, github_repo)
        
        if github_result:
            # GitHub operation was detected and executed
            return github_result
        else:
            # No GitHub operation detected, use AI for general conversation
            try:
                ai_response = self._get_ai_response(message, github_repo)
                return {
                    "response": ai_response,
                    "operation_type": "ai_response"
                }
            except Exception as e:
                print(f"DEBUG: AI failed: {e}")
                return {
                    "response": "I'm sorry, I'm currently unable to process your request. Please try again later.",
                    "operation_type": "fallback"
                }
    
    def _process_github_operations(self, message: str, user_id: str, session_id: str, github_repo: str = None) -> Optional[Dict[str, Any]]:
        """Detect and execute GitHub operations based on user message"""
        message_lower = message.lower()
        
        print(f"DEBUG: Processing message: '{message}'")
        print(f"DEBUG: GitHub repo: {github_repo}")
        
        # Extract repository info if not provided
        if not github_repo:
            print("DEBUG: No github_repo provided, cannot execute GitHub operations")
            return None
        
        try:
            # Parse repository owner and name
            if '/' in github_repo:
                repo_owner, repo_name = github_repo.split('/', 1)
                print(f"DEBUG: Parsed repo - Owner: {repo_owner}, Name: {repo_name}")
            else:
                print("DEBUG: Invalid github_repo format")
                return None
            
            # Check for different GitHub operations with more flexible matching
            if any(keyword in message_lower for keyword in ["show", "list", "view", "all", "open", "issues", "bugs"]):
                print("DEBUG: Detected list issues operation")
                return self._handle_list_issues(repo_owner, repo_name, message_lower)
            
            elif any(keyword in message_lower for keyword in ["create", "report", "file", "submit", "bug", "issue"]):
                print("DEBUG: Detected create issue operation")
                return self._handle_create_issue(message, user_id, session_id, repo_owner, repo_name)
            
            elif any(keyword in message_lower for keyword in ["repo", "repository", "project", "about", "info"]):
                print("DEBUG: Detected repo info operation")
                return self._handle_repo_info(repo_owner, repo_name)
            
            elif any(keyword in message_lower for keyword in ["analysis", "statistics", "how many", "trends", "count"]):
                print("DEBUG: Detected bug analysis operation")
                return self._handle_bug_analysis(user_id, github_repo, message_lower)
            
            elif any(keyword in message_lower for keyword in ["close", "resolve", "fix"]):
                print("DEBUG: Detected close issues operation")
                return self._handle_close_issues(repo_owner, repo_name, message_lower)
            
            elif any(keyword in message_lower for keyword in ["help", "what can you do", "commands", "available"]):
                print("DEBUG: Detected help operation")
                return self._handle_help_request()
            
            # No GitHub operation detected
            print("DEBUG: No GitHub operation detected, will use AI")
            return None
            
        except Exception as e:
            print(f"Error in GitHub operations: {e}")
            return None
    
    def _handle_list_issues(self, repo_owner: str, repo_name: str, message_lower: str) -> Dict[str, Any]:
        """Handle listing issues"""
        state = "open"
        if "closed" in message_lower:
            state = "closed"
        
        issues = self.list_issues(repo_owner, repo_name, state)
        
        if isinstance(issues, list) and len(issues) > 0:
            issue_list = []
            for issue in issues[:10]:  # Limit to 10 issues
                issue_list.append({
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "state": issue.get("state"),
                    "url": issue.get("html_url")
                })
            
            response = f"Found {len(issues)} {state} issues in {repo_owner}/{repo_name}:\n\n"
            for issue in issue_list:
                response += f"#{issue['number']}: {issue['title']} ({issue['state']})\n"
                response += f"URL: {issue['url']}\n\n"
        else:
            response = f"No {state} issues found in {repo_owner}/{repo_name}."
        
        return {
            "response": response,
            "operation_type": "list_issues",
            "data": {"issues": issues[:10] if isinstance(issues, list) else []}
        }
    
    def _handle_create_issue(self, message: str, user_id: str, session_id: str, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Handle creating issues"""
        # Extract title and description from message
        title = self._extract_issue_title(message)
        description = self._extract_issue_description(message)
        
        if not title:
            title = "Bug Report"
        if not description:
            description = f"Bug reported via AI Agent: {message}"
        
        # Create the issue
        result = self.create_github_issue(repo_owner, repo_name, title, description)
        
        if result.get("success"):
            issue_data = result["issue"]
            bug_data = result["bug_data"]
            
            # Save to database
            saved_bug = db_service.create_bug(bug_data)
            
            response = f"✅ Issue created successfully!\n\n"
            response += f"**Title:** {title}\n"
            response += f"**Issue #:** {issue_data['number']}\n"
            response += f"**URL:** {issue_data['html_url']}\n"
            response += f"**Status:** {bug_data['status']}\n"
            response += f"**Priority:** {bug_data['priority']}\n"
            response += f"**Type:** {bug_data['bug_type']}"
            
            return {
                "response": response,
                "operation_type": "create_issue",
                "bug_created": True,
                "bug_data": saved_bug,
                "data": issue_data
            }
        else:
            return {
                "response": f"❌ Failed to create issue: {result.get('error', 'Unknown error')}",
                "operation_type": "create_issue",
                "bug_created": False,
                "bug_data": None
            }
    
    def _handle_repo_info(self, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Handle repository information requests"""
        repo_info = self.get_repository_info(repo_owner, repo_name)
        
        if "error" not in repo_info:
            response = f"📁 **Repository Information**\n\n"
            response += f"**Name:** {repo_info.get('name', 'N/A')}\n"
            response += f"**Owner:** {repo_info.get('owner', {}).get('login', 'N/A')}\n"
            response += f"**Description:** {repo_info.get('description', 'No description')}\n"
            response += f"**Language:** {repo_info.get('language', 'N/A')}\n"
            response += f"**Stars:** {repo_info.get('stargazers_count', 0)}\n"
            response += f"**Forks:** {repo_info.get('forks_count', 0)}\n"
            response += f"**Open Issues:** {repo_info.get('open_issues_count', 0)}\n"
            response += f"**URL:** {repo_info.get('html_url', 'N/A')}"
        else:
            response = f"❌ Error fetching repository information: {repo_info.get('error')}"
        
        return {
            "response": response,
            "operation_type": "repo_info",
            "data": repo_info
        }
    
    def _handle_bug_analysis(self, user_id: str, github_repo: str, message_lower: str) -> Dict[str, Any]:
        """Handle bug analysis requests"""
        # Extract time period
        time_period = self._extract_time_period(message_lower)
        
        # Get bugs from database
        bugs = db_service.get_bugs_by_repository(github_repo, limit=100)
        
        if bugs:
            analysis = self._perform_bug_analysis(bugs, time_period, "comprehensive")
            
            response = f"📊 **Bug Analysis Report**\n\n"
            response += f"**Repository:** {github_repo}\n"
            response += f"**Time Period:** {time_period.replace('_', ' ').title()}\n\n"
            
            if "summary" in analysis:
                summary = analysis["summary"]
                response += f"**Total Bugs:** {summary.get('total_bugs', 0)}\n"
                response += f"**Open Bugs:** {summary.get('open_bugs', 0)}\n"
                response += f"**Closed Bugs:** {summary.get('closed_bugs', 0)}\n"
                response += f"**Resolution Rate:** {summary.get('resolution_rate', 0):.1f}%\n\n"
            
            if "insights" in analysis:
                response += "**Key Insights:**\n"
                for insight in analysis["insights"][:3]:
                    response += f"• {insight}\n"
        else:
            response = f"No bug data found for {github_repo}."
        
        return {
            "response": response,
            "operation_type": "bug_analysis",
            "data": analysis if bugs else None
        }
    
    def _handle_close_issues(self, repo_owner: str, repo_name: str, message_lower: str) -> Dict[str, Any]:
        """Handle closing issues"""
        try:
            # Get all open issues
            open_issues = self.list_issues(repo_owner, repo_name, "open")
            
            if not isinstance(open_issues, list) or len(open_issues) == 0:
                return {
                    "response": f"No open issues found in {repo_owner}/{repo_name}.",
                    "operation_type": "close_issues",
                    "issues_closed": 0
                }
            
            # Close each open issue
            closed_count = 0
            failed_count = 0
            
            for issue in open_issues:
                try:
                    # Close the issue via GitHub API
                    headers = {
                        "Authorization": f"token {self.github_token}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                    
                    data = {"state": "closed"}
                    url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues/{issue['number']}"
                    
                    response = requests.patch(url, headers=headers, json=data)
                    
                    if response.status_code == 200:
                        closed_count += 1
                        print(f"DEBUG: Closed issue #{issue['number']}")
                    else:
                        failed_count += 1
                        print(f"DEBUG: Failed to close issue #{issue['number']}: {response.status_code}")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"DEBUG: Error closing issue #{issue['number']}: {e}")
            
            # Generate response
            if closed_count > 0:
                response = f"✅ Successfully closed {closed_count} open issues in {repo_owner}/{repo_name}."
                if failed_count > 0:
                    response += f"\n❌ Failed to close {failed_count} issues."
            else:
                response = f"❌ Failed to close any issues. {failed_count} issues could not be closed."
            
            return {
                "response": response,
                "operation_type": "close_issues",
                "issues_closed": closed_count,
                "issues_failed": failed_count
            }
            
        except Exception as e:
            print(f"DEBUG: Error in close issues operation: {e}")
            return {
                "response": f"❌ Error closing issues: {str(e)}",
                "operation_type": "close_issues",
                "issues_closed": 0
            }
    
    def _handle_help_request(self) -> Dict[str, Any]:
        """Handle help requests"""
        response = """🤖 **GitHub AI Agent - Available Commands**

**GitHub Operations:**
• "Show issues" or "List bugs" - View all open issues
• "Show closed issues" - View closed issues  
• "Create bug [description]" - Create a new issue
• "Close all issues" - Close all open issues
• "Repo info" - Get repository information
• "Bug analysis" - Get bug statistics and trends

**Examples:**
• "Show me all open issues"
• "Create a bug for login page not working"
• "Close all open issues"
• "How many bugs are open?"
• "Repository information"

**General:**
• Ask me anything about GitHub or your repository
• I can help with code, documentation, and best practices

Need help with something specific? Just ask!"""
        
        return {
            "response": response,
            "operation_type": "help"
        }
    
    def _extract_issue_title(self, message: str) -> str:
        """Extract issue title from message"""
        # Simple extraction - look for patterns like "for X" or "about X"
        import re
        
        # Look for "for [something]" or "about [something]"
        patterns = [
            r"for\s+([^.!?]+)",
            r"about\s+([^.!?]+)", 
            r"regarding\s+([^.!?]+)",
            r"bug\s+in\s+([^.!?]+)",
            r"issue\s+with\s+([^.!?]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if len(title) > 5:  # Minimum length
                    return title
        
        return ""
    
    def _extract_issue_description(self, message: str) -> str:
        """Extract issue description from message"""
        # Remove common prefixes and return the rest as description
        prefixes = [
            "create bug", "create issue", "report bug", "file bug", 
            "submit issue", "bug report", "issue report"
        ]
        
        description = message
        for prefix in prefixes:
            if description.lower().startswith(prefix):
                description = description[len(prefix):].strip()
                break
        
        return description if description else "Issue reported via AI Agent"
    
    def _get_ai_response(self, message: str, github_repo: str = None) -> str:
        """Get AI response using OpenAI only"""
        if self.openai_api_key:
            try:
                return self._get_openai_response(message, github_repo)
            except Exception as e:
                print(f"OpenAI API error: {e}")
        return "I'm sorry, I'm currently unable to process your request. Please try again later."
    
    def _get_openai_response(self, message: str, github_repo: str = None) -> str:
        """Get response from OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        context = f"You are a helpful AI assistant for managing GitHub repositories. "
        if github_repo:
            context += f"The current repository is: {github_repo}. "
        
        context += "You can help with creating issues, analyzing code, and providing guidance on repository management."
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def _get_huggingface_response(self, message: str, github_repo: str = None) -> str:
        """Get response from Hugging Face API"""
        headers = {
            "Authorization": f"Bearer {self.huggingface_api_key}",
            "Content-Type": "application/json"
        }
        
        context = f"Context: You are a helpful AI assistant for managing GitHub repositories. "
        if github_repo:
            context += f"Current repository: {github_repo}. "
        
        context += "You can help with creating issues, analyzing code, and providing guidance."
        
        full_prompt = f"{context}\n\nUser: {message}\n\nAssistant:"
        
        data = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        response = requests.post(
            "https://api-inference.huggingface.co/models/philippelaban/keep_it_simple",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0]["generated_text"].split("Assistant:")[-1].strip()
        
        return "I'm sorry, I couldn't generate a response at the moment."
    
    def get_repository_info(self, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Get repository information"""
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def list_issues(self, repo_owner: str, repo_name: str, state: str = "open") -> List[Dict[str, Any]]:
        """List issues in a repository"""
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues"
        params = {"state": state}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return [{"error": str(e)}]

# Legacy function for backward compatibility
async def process_query(user_query: str, github_token: str, openai_key: str):
    agent = GitHubAIAgent()
    response = await agent.process_chat_message(user_query, "", "")
    return response 
