import { useState, useCallback } from 'react';
import { ChatMessage } from '../types';

export const useAIAgent = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'agent',
      content: "Hello! I'm your GitHub AI assistant. I can help you manage issues, pull requests, and other GitHub operations using natural language. What would you like to do today?",
      timestamp: new Date()
    }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const processQuery = useCallback(async (userQuery: string) => {
    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: userQuery,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsProcessing(true);

    // Add loading message
    const loadingMessage: ChatMessage = {
      id: (Date.now() + 1).toString(),
      type: 'agent',
      content: 'Let me process that for you...',
      timestamp: new Date(),
      loading: true
    };
    setMessages(prev => [...prev, loadingMessage]);

    try {
      // Call backend with session management
      const endpoint = sessionId ? '/chat' : '/query';
      const payload = sessionId 
        ? { message: userQuery, session_id: sessionId }
        : { query: userQuery };

      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      const data = await response.json();
      
      // Remove loading messages and add response
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => !msg.loading);
        return [
          ...withoutLoading,
          {
            id: (Date.now() + 2).toString(),
            type: 'agent',
            content: data.response || data.result || 'No response from agent.',
            timestamp: new Date(),
            data: data.data || data.log ? { log: data.log } : undefined,
            suggestions: data.suggestions || []
          }
        ];
      });
    } catch (error) {
      setMessages(prev => {
        const withoutLoading = prev.filter(msg => !msg.loading);
        return [
          ...withoutLoading,
          {
            id: (Date.now() + 2).toString(),
            type: 'agent',
            content: 'I encountered an error while processing your request. Please try again.',
            timestamp: new Date()
          }
        ];
      });
    } finally {
      setIsProcessing(false);
    }
  }, [sessionId]);

  return {
    messages,
    isProcessing,
    processQuery,
    sessionId,
    setSessionId
  };
};
