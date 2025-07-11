import React, { useState, useEffect } from 'react'
import { 
  BookOpen, 
  Target, 
  BarChart3, 
  Settings, 
  RefreshCw, 
  Download,
  Clock,
  CheckCircle,
  AlertCircle,
  TrendingUp
} from 'lucide-react'
import { sessionTracker } from '../utils/sessionTracker.js'
import { aiEngine } from './AIEngine.js'

const Sidebar = ({ 
  subject, 
  topic, 
  onSubjectChange, 
  onTopicChange,
  className = '' 
}) => {
  const [sessionStats, setSessionStats] = useState(null)
  const [isExpanded, setIsExpanded] = useState(true)

  const subjects = [
    {
      id: 'statics',
      name: 'Statics',
      icon: BookOpen,
      topics: [
        { id: 'free_body_diagrams', name: 'Free Body Diagrams' },
        { id: 'force_analysis', name: 'Force Analysis' },
        { id: 'moment_calculations', name: 'Moment Calculations' },
        { id: 'equilibrium', name: 'Equilibrium' }
      ]
    },
    {
      id: 'dynamics',
      name: 'Dynamics',
      icon: TrendingUp,
      topics: [
        { id: 'motion_analysis', name: 'Motion Analysis' },
        { id: 'kinematics', name: 'Kinematics' },
        { id: 'kinetics', name: 'Kinetics' }
      ]
    },
    {
      id: 'thermodynamics',
      name: 'Thermodynamics',
      icon: Target,
      topics: [
        { id: 'energy_analysis', name: 'Energy Analysis' },
        { id: 'heat_transfer', name: 'Heat Transfer' },
        { id: 'entropy', name: 'Entropy' }
      ]
    },
    {
      id: 'fluid_mechanics',
      name: 'Fluid Mechanics',
      icon: BarChart3,
      topics: [
        { id: 'fluid_statics', name: 'Fluid Statics' },
        { id: 'fluid_dynamics', name: 'Fluid Dynamics' },
        { id: 'pressure_analysis', name: 'Pressure Analysis' }
      ]
    }
  ]

  // Update session stats periodically
  useEffect(() => {
    const updateStats = () => {
      const stats = sessionTracker.getSessionStats()
      setSessionStats(stats)
    }

    updateStats()
    const interval = setInterval(updateStats, 5000) // Update every 5 seconds

    return () => clearInterval(interval)
  }, [])

  const handleSubjectChange = (newSubject) => {
    onSubjectChange?.(newSubject)
    // Reset topic to first available topic for new subject
    const selectedSubject = subjects.find(s => s.id === newSubject)
    if (selectedSubject && selectedSubject.topics.length > 0) {
      onTopicChange?.(selectedSubject.topics[0].id)
    }
  }

  const handleTopicChange = (newTopic) => {
    onTopicChange?.(newTopic)
  }

  const formatDuration = (seconds) => {
    if (!seconds) return '0s'
    
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    
    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`
    }
    return `${remainingSeconds}s`
  }

  const exportSession = () => {
    const sessionData = sessionTracker.exportSession()
    if (sessionData) {
      const blob = new Blob([JSON.stringify(sessionData, null, 2)], {
        type: 'application/json'
      })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `session-${sessionData.id}-${Date.now()}.json`
      link.click()
      URL.revokeObjectURL(url)
    }
  }

  const resetSession = () => {
    if (confirm('Are you sure you want to reset the current session? This will clear all progress.')) {
      sessionTracker.clearSession()
      setSessionStats(null)
    }
  }

  const getCurrentSubject = () => subjects.find(s => s.id === subject)
  const getCurrentTopic = () => {
    const currentSubject = getCurrentSubject()
    return currentSubject?.topics.find(t => t.id === topic)
  }

  return (
    <div className={`bg-white border-r border-gray-200 flex flex-col ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Settings</h2>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1 rounded hover:bg-gray-100"
          >
            <Settings size={16} className="text-gray-600" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {/* Subject Selection */}
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Subject</h3>
          <div className="space-y-2">
            {subjects.map((subjectOption) => (
              <button
                key={subjectOption.id}
                onClick={() => handleSubjectChange(subjectOption.id)}
                className={`w-full flex items-center space-x-3 p-2 rounded-lg text-left transition-colors ${
                  subject === subjectOption.id
                    ? 'bg-primary-100 text-primary-700 border border-primary-200'
                    : 'hover:bg-gray-50 text-gray-700'
                }`}
              >
                <subjectOption.icon size={16} />
                <span className="text-sm font-medium">{subjectOption.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Topic Selection */}
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Topic</h3>
          <div className="space-y-1">
            {getCurrentSubject()?.topics.map((topicOption) => (
              <button
                key={topicOption.id}
                onClick={() => handleTopicChange(topicOption.id)}
                className={`w-full text-left p-2 rounded text-sm transition-colors ${
                  topic === topicOption.id
                    ? 'bg-accent-100 text-accent-700 font-medium'
                    : 'hover:bg-gray-50 text-gray-600'
                }`}
              >
                {topicOption.name}
              </button>
            ))}
          </div>
        </div>

        {/* Session Statistics */}
        {sessionStats && (
          <div className="p-4 border-b border-gray-200">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Session Progress</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <Clock size={14} className="text-gray-500" />
                  <span className="text-gray-600">Duration</span>
                </div>
                <span className="font-medium">{formatDuration(sessionStats.duration)}</span>
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <CheckCircle size={14} className="text-green-500" />
                  <span className="text-gray-600">Questions</span>
                </div>
                <span className="font-medium">{sessionStats.userMessageCount}</span>
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <AlertCircle size={14} className="text-red-500" />
                  <span className="text-gray-600">Misconceptions</span>
                </div>
                <span className="font-medium">{sessionStats.misconceptionCount}</span>
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <BarChart3 size={14} className="text-blue-500" />
                  <span className="text-gray-600">Drawings</span>
                </div>
                <span className="font-medium">{sessionStats.drawingCount}</span>
              </div>
            </div>
          </div>
        )}

        {/* AI Recommendations */}
        {sessionStats && (
          <div className="p-4 border-b border-gray-200">
            <h3 className="text-sm font-medium text-gray-700 mb-3">AI Recommendations</h3>
            <div className="space-y-2">
              {sessionStats.misconceptionCount > 0 && (
                <div className="text-xs text-red-600 bg-red-50 p-2 rounded">
                  Address {sessionStats.misconceptionCount} misconception(s)
                </div>
              )}
              
              {sessionStats.drawingCount < 2 && (
                <div className="text-xs text-blue-600 bg-blue-50 p-2 rounded">
                  Practice with more drawings
                </div>
              )}
              
              {sessionStats.userMessageCount < 3 && (
                <div className="text-xs text-green-600 bg-green-50 p-2 rounded">
                  Engage more with the AI tutor
                </div>
              )}
            </div>
          </div>
        )}

        {/* Session Actions */}
        <div className="p-4">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Session</h3>
          <div className="space-y-2">
            <button
              onClick={exportSession}
              className="w-full flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-50 text-gray-700 text-sm"
            >
              <Download size={14} />
              <span>Export Session</span>
            </button>
            
            <button
              onClick={resetSession}
              className="w-full flex items-center space-x-2 p-2 rounded-lg hover:bg-red-50 text-red-600 text-sm"
            >
              <RefreshCw size={14} />
              <span>Reset Session</span>
            </button>
          </div>
        </div>
      </div>

      {/* Current Selection Display */}
      <div className="p-4 border-t border-gray-200 bg-gray-50">
        <div className="text-xs text-gray-500 mb-1">Current</div>
        <div className="text-sm font-medium text-gray-900">
          {getCurrentSubject()?.name} • {getCurrentTopic()?.name}
        </div>
      </div>
    </div>
  )
}

export default Sidebar 