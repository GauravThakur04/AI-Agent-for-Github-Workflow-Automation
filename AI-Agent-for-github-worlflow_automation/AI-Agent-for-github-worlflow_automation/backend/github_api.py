# Placeholder for GitHub API helper functions 

import httpx
import os

class GitHubAPI:
    def __init__(self, repo: str = "octocat/Hello-World"):
        self.repo = repo
        self.github_api = 'https://api.github.com'

    def _get_headers(self, token: str):
        """Get headers for GitHub API requests"""
        return {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github+json'
        }

    def fetch_issues(self, token: str):
        """Fetch all issues from the repository"""
        headers = self._get_headers(token)
        url = f'{self.github_api}/repos/{self.repo}/issues'
        resp = httpx.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def create_issue(self, token: str, title: str, body: str = ""):
        """Create a new issue"""
        headers = self._get_headers(token)
        url = f'{self.github_api}/repos/{self.repo}/issues'
        data = {'title': title, 'body': body}
        resp = httpx.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def fetch_prs(self, token: str):
        """Fetch all pull requests from the repository"""
        headers = self._get_headers(token)
        url = f'{self.github_api}/repos/{self.repo}/pulls'
        resp = httpx.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def add_comment(self, token: str, issue_number: int, comment: str):
        """Add a comment to an issue"""
        headers = self._get_headers(token)
        url = f'{self.github_api}/repos/{self.repo}/issues/{issue_number}/comments'
        data = {'body': comment}
        resp = httpx.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def assign_user(self, token: str, issue_number: int, assignee: str):
        """Assign a user to an issue"""
        headers = self._get_headers(token)
        url = f'{self.github_api}/repos/{self.repo}/issues/{issue_number}/assignees'
        data = {'assignees': [assignee]}
        resp = httpx.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_issue(self, token: str, issue_number: int):
        """Get a specific issue by number"""
        headers = self._get_headers(token)
        url = f'{self.github_api}/repos/{self.repo}/issues/{issue_number}'
        resp = httpx.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def update_issue(self, token: str, issue_number: int, **kwargs):
        """Update an issue with new data"""
        headers = self._get_headers(token)
        url = f'{self.github_api}/repos/{self.repo}/issues/{issue_number}'
        resp = httpx.patch(url, headers=headers, json=kwargs)
        resp.raise_for_status()
        return resp.json()

    def get_repo_info(self, token: str):
        """Get repository information"""
        headers = self._get_headers(token)
        url = f'{self.github_api}/repos/{self.repo}'
        resp = httpx.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

# Legacy function for backward compatibility
REPO = os.getenv('GITHUB_REPO', 'octocat/Hello-World')

def fetch_issues(token):
    """Legacy function for backward compatibility"""
    api = GitHubAPI(REPO)
    return api.fetch_issues(token)

def create_issue(token, title, body):
    """Legacy function for backward compatibility"""
    api = GitHubAPI(REPO)
    return api.create_issue(token, title, body)

def fetch_prs(token):
    """Legacy function for backward compatibility"""
    api = GitHubAPI(REPO)
    return api.fetch_prs(token) 
