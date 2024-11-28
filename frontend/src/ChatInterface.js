import React, { useState, useEffect } from 'react';
import './ChatInterface.css';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatInterface = ({ title }) => {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentDate, setCurrentDate] = useState(null);

  useEffect(() => {
    setSessionId(Math.random().toString(36).substring(7));
  }, []);

  const sendMessage = async (message) => {
    const timestamp = new Date().toISOString();
    setMessages([...messages, { role: 'user', content: message, timestamp }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, session_id: sessionId }),
      });
      const data = await response.json();
      
      setCurrentDate(data.current_date);
      setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: data.message, timestamp: new Date().toISOString() }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: 'Sorry, an error occurred. Please try again.', timestamp: new Date().toISOString() }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1 className="chat-title">{title}</h1>
        {currentDate && <div className="current-date">Current date: {currentDate}</div>}
      </div>
      <MessageList messages={messages} />
      {isLoading && <div className="loading-indicator">AI is thinking...</div>}
      <MessageInput onSendMessage={sendMessage} />
    </div>
  );
};

export default ChatInterface;