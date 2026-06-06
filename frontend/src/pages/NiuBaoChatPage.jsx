import { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bytemd/dist/index.css';
import 'github-markdown-css/github-markdown-light.css';
import 'highlight.js/styles/github.css';
import 'katex/dist/katex.css';

import gfm from '@bytemd/plugin-gfm';
import highlightSsr from '@bytemd/plugin-highlight-ssr';
import math from '@bytemd/plugin-math';
import { Viewer } from '@bytemd/react';

import { useAuth } from '../contexts/use-auth';
import httpClient from '../api/http-client';

function ChatPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const storageKey = useMemo(() => (user ? `niubao_chats_${user.id}` : 'niubao_chats_guest'), [user]);

  const initialConversations = useMemo(() => {
    try {
      const stored = localStorage.getItem(storageKey);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  }, []);

  const [conversations, setConversations] = useState(initialConversations);
  const [activeChatId, setActiveChatId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const viewerPlugins = useMemo(() => [gfm(), math({ katexOptions: { strict: false } }), highlightSsr()], []);

  useEffect(() => {
    localStorage.setItem(storageKey, JSON.stringify(conversations));
  }, [conversations, storageKey]);

  useEffect(() => {
    if (activeChatId) {
      const chat = conversations.find((c) => c.id === activeChatId);
      setMessages(chat ? chat.messages : []);
    } else {
      setMessages([]);
    }
  }, [activeChatId, conversations]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  function handleNewChat() {
    const newChat = { id: Date.now().toString(), title: '新对话', messages: [] };
    setConversations((prev) => [newChat, ...prev]);
    setActiveChatId(newChat.id);
  }

  function handleDeleteChat(chatId, e) {
    e.stopPropagation();
    const updated = conversations.filter((c) => c.id !== chatId);
    setConversations(updated);
    if (activeChatId === chatId) {
      setActiveChatId(updated.length > 0 ? updated[0].id : null);
    }
  }

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;
    const newMessages = [...messages, { role: 'user', content: text }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);
    try {
      const response = await httpClient.post('/ai/chat', { messages: newMessages });
      const updatedMessages = [...newMessages, { role: 'assistant', content: response.data.reply }];
      setMessages(updatedMessages);
      setConversations((prev) =>
        prev.map((c) =>
          c.id === activeChatId ? { ...c, title: text.slice(0, 30), messages: updatedMessages } : c
        )
      );
    } catch {
      const updatedMessages = [...newMessages, { role: 'assistant', content: '😢 不好意思，我好像断线了，请稍后再试。' }];
      setMessages(updatedMessages);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <section className="page-section chat-page">
      <div className="chat-layout">
        <aside className="chat-sidebar">
          <button className="secondary-button" style={{ width: '100%', marginBottom: 12 }} onClick={handleNewChat}>
            + 新建对话
          </button>
          <div className="chat-conversations">
            {conversations.map((chat) => (
              <button
                key={chat.id}
                className={`chat-conv-item ${chat.id === activeChatId ? 'active' : ''}`}
                onClick={() => setActiveChatId(chat.id)}
              >
                <span>{chat.title}</span>
                <button className="chat-conv-delete" onClick={(e) => handleDeleteChat(chat.id, e)}>✕</button>
              </button>
            ))}
          </div>
        </aside>
        <main className="chat-main">
          {activeChatId ? (
            <>
              <div className="chat-messages">
                {messages.map((msg, i) => (
                  <div key={i} className={`chat-bubble ${msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-bot'}`}>
                    {msg.role === 'assistant' ? (
                      <div className="markdown-body" style={{ fontSize: 14 }}>
                        <Viewer plugins={viewerPlugins} value={msg.content} />
                      </div>
                    ) : (
                      <p>{msg.content}</p>
                    )}
                  </div>
                ))}
                {loading && <div className="chat-bubble chat-bubble-bot"><p>🤔 牛宝正在思考...</p></div>}
                <div ref={messagesEndRef} />
              </div>
              <div className="chat-input-row">
                <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyDown} placeholder="跟牛宝说点什么..." disabled={loading} />
                <button onClick={handleSend} disabled={loading || !input.trim()}>发送</button>
              </div>
            </>
          ) : (
            <div className="chat-empty" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <p style={{ fontSize: 48, margin: '0 0 12px' }}>🐮</p>
              <p style={{ color: '#888', fontSize: 18 }}>选择或新建一个对话</p>
            </div>
          )}
        </main>
      </div>
    </section>
  );
}

export default ChatPage;