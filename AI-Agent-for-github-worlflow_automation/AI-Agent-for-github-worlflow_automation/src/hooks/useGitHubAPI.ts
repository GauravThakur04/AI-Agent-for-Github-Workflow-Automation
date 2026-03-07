import { useState, useCallback } from 'react';
import { GitHubRepo, GitHubIssue, GitHubPR } from '../types';

// Mock data for demonstration
const mockRepos: GitHubRepo[] = [
  {
    id: 1,
    name: 'awesome-project',
    full_name: 'user/awesome-project',
    owner: {
      login: 'user',
      avatar_url: 'https://images.pexels.com/photos/1040881/pexels-photo-1040881.jpeg?auto=compress&cs=tinysrgb&w=40&h=40&fit=crop'
    },
    description: 'An awesome project for demonstration',
    private: false,
    html_url: 'https://github.com/user/awesome-project'
  }
];

const mockIssues: GitHubIssue[] = [
  {
    id: 1,
    number: 123,
    title: 'Login failure on mobile devices',
    body: 'Users are experiencing login failures specifically on mobile devices...',
    state: 'open',
    user: {
      login: 'user',
      avatar_url: 'https://images.pexels.com/photos/1040881/pexels-photo-1040881.jpeg?auto=compress&cs=tinysrgb&w=40&h=40&fit=crop'
    },
    labels: [
      { id: 1, name: 'bug', color: 'd73a49' },
      { id: 2, name: 'mobile', color: '0075ca' }
    ],
    assignees: [],
    created_at: '2025-01-15T10:00:00Z',
    updated_at: '2025-01-15T10:00:00Z',
    html_url: 'https://github.com/user/awesome-project/issues/123'
  },
  {
    id: 2,
    number: 124,
    title: 'Add dark mode support',
    body: 'Implement dark mode for better user experience...',
    state: 'open',
    user: {
      login: 'designer',
      avatar_url: 'https://images.pexels.com/photos/1374510/pexels-photo-1374510.jpeg?auto=compress&cs=tinysrgb&w=40&h=40&fit=crop'
    },
    labels: [
      { id: 3, name: 'enhancement', color: 'a2eeef' },
      { id: 4, name: 'ui/ux', color: 'fbca04' }
    ],
    assignees: [
      {
        login: 'developer',
        avatar_url: 'https://images.pexels.com/photos/1043474/pexels-photo-1043474.jpeg?auto=compress&cs=tinysrgb&w=40&h=40&fit=crop'
      }
    ],
    created_at: '2025-01-14T15:30:00Z',
    updated_at: '2025-01-14T15:30:00Z',
    html_url: 'https://github.com/user/awesome-project/issues/124'
  }
];

const mockPRs: GitHubPR[] = [
  {
    id: 1,
    number: 45,
    title: 'Fix authentication bug',
    body: 'This PR fixes the authentication bug reported in #123...',
    state: 'open',
    user: {
      login: 'developer',
      avatar_url: 'https://images.pexels.com/photos/1043474/pexels-photo-1043474.jpeg?auto=compress&cs=tinysrgb&w=40&h=40&fit=crop'
    },
    created_at: '2025-01-15T14:00:00Z',
    updated_at: '2025-01-15T16:00:00Z',
    html_url: 'https://github.com/user/awesome-project/pull/45',
    draft: false
  }
];

export const useGitHubAPI = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [currentRepo, setCurrentRepo] = useState<GitHubRepo | null>(null);
  const [loading, setLoading] = useState(false);

  const connectToGitHub = useCallback(async (token: string) => {
    setLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setIsConnected(true);
    setCurrentRepo(mockRepos[0]);
    setLoading(false);
  }, []);

  const fetchRepos = useCallback(async (): Promise<GitHubRepo[]> => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setLoading(false);
    return mockRepos;
  }, []);

  const fetchIssues = useCallback(async (filters?: any): Promise<GitHubIssue[]> => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 800));
    setLoading(false);
    return mockIssues;
  }, []);

  const fetchPRs = useCallback(async (filters?: any): Promise<GitHubPR[]> => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 800));
    setLoading(false);
    return mockPRs;
  }, []);

  const createIssue = useCallback(async (title: string, body: string, labels?: string[]): Promise<GitHubIssue> => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1200));
    const newIssue: GitHubIssue = {
      id: Date.now(),
      number: 125,
      title,
      body,
      state: 'open',
      user: {
        login: 'ai-agent',
        avatar_url: 'https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&w=40&h=40&fit=crop'
      },
      labels: labels?.map((label, index) => ({
        id: Date.now() + index,
        name: label,
        color: 'd73a49'
      })) || [],
      assignees: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      html_url: `https://github.com/user/awesome-project/issues/125`
    };
    setLoading(false);
    return newIssue;
  }, []);

  const updateIssue = useCallback(async (issueNumber: number, updates: any): Promise<GitHubIssue> => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    const updatedIssue = mockIssues.find(issue => issue.number === issueNumber);
    setLoading(false);
    return { ...updatedIssue!, ...updates };
  }, []);

  return {
    isConnected,
    currentRepo,
    loading,
    connectToGitHub,
    fetchRepos,
    fetchIssues,
    fetchPRs,
    createIssue,
    updateIssue
  };
};