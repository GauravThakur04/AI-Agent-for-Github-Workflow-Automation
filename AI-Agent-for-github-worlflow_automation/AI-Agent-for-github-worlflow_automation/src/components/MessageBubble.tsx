import React, { useState, useEffect } from 'react';
import { Bot, User, ExternalLink, Tag, Users, Clock, Loader2, CheckCircle, AlertCircle, GitPullRequest, GitCommit } from 'lucide-react';
import { ChatMessage, GitHubIssue, GitHubPR } from '../types';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.type === 'user';
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const renderIssueCard = (issue: GitHubIssue) => (
    <div key={issue.id} className="bg-white border border-gray-200 rounded-xl p-4 mt-3 hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02]">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-3">
            <span className="text-sm font-semibold text-gray-900 bg-gray-100 px-2 py-1 rounded-md">#{issue.number}</span>
            <span className={`px-3 py-1 text-xs font-medium rounded-full flex items-center space-x-1 ${
              issue.state === 'open' ? 'bg-green-100 text-green-800' : 'bg-purple-100 text-purple-800'
            }`}>
              {issue.state === 'open' ? <CheckCircle className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
              <span>{issue.state}</span>
            </span>
          </div>
          <h4 className="font-semibold text-gray-900 mb-2 text-lg">{issue.title}</h4>
          <p className="text-sm text-gray-600 mb-4 line-clamp-2 leading-relaxed">{issue.body}</p>
          
          <div className="flex items-center space-x-4 text-xs text-gray-500 mb-3">
            <div className="flex items-center space-x-2">
              <img src={issue.user.avatar_url} alt={issue.user.login} className="w-5 h-5 rounded-full border-2 border-gray-200" />
              <span className="font-medium">{issue.user.login}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Clock className="w-3 h-3" />
              <span>{formatDate(issue.created_at)}</span>
            </div>
            {issue.assignees.length > 0 && (
              <div className="flex items-center space-x-1">
                <Users className="w-3 h-3" />
                <span>{issue.assignees.length} assigned</span>
              </div>
            )}
          </div>
          
          {issue.labels.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {issue.labels.map((label) => (
                <span
                  key={label.id}
                  className="inline-flex items-center px-2 py-1 text-xs font-medium rounded-full border"
                  style={{
                    backgroundColor: `#${label.color}15`,
                    color: `#${label.color}`,
                    borderColor: `#${label.color}30`
                  }}
                >
                  <Tag className="w-3 h-3 mr-1" />
                  {label.name}
                </span>
              ))}
            </div>
          )}
        </div>
        
        <a
          href={issue.html_url}
          target="_blank"
          rel="noopener noreferrer"
          className="ml-4 p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </div>
  );

  const renderPRCard = (pr: GitHubPR) => (
    <div key={pr.id} className="bg-white border border-gray-200 rounded-xl p-4 mt-3 hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02]">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-3">
            <span className="text-sm font-semibold text-gray-900 bg-gray-100 px-2 py-1 rounded-md">#{pr.number}</span>
            <span className={`px-3 py-1 text-xs font-medium rounded-full flex items-center space-x-1 ${
              pr.state === 'open' ? 'bg-green-100 text-green-800' : 
              pr.state === 'merged' ? 'bg-purple-100 text-purple-800' : 
              'bg-red-100 text-red-800'
            }`}>
              {pr.state === 'open' ? <GitPullRequest className="w-3 h-3" /> : 
               pr.state === 'merged' ? <GitCommit className="w-3 h-3" /> : 
               <AlertCircle className="w-3 h-3" />}
              <span>{pr.state}</span>
            </span>
            {pr.draft && (
              <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full font-medium">
                Draft
              </span>
            )}
          </div>
          <h4 className="font-semibold text-gray-900 mb-2 text-lg">{pr.title}</h4>
          <p className="text-sm text-gray-600 mb-4 line-clamp-2 leading-relaxed">{pr.body}</p>
          
          <div className="flex items-center space-x-4 text-xs text-gray-500">
            <div className="flex items-center space-x-2">
              <img src={pr.user.avatar_url} alt={pr.user.login} className="w-5 h-5 rounded-full border-2 border-gray-200" />
              <span className="font-medium">{pr.user.login}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Clock className="w-3 h-3" />
              <span>{formatDate(pr.created_at)}</span>
            </div>
          </div>
        </div>
        
        <a
          href={pr.html_url}
          target="_blank"
          rel="noopener noreferrer"
          className="ml-4 p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200"
        >
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </div>
  );

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} items-start space-x-3 transition-all duration-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
      {!isUser && (
        <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={`max-w-2xl ${isUser ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white' : 'bg-white border border-gray-200'} rounded-2xl px-5 py-4 shadow-lg hover:shadow-xl transition-all duration-300`}>
        <div className="flex items-center space-x-2 mb-2">
          {isUser && <User className="w-4 h-4" />}
          <span className={`text-sm font-semibold ${isUser ? 'text-blue-100' : 'text-gray-700'}`}>
            {isUser ? 'You' : 'AI Agent'}
          </span>
          <span className={`text-xs ${isUser ? 'text-blue-200' : 'text-gray-500'}`}>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        
        <div className={`text-sm ${isUser ? 'text-white' : 'text-gray-800'} whitespace-pre-wrap leading-relaxed`}>
          {message.loading ? (
            <div className="flex items-center space-x-3">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
              <span>Processing your request...</span>
            </div>
          ) : (
            message.content
          )}
        </div>
        
        {/* Render data cards with animations */}
        {message.data?.issues && (
          <div className="mt-4 space-y-3">
            {message.data.issues.map((issue, index) => (
              <div key={issue.id} style={{ animationDelay: `${index * 100}ms` }} className="animate-fade-in-up">
                {renderIssueCard(issue)}
              </div>
            ))}
          </div>
        )}
        
        {message.data?.prs && (
          <div className="mt-4 space-y-3">
            {message.data.prs.map((pr, index) => (
              <div key={pr.id} style={{ animationDelay: `${index * 100}ms` }} className="animate-fade-in-up">
                {renderPRCard(pr)}
              </div>
            ))}
          </div>
        )}
        
        {message.data?.issue && (
          <div className="mt-4 animate-fade-in-up">
            {renderIssueCard(message.data.issue)}
          </div>
        )}
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-gray-400 to-gray-500 rounded-full flex items-center justify-center shadow-lg">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};