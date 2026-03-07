import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Sparkles, Bot, MessageSquare } from 'lucide-react';
import { ChatMessage } from '../types';
import { MessageBubble } from './MessageBubble';

interface User {
  sessionId: string;
  username: string;
  githubRepo: string;
}

interface ChatInterfaceProps {
  messages: ChatMessage[];
  isProcessing: boolean;
  onSendMessage: (message: string) => void;
  user?: User | null;
  isDemoMode?: boolean;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  isProcessing,
  onSendMessage,
  user,
  isDemoMode = false
}) => {
  const [inputValue, setInputValue] = useState('');
  const [showTypingIndicator, setShowTypingIndicator] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isProcessing) {
      setShowTypingIndicator(true);
    } else {
      // Delay hiding typing indicator for better UX
      const timer = setTimeout(() => setShowTypingIndicator(false), 500);
      return () => clearTimeout(timer);
    }
  }, [isProcessing]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isProcessing) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const suggestionQueries = [
    "Create a bug for login failure",
    "Show me all open issues",
    "What PRs are pending review?",
    "Update issue #123 status",
    "Summarize repository activity"
  ];

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Welcome Message */}
      {messages.length === 0 && (
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="text-center max-w-md">
            <div className="mb-6">
              <div className="relative inline-block">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
                  <Bot className="w-10 h-10 text-white" />
                </div>
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                  <div className="w-2 h-2 bg-white rounded-full"></div>
                </div>
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">GitHub AI Agent</h2>
              <p className="text-gray-600 mb-6">Your intelligent assistant for GitHub repository management</p>

              {/* User/Demo Mode Info */}
              {user && (
                <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                  <p className="text-sm text-blue-800">
                    <strong>Welcome back, {user.username}!</strong><br />
                    Working with: <code className="bg-blue-100 px-1 rounded">{user.githubRepo}</code>
                  </p>
                </div>
              )}

              {isDemoMode && (
                <div className="mb-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                  <p className="text-sm text-yellow-800">
                    <strong>Demo Mode</strong><br />
                    Using sample repository: <code className="bg-yellow-100 px-1 rounded">octocat/Hello-World</code>
                  </p>
                </div>
              )}
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
              <div className="flex items-center mb-4">
                <Sparkles className="w-5 h-5 text-blue-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-800">Try asking me:</h3>
              </div>
              <div className="space-y-3">
                {suggestionQueries.map((query, index) => (
                  <button
                    key={index}
                    onClick={() => !isProcessing && onSendMessage(query)}
                    disabled={isProcessing}
                    className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 disabled:opacity-50 group"
                  >
                    <div className="flex items-center">
                      <MessageSquare className="w-4 h-4 text-gray-400 group-hover:text-blue-600 mr-3 transition-colors" />
                      <span className="text-sm text-gray-700 group-hover:text-gray-900">"{query}"</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div key={message.id} className={`animate-fade-in-up`} style={{ animationDelay: `${index * 100}ms` }}>
            <MessageBubble message={message} />
          </div>
        ))}

        {/* Typing Indicator */}
        {showTypingIndicator && (
          <div className="flex justify-start items-start space-x-2 animate-fade-in">
            <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 shadow-sm">
              <div className="flex items-center space-x-2 mb-1">
                <span className="text-sm font-medium text-gray-700">AI Agent</span>
                <span className="text-xs text-gray-500">
                  {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
                <span className="text-sm text-gray-600">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t border-gray-200 shadow-lg">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask me to create issues, check PRs, or help with GitHub tasks..."
              disabled={isProcessing}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed transition-all duration-200 shadow-sm"
            />
            {isProcessing && (
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
              </div>
            )}
          </div>
          <button
            type="submit"
            disabled={!inputValue.trim() || isProcessing}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            {isProcessing ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
            <span className="hidden sm:inline font-medium">Send</span>
          </button>
        </form>
      </div>
    </div>
  );
};