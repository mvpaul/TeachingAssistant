import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  ArrowLeft, 
  BookOpen, 
  Clock, 
  Star, 
  Target,
  CheckCircle,
  AlertCircle,
  Play,
  Pause,
  RotateCcw
} from 'lucide-react'
import Whiteboard from '../../components/Whiteboard.jsx'
import ChatBox from '../../components/ChatBox.jsx'
import { aiEngine } from '../../components/AIEngine.js'
import { sessionTracker } from '../../utils/sessionTracker.js'
import toast from 'react-hot-toast'

const ProblemViewer = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [problem, setProblem] = useState(null)
  const [messages, setMessages] = useState([])
  const [misconceptions, setMisconceptions] = useState([])
  const [suggestions, setSuggestions] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isStarted, setIsStarted] = useState(false)
  const [timeSpent, setTimeSpent] = useState(0)
  const [isPaused, setIsPaused] = useState(false)

  // Problem database
  const problems = {
    'fbd_1': {
      id: 'fbd_1',
      title: 'Block on Inclined Plane',
      subject: 'statics',
      topic: 'free_body_diagrams',
      difficulty: 'easy',
      timeEstimate: '5-10 min',
      description: 'A block of mass m rests on an inclined plane that makes an angle θ with the horizontal. Draw the free body diagram for the block.',
      instructions: [
        'Identify all forces acting on the block',
        'Draw the force vectors with proper directions',
        'Label each force clearly',
        'Consider the coordinate system'
      ],
      hints: [
        'Don\'t forget the normal force from the surface',
        'The weight force acts vertically downward',
        'Consider if there\'s friction'
      ],
      solution: {
        forces: ['Weight (mg)', 'Normal Force (N)', 'Friction (f)'],
        diagram: 'Free body diagram with three forces',
        equations: ['ΣFx = 0', 'ΣFy = 0']
      }
    },
    'fbd_2': {
      id: 'fbd_2',
      title: 'Pulley System',
      subject: 'statics',
      topic: 'free_body_diagrams',
      difficulty: 'medium',
      timeEstimate: '10-15 min',
      description: 'Two masses m1 and m2 are connected by a massless string over a frictionless pulley. Draw the free body diagrams for both masses.',
      instructions: [
        'Draw separate diagrams for each mass',
        'Show the tension force in the string',
        'Consider the direction of motion',
        'Include all relevant forces'
      ],
      hints: [
        'The tension is the same throughout the string',
        'Consider the acceleration of the system',
        'Don\'t forget the weight forces'
      ],
      solution: {
        forces: ['Weight (m1g)', 'Weight (m2g)', 'Tension (T)'],
        diagram: 'Two free body diagrams connected by tension',
        equations: ['m1a = T - m1g', 'm2a = m2g - T']
      }
    },
    'force_1': {
      id: 'force_1',
      title: 'Basic Force Resolution',
      subject: 'statics',
      topic: 'force_analysis',
      difficulty: 'easy',
      timeEstimate: '5-8 min',
      description: 'A force F acts at an angle θ to the horizontal. Resolve this force into its x and y components.',
      instructions: [
        'Draw the original force vector',
        'Show the x and y components',
        'Use trigonometry to find magnitudes',
        'Label all components clearly'
      ],
      hints: [
        'Use Fx = F cos(θ)',
        'Use Fy = F sin(θ)',
        'Check your signs carefully'
      ],
      solution: {
        forces: ['F', 'Fx = F cos(θ)', 'Fy = F sin(θ)'],
        diagram: 'Force vector with resolved components',
        equations: ['Fx = F cos(θ)', 'Fy = F sin(θ)']
      }
    }
  }

  useEffect(() => {
    const problemData = problems[id]
    if (!problemData) {
      toast.error('Problem not found')
      navigate('/')
      return
    }

    setProblem(problemData)

    // Initialize session for this problem
    const sessionId = `problem-${id}-${Date.now()}`
    sessionTracker.createSession(sessionId, {
      subject: problemData.subject,
      topic: problemData.topic,
      problemId: id,
      metadata: {
        problemTitle: problemData.title,
        difficulty: problemData.difficulty
      }
    })
  }, [id, navigate])

  // Timer effect
  useEffect(() => {
    let interval
    if (isStarted && !isPaused) {
      interval = setInterval(() => {
        setTimeSpent(prev => prev + 1)
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [isStarted, isPaused])

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  const handleStartProblem = () => {
    setIsStarted(true)
    setIsPaused(false)
    
    // Add initial AI message
    const initialMessage = {
      id: `ai-${Date.now()}`,
      type: 'ai',
      content: `Welcome to "${problem.title}"! ${problem.description} Let's start by drawing the free body diagram. What do you think the first step should be?`,
      timestamp: new Date(),
      data: {
        strategy: 'problem_introduction',
        problemId: problem.id
      }
    }
    
    setMessages([initialMessage])
    toast.success('Problem started!')
  }

  const handlePauseProblem = () => {
    setIsPaused(!isPaused)
    toast.info(isPaused ? 'Problem resumed' : 'Problem paused')
  }

  const handleResetProblem = () => {
    if (confirm('Are you sure you want to reset this problem? All progress will be lost.')) {
      setIsStarted(false)
      setIsPaused(false)
      setTimeSpent(0)
      setMessages([])
      setMisconceptions([])
      setSuggestions([])
      toast.success('Problem reset')
    }
  }

  const handleDrawingSubmit = async (drawingData) => {
    setIsLoading(true)
    
    try {
      const analysis = await aiEngine.analyzeDrawing(drawingData, {
        subject: problem.subject,
        topic: problem.topic,
        problemId: problem.id
      })

      if (analysis.success) {
        const aiMessage = {
          id: `ai-${Date.now()}`,
          type: 'ai',
          content: analysis.question,
          timestamp: new Date(),
          data: {
            strategy: 'drawing_analysis',
            misconceptions: analysis.misconceptions,
            problemId: problem.id
          }
        }

        setMessages(prev => [...prev, aiMessage])
        setMisconceptions(analysis.misconceptions)
        setSuggestions(analysis.suggestions)
      }
    } catch (error) {
      console.error('Drawing analysis error:', error)
      toast.error('Error analyzing drawing')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = async (message) => {
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
        subject: problem.subject,
        topic: problem.topic,
        problemId: problem.id
      })

      if (response.success) {
        const aiMessage = {
          id: `ai-${Date.now()}`,
          type: 'ai',
          content: response.question,
          timestamp: new Date(),
          data: {
            strategy: response.strategy,
            misconceptions: response.misconceptions,
            problemId: problem.id
          }
        }

        setMessages(prev => [...prev, aiMessage])
        setMisconceptions(response.misconceptions || [])
      }
    } catch (error) {
      console.error('Message processing error:', error)
      toast.error('Error processing message')
    } finally {
      setIsLoading(false)
    }
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'text-green-600 bg-green-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'hard': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  if (!problem) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading problem...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/')}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft size={20} />
                <span>Back to Problems</span>
              </button>
            </div>

            <div className="flex items-center space-x-4">
              {isStarted && (
                <>
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Clock size={16} />
                    <span>{formatTime(timeSpent)}</span>
                  </div>
                  
                  <button
                    onClick={handlePauseProblem}
                    className="flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium bg-gray-100 hover:bg-gray-200"
                  >
                    {isPaused ? <Play size={16} /> : <Pause size={16} />}
                    <span>{isPaused ? 'Resume' : 'Pause'}</span>
                  </button>
                  
                  <button
                    onClick={handleResetProblem}
                    className="flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium bg-red-100 text-red-600 hover:bg-red-200"
                  >
                    <RotateCcw size={16} />
                    <span>Reset</span>
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Problem Info */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <h1 className="text-2xl font-bold text-gray-900">{problem.title}</h1>
                <span className={`text-xs font-medium px-2 py-1 rounded ${getDifficultyColor(problem.difficulty)}`}>
                  {problem.difficulty}
                </span>
              </div>
              
              <p className="text-gray-600 mb-4">{problem.description}</p>
              
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <BookOpen size={16} />
                  <span>{problem.subject} • {problem.topic}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock size={16} />
                  <span>Est. {problem.timeEstimate}</span>
                </div>
              </div>
            </div>

            {!isStarted && (
              <button
                onClick={handleStartProblem}
                className="btn-primary flex items-center space-x-2"
              >
                <Play size={16} />
                <span>Start Problem</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      {isStarted ? (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Problem Instructions */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Instructions</h3>
                
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Steps:</h4>
                    <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                      {problem.instructions.map((instruction, index) => (
                        <li key={index}>{instruction}</li>
                      ))}
                    </ol>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Hints:</h4>
                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                      {problem.hints.map((hint, index) => (
                        <li key={index}>{hint}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* Whiteboard and Chat */}
            <div className="lg:col-span-2 space-y-8">
              {/* Whiteboard */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Work</h3>
                <Whiteboard
                  onDrawingSubmit={handleDrawingSubmit}
                  width={700}
                  height={500}
                />
              </div>

              {/* Chat */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                <ChatBox
                  messages={messages}
                  onSendMessage={handleSendMessage}
                  isLoading={isLoading}
                  misconceptions={misconceptions}
                  suggestions={suggestions}
                  className="h-80"
                />
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <Target size={64} className="mx-auto mb-6 text-gray-300" />
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Ready to Start?</h2>
            <p className="text-gray-600 mb-8">
              Click the "Start Problem" button above to begin working on this problem with AI tutoring assistance.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProblemViewer 