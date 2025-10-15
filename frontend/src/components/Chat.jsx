import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { chatAPI } from '../services/api';
import Sidebar from './SideBar';
import Message from './Message';
import '../styles/Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [refreshSidebar, setRefreshSidebar] = useState(0);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const { user, logout } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadConversation = async (conversationId) => {
    try {
      const response = await chatAPI.getConversationHistory(conversationId);
      if (conversationId) {
        setMessages(response.data.messages || []);
      } else {
        setMessages([]);
      }
      setCurrentConversationId(conversationId);
    } catch (error) {
      console.error('Failed to load conversation:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage({ message: inputMessage });
      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMessage]);
      
      setRefreshSidebar(prev => prev + 1);
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setCurrentConversationId(null);
  };

  return (
    <div className="chat-container">
      <Sidebar 
        onConversationSelect={loadConversation}
        currentConversationId={currentConversationId}
        refreshTrigger={refreshSidebar}
      />
      <div className="chat-main">
        <div className="chat-header">
          <h2>Chat with AI Assistant</h2>
          <div className="user-info">
            <span>Welcome, {user?.username}</span>
            <button onClick={logout} className="logout-btn">Logout</button>
          </div>
        </div>
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <h3>Start a new conversation</h3>
              <p>Send a message to begin chatting with the AI assistant.</p>
            </div>
          ) : (
            messages.map((message, index) => (
              <Message
                key={index}
                message={message}
                isUser={message.role === 'user'}
              />
            ))
          )}
          {loading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <form onSubmit={handleSendMessage} className="message-form">
          <input
            ref={inputRef}
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            disabled={loading}
            autoFocus
          />
          <button type="submit" disabled={loading || !inputMessage.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chat;