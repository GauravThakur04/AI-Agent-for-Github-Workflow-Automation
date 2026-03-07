import React, { useState, useEffect } from 'react';
import { Github, Bot, Settings, Wifi, WifiOff, Activity, User, LogOut } from 'lucide-react';

interface User {
  sessionId: string;
  username: string;
  githubRepo: string;
}

interface HeaderProps {
  isConnected: boolean;
  currentRepo?: any;
  onSettingsClick: () => void;
  user?: User | null;
  isDemoMode?: boolean;
  onLogout?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ 
  isConnected, 
  currentRepo, 
  onSettingsClick, 
  user, 
  isDemoMode = false,
  onLogout 
}) => {
  const [isOnline, setIsOnline] = useState(true);
  const [showStatus, setShowStatus] = useState(false);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  useEffect(() => {
    if (isConnected) {
      setShowStatus(true);
      const timer = setTimeout(() => setShowStatus(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [isConnected]);

  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
                  <Bot className="h-6 w-6 text-white" />
                </div>
                {isConnected && (
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white animate-pulse"></div>
                )}
              </div>
              <div>
                <h1 className="text-xl font-bold gradient-text">GitHub AI Agent</h1>
                <p className="text-sm text-gray-500 flex items-center space-x-1">
                  <Activity className="w-3 h-3" />
                  <span>Intelligent Workflow Assistant</span>
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Connection Status */}
            <div className="flex items-center space-x-2">
              {isOnline ? (
                <div className="flex items-center space-x-1 text-green-600">
                  <Wifi className="h-4 w-4" />
                  <span className="text-xs font-medium">Online</span>
                </div>
              ) : (
                <div className="flex items-center space-x-1 text-red-600">
                  <WifiOff className="h-4 w-4" />
                  <span className="text-xs font-medium">Offline</span>
                </div>
              )}
            </div>

            {/* User Info */}
            {user && (
              <div className="flex items-center space-x-2 bg-blue-50 px-3 py-2 rounded-lg border border-blue-200">
                <User className="h-4 w-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-800">{user.username}</span>
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              </div>
            )}

            {/* Demo Mode Indicator */}
            {isDemoMode && (
              <div className="flex items-center space-x-2 bg-yellow-50 px-3 py-2 rounded-lg border border-yellow-200">
                <span className="text-sm font-medium text-yellow-800">Demo Mode</span>
                <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
              </div>
            )}

            {/* Repository Status */}
            {(user || isDemoMode) && (
              <div className={`flex items-center space-x-2 bg-green-50 px-3 py-2 rounded-lg border border-green-200 transition-all duration-300 ${showStatus ? 'animate-pulse-glow' : ''}`}>
                <Github className="h-4 w-4 text-green-600" />
                <span className="text-sm font-medium text-green-800">
                  {user ? user.githubRepo : 'octocat/Hello-World'}
                </span>
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              </div>
            )}

            {/* Connection Status Indicator */}
            {isConnected && (
              <div className="flex items-center space-x-2 bg-green-50 px-3 py-2 rounded-lg border border-green-200">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-xs font-medium text-green-800">Connected</span>
              </div>
            )}
            
            {/* Logout Button */}
            {onLogout && (user || isDemoMode) && (
              <button
                onClick={onLogout}
                className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200 hover:scale-105"
                title="Logout"
              >
                <LogOut className="h-5 w-5" />
              </button>
            )}
            
            {/* Settings Button */}
            <button
              onClick={onSettingsClick}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all duration-200 hover:scale-105"
            >
              <Settings className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};