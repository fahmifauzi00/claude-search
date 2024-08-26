import React from 'react';

const Message = ({ role, content, timestamp }) => {
  return (
    <div className={`message-container ${role}`}>
      <div className={`message ${role}`}>
        <div className="message-content">{content}</div>
        <div className="message-timestamp">{timestamp}</div>
      </div>
    </div>
  );
};

export default Message;