import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, AlertCircle, CheckCircle, Clock } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import toast from 'react-hot-toast'

const ChatBox = ({ 
  messages = [], 
  onSendMessage, 
  isLoading = false,
  misconceptions = [],
  suggestions = [],
  className = '' 
}) => {
  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Focus input when component mounts
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!inputValue.trim() || isLoading) return

    const message = inputValue.trim()
    setInputValue('')

    try {
      await onSendMessage(message)
    } catch (error) {
      toast.error('Failed to send message')
      console.error('Send message error:', error)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const getMessageIcon = (type) => {
    switch (type) {
      case 'ai':
        return <Bot size={16} className="text-primary-600" />
      case 'user':
        return <User size={16} className="text-accent-600" />
      case 'system':
        return <Clock size={16} className="text-gray-500" />
      default:
        return <Bot size={16} className="text-gray-500" />
    }
  }

  const getMessageStyle = (type) => {
    switch (type) {
      case 'ai':
        return 'bg-primary-50 border-primary-200'
      case 'user':
        return 'bg-accent-50 border-accent-200 ml-auto'
      case 'system':
        return 'bg-gray-50 border-gray-200'
      default:
        return 'bg-white border-gray-200'
    }
  }

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return ''
    
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className={`flex flex-col h-full bg-white rounded-lg shadow-sm border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <Bot size={20} className="text-primary-600" />
          <h3 className="font-semibold text-gray-900">AI Tutor Chat</h3>
          {isLoading && (
            <div className="flex items-center space-x-1 text-sm text-gray-500">
              <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-primary-600"></div>
              <span>Thinking...</span>
            </div>
          )}
        </div>
        
        <div className="text-sm text-gray-500">
          {messages.length} messages
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <Bot size={48} className="mx-auto mb-4 text-gray-300" />
            <p className="text-lg font-medium">Welcome to AI Tutoring!</p>
            <p className="text-sm">Draw something and submit it to start a conversation.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={message.id || index}
              className={`flex items-start space-x-3 max-w-[80%] ${message.type === 'user' ? 'ml-auto' : ''}`}
            >
              {message.type !== 'user' && (
                <div className="flex-shrink-0 mt-1">
                  {getMessageIcon(message.type)}
                </div>
              )}
              
              <div className={`flex-1 p-3 rounded-lg border ${getMessageStyle(message.type)}`}>
                <div className="flex items-start justify-between mb-1">
                  <span className="text-xs font-medium text-gray-600 capitalize">
                    {message.type === 'ai' ? 'AI Tutor' : message.type}
                  </span>
                  {message.timestamp && (
                    <span className="text-xs text-gray-400">
                      {formatTimestamp(message.timestamp)}
                    </span>
                  )}
                </div>
                
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown 
                    remarkPlugins={[remarkGfm]}
                    components={{
                      p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                      strong: ({ children }) => <strong className="font-semibold text-gray-900">{children}</strong>,
                      em: ({ children }) => <em className="italic">{children}</em>,
                      code: ({ children }) => <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono">{children}</code>,
                      pre: ({ children }) => <pre className="bg-gray-100 p-2 rounded text-sm overflow-x-auto">{children}</pre>
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                
                  {/* Message metadata */}
                  {message.data && (
                    <div className="mt-2 pt-2 border-t border-gray-200">
                      {message.data.strategy && (
                        <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-2">
                          {message.data.strategy}
                        </span>
                      )}
                      {message.data.misconceptions && message.data.misconceptions.length > 0 && (
                        <span className="inline-block bg-red-100 text-red-800 text-xs px-2 py-1 rounded">
                          {message.data.misconceptions.length} misconception(s)
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
              
              {message.type === 'user' && (
                <div className="flex-shrink-0 mt-1">
                  {getMessageIcon(message.type)}
                </div>
              )}
            </div>
          ))
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Misconceptions and Suggestions */}
      {(misconceptions.length > 0 || suggestions.length > 0) && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          {misconceptions.length > 0 && (
            <div className="mb-3">
              <div className="flex items-center space-x-2 mb-2">
                <AlertCircle size={16} className="text-red-500" />
                <span className="text-sm font-medium text-gray-700">Misconceptions Detected</span>
              </div>
              <div className="space-y-1">
                {misconceptions.map((misconception, index) => (
                  <div key={index} className="text-sm text-red-700 bg-red-50 p-2 rounded">
                    {misconception.message}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {suggestions.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <CheckCircle size={16} className="text-green-500" />
                <span className="text-sm font-medium text-gray-700">Suggestions</span>
              </div>
              <div className="space-y-1">
                {suggestions.map((suggestion, index) => (
                  <div key={index} className="text-sm text-green-700 bg-green-50 p-2 rounded">
                    {suggestion.suggestion}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Input */}
      <div className="border-t border-gray-200 p-4">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your response..."
            disabled={isLoading}
            className="flex-1 input-field disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed px-4"
          >
            <Send size={16} />
          </button>
        </form>
        
        <div className="mt-2 text-xs text-gray-500">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  )
}

export default ChatBox 