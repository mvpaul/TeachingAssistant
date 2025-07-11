import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Pen, 
  MessageSquare, 
  BookOpen, 
  Upload,
  Settings,
  Bot,
  Sparkles
} from 'lucide-react'
import Whiteboard from '../components/Whiteboard.jsx'
import ChatBox from '../components/ChatBox.jsx'
import Sidebar from '../components/Sidebar.jsx'
import FileUploader from '../components/FileUploader.jsx'
import ProblemSelector from '../components/ProblemSelector.jsx'
import { aiEngine } from '../components/AIEngine.js'
import { sessionTracker } from '../utils/sessionTracker.js'
import toast from 'react-hot-toast'

const HomePage = () => {
  const [subject, setSubject] = useState('statics')
  const [topic, setTopic] = useState('free_body_diagrams')
  const [messages, setMessages] = useState([])
  const [misconceptions, setMisconceptions] = useState([])
  const [suggestions, setSuggestions] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [showFileUploader, setShowFileUploader] = useState(false)
  const [showProblemSelector, setShowProblemSelector] = useState(false)
  const [currentView, setCurrentView] = useState('whiteboard') // 'whiteboard', 'problems', 'upload'
  
  const navigate = useNavigate()

  // Initialize session
  useEffect(() => {
    const sessionId = `session-${Date.now()}`
    sessionTracker.createSession(sessionId, {
      subject,
      topic,
      metadata: {
        userAgent: navigator.userAgent,
        screenSize: `${window.screen.width}x${window.screen.height}`
      }
    })
  }, [])

  // Update session when subject/topic changes
  useEffect(() => {
    const session = sessionTracker.getCurrentSession()
    if (session) {
      sessionTracker.updateState({
        subject,
        topic
      })
    }
  }, [subject, topic])

  const handleDrawingSubmit = async (drawingData) => {
    setIsLoading(true)
    
    try {
      const analysis = await aiEngine.analyzeDrawing(drawingData, {
        subject,
        topic
      })

      if (analysis.success) {
        // Add AI message to chat
        const aiMessage = {
          id: `ai-${Date.now()}`,
          type: 'ai',
          content: analysis.question,
          timestamp: new Date(),
          data: {
            strategy: 'initial_analysis',
            misconceptions: analysis.misconceptions
          }
        }

        setMessages(prev => [...prev, aiMessage])
        setMisconceptions(analysis.misconceptions)
        setSuggestions(analysis.suggestions)

        toast.success('Drawing analyzed successfully!')
      } else {
        toast.error('Failed to analyze drawing')
      }
    } catch (error) {
      console.error('Drawing analysis error:', error)
      toast.error('Error analyzing drawing')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = async (message) => {
    // Add user message
    const userMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: message,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await aiEngine.processResponse(message, {
        subject,
        topic
      })

      if (response.success) {
        // Add AI response
        const aiMessage = {
          id: `ai-${Date.now()}`,
          type: 'ai',
          content: response.question,
          timestamp: new Date(),
          data: {
            strategy: response.strategy,
            misconceptions: response.misconceptions
          }
        }

        setMessages(prev => [...prev, aiMessage])
        setMisconceptions(response.misconceptions || [])
      } else {
        toast.error('Failed to process response')
      }
    } catch (error) {
      console.error('Message processing error:', error)
      toast.error('Error processing message')
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = async (files) => {
    // Process uploaded files
    console.log('Files uploaded:', files)
    toast.success(`${files.length} file(s) uploaded`)
    setShowFileUploader(false)
  }

  const handleSubjectChange = (newSubject) => {
    setSubject(newSubject)
    // Reset messages when changing subject
    setMessages([])
    setMisconceptions([])
    setSuggestions([])
  }

  const handleTopicChange = (newTopic) => {
    setTopic(newTopic)
    // Reset messages when changing topic
    setMessages([])
    setMisconceptions([])
    setSuggestions([])
  }

  const getCurrentViewComponent = () => {
    switch (currentView) {
      case 'problems':
        return <ProblemSelector />
      case 'upload':
        return (
          <div className="max-w-2xl mx-auto">
            <FileUploader onFileUpload={handleFileUpload} />
          </div>
        )
      default:
        return (
          <Whiteboard
            onDrawingSubmit={handleDrawingSubmit}
            width={800}
            height={600}
          />
        )
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Bot size={24} className="text-primary-600" />
                <h1 className="text-xl font-bold text-gray-900">Smart Whiteboard</h1>
                <Sparkles size={16} className="text-yellow-500" />
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={() => setCurrentView('whiteboard')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentView === 'whiteboard'
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Pen size={16} />
                <span>Whiteboard</span>
              </button>

              <button
                onClick={() => setCurrentView('problems')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentView === 'problems'
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <BookOpen size={16} />
                <span>Problems</span>
              </button>

              <button
                onClick={() => setCurrentView('upload')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentView === 'upload'
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Upload size={16} />
                <span>Upload</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === 'whiteboard' ? (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Sidebar */}
            <div className="lg:col-span-1">
              <Sidebar
                subject={subject}
                topic={topic}
                onSubjectChange={handleSubjectChange}
                onTopicChange={handleTopicChange}
                className="h-fit sticky top-8"
              />
            </div>

            {/* Main Content Area */}
            <div className="lg:col-span-3 space-y-8">
              {/* Whiteboard */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">Smart Whiteboard</h2>
                  <div className="text-sm text-gray-500">
                    {subject} • {topic}
                  </div>
                </div>
                
                {getCurrentViewComponent()}
              </div>

              {/* Chat */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                <ChatBox
                  messages={messages}
                  onSendMessage={handleSendMessage}
                  isLoading={isLoading}
                  misconceptions={misconceptions}
                  suggestions={suggestions}
                  className="h-96"
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="max-w-6xl mx-auto">
            {getCurrentViewComponent()}
          </div>
        )}
      </div>
    </div>
  )
}

export default HomePage 