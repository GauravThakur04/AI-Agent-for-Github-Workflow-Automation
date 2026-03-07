import { Header } from './components/Header';
import { ChatInterface } from './components/ChatInterface';
import AuthModal from './components/AuthModal';
import { useAIAgent } from './hooks/useAIAgent';
import { useEffect, useState } from 'react';

interface User {
  sessionId: string;
  username: string;
  githubRepo: string;
}

function App() {
  const {
    messages,
    isProcessing,
    processQuery,
    setSessionId
  } = useAIAgent();

  const [isLoaded, setIsLoaded] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [isDemoMode, setIsDemoMode] = useState(false);

  useEffect(() => {
    // Add a small delay for smooth loading animation
    const timer = setTimeout(() => setIsLoaded(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const handleLogin = (sessionId: string, username: string, githubRepo: string) => {
    setUser({ sessionId, username, githubRepo });
    setSessionId(sessionId);
    setShowAuthModal(false);
    setIsDemoMode(false);
  };

  const handleDemoMode = () => {
    setIsDemoMode(true);
    setShowAuthModal(false);
    setUser(null);
    setSessionId(null);
  };

  const handleLogout = () => {
    setUser(null);
    setIsDemoMode(false);
    setSessionId(null);
    setShowAuthModal(true);
  };

  const handleSettingsClick = () => {
    if (!user && !isDemoMode) {
      setShowAuthModal(true);
    } else {
      // Show user profile or settings
      console.log('Show user settings');
    }
  };

  return (
    <div className={`h-screen bg-white flex flex-col transition-all duration-700 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}>
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <Header
        isConnected={!!user || isDemoMode}
        onSettingsClick={handleSettingsClick}
        user={user}
        isDemoMode={isDemoMode}
        onLogout={handleLogout}
      />

      <main className="flex-1 flex flex-col overflow-hidden relative z-10">
        {!user && !isDemoMode ? (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center max-w-md mx-auto p-8">
              <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-4">
                  GitHub AI Agent
                </h1>
                <p className="text-lg text-gray-600 mb-8">
                  Your intelligent assistant for GitHub repository management
                </p>
              </div>

              <div className="space-y-4">
                <button
                  onClick={() => setShowAuthModal(true)}
                  className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  Sign In / Create Account
                </button>

                <button
                  onClick={handleDemoMode}
                  className="w-full bg-gray-100 text-gray-700 py-3 px-6 rounded-lg hover:bg-gray-200 transition-colors font-medium"
                >
                  Try Demo Mode
                </button>
              </div>

              <div className="mt-8 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-blue-800 mb-2">What you can do:</h3>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• Create and manage GitHub issues</li>
                  <li>• View pull requests and repository data</li>
                  <li>• Add comments and assign users</li>
                  <li>• Get intelligent suggestions for workflows</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <ChatInterface
            messages={messages}
            isProcessing={isProcessing}
            onSendMessage={processQuery}
            user={user}
            isDemoMode={isDemoMode}
          />
        )}
      </main>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onLogin={handleLogin}
      />
    </div>
  );
}

export default App;