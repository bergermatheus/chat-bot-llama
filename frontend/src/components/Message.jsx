import React from 'react';
import '../styles/Message.css';

const Message = ({ message, isUser }) => {
  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        <div className="message-text">{message.content}</div>
        <div className="message-time">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default Message;