import React from 'react';
import Message from './Message';

const MessageList = ({ messages }) => {
  return (
    <div className="message-list-container">
      <div className="message-list">
        {messages.map((message, index) => (
          <Message 
            key={index} 
            role={message.role} 
            content={message.content} 
            timestamp={new Date(message.timestamp).toLocaleTimeString()}
          />
        ))}
      </div>
    </div>
  );
};

export default MessageList;