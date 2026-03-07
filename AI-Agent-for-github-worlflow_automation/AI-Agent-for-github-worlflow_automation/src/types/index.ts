export interface GitHubRepo {
  id: number;
  name: string;
  full_name: string;
  owner: {
    login: string;
    avatar_url: string;
  };
  description: string;
  private: boolean;
  html_url: string;
}

export interface GitHubIssue {
  id: number;
  number: number;
  title: string;
  body: string;
  state: 'open' | 'closed';
  user: {
    login: string;
    avatar_url: string;
  };
  labels: Array<{
    id: number;
    name: string;
    color: string;
  }>;
  assignees: Array<{
    login: string;
    avatar_url: string;
  }>;
  created_at: string;
  updated_at: string;
  html_url: string;
}

export interface GitHubPR {
  id: number;
  number: number;
  title: string;
  body: string;
  state: 'open' | 'closed' | 'merged';
  user: {
    login: string;
    avatar_url: string;
  };
  created_at: string;
  updated_at: string;
  html_url: string;
  draft: boolean;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'agent';
  content: string;
  timestamp: Date;
  loading?: boolean;
  data?: any;
  suggestions?: string[];
}

export interface AgentAction {
  type: 'create_issue' | 'update_issue' | 'fetch_issues' | 'fetch_prs' | 'add_comment' | 'general_query';
  parameters: Record<string, any>;
  result?: any;
  error?: string;
}

export interface User {
  sessionId: string;
  username: string;
  githubRepo: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  session_id?: string;
  user_id?: string;
  username?: string;
  github_repo?: string;
  error?: string;
}