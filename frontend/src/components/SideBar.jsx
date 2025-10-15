import React, { useState, useEffect } from 'react';
import { chatAPI } from '../services/api';
import '../styles/Sidebar.css';

const Sidebar = ({ onConversationSelect, currentConversationId, refreshTrigger }) => {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConversations();
  }, [refreshTrigger]);

  const loadConversations = async () => {
    try {
      const response = await chatAPI.getConversationHistory();
      setConversations(response.data.conversations || []);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    onConversationSelect(null);
  };

  const handleConversationClick = (conversationId) => {
    onConversationSelect(conversationId);
  };

  if (loading) {
    return (
      <div className="sidebar">
        <div className="sidebar-header">
          <button onClick={handleNewChat} className="new-chat-btn">
            + New Chat
          </button>
        </div>
        <div className="loading">Loading conversations...</div>
      </div>
    );
  }

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <button onClick={handleNewChat} className="new-chat-btn">
          + New Chat
        </button>
      </div>
      <div className="conversations-list">
        {conversations.map((conversation) => (
          <div
            key={conversation.conversation_id}
            className={`conversation-item ${
              currentConversationId === conversation.conversation_id ? 'active' : ''
            }`}
            onClick={() => handleConversationClick(conversation.conversation_id)}
          >
            <div className="conversation-preview">
              {conversation.messages.length > 0
                ? conversation.messages[conversation.messages.length - 1].content.substring(0, 50) + '...'
                : 'Empty conversation'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;