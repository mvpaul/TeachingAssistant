import React, { useState, useEffect } from 'react'
import { 
  BookOpen, 
  Target, 
  BarChart3, 
  TrendingUp,
  Star,
  Clock,
  CheckCircle,
  Play,
  Lock,
  Award
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const ProblemSelector = ({ className = '' }) => {
  const [selectedSubject, setSelectedSubject] = useState('statics')
  const [selectedDifficulty, setSelectedDifficulty] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  const subjects = [
    {
      id: 'statics',
      name: 'Statics',
      icon: BookOpen,
      color: 'blue',
      topics: [
        {
          id: 'free_body_diagrams',
          name: 'Free Body Diagrams',
          problems: [
            { id: 'fbd_1', title: 'Block on Inclined Plane', difficulty: 'easy', timeEstimate: '5-10 min', completed: false },
            { id: 'fbd_2', title: 'Pulley System', difficulty: 'medium', timeEstimate: '10-15 min', completed: false },
            { id: 'fbd_3', title: 'Complex Truss Analysis', difficulty: 'hard', timeEstimate: '20-30 min', completed: false }
          ]
        },
        {
          id: 'force_analysis',
          name: 'Force Analysis',
          problems: [
            { id: 'force_1', title: 'Basic Force Resolution', difficulty: 'easy', timeEstimate: '5-8 min', completed: false },
            { id: 'force_2', title: '3D Force Systems', difficulty: 'medium', timeEstimate: '12-18 min', completed: false },
            { id: 'force_3', title: 'Distributed Loads', difficulty: 'hard', timeEstimate: '25-35 min', completed: false }
          ]
        },
        {
          id: 'equilibrium',
          name: 'Equilibrium',
          problems: [
            { id: 'eq_1', title: '2D Equilibrium', difficulty: 'easy', timeEstimate: '8-12 min', completed: false },
            { id: 'eq_2', title: '3D Equilibrium', difficulty: 'medium', timeEstimate: '15-20 min', completed: false },
            { id: 'eq_3', title: 'Statically Indeterminate', difficulty: 'hard', timeEstimate: '30-45 min', completed: false }
          ]
        }
      ]
    },
    {
      id: 'dynamics',
      name: 'Dynamics',
      icon: TrendingUp,
      color: 'green',
      topics: [
        {
          id: 'kinematics',
          name: 'Kinematics',
          problems: [
            { id: 'kin_1', title: 'Rectilinear Motion', difficulty: 'easy', timeEstimate: '6-10 min', completed: false },
            { id: 'kin_2', title: 'Curvilinear Motion', difficulty: 'medium', timeEstimate: '12-18 min', completed: false },
            { id: 'kin_3', title: 'Relative Motion', difficulty: 'hard', timeEstimate: '20-30 min', completed: false }
          ]
        },
        {
          id: 'kinetics',
          name: 'Kinetics',
          problems: [
            { id: 'kinetics_1', title: 'Newton\'s Laws', difficulty: 'easy', timeEstimate: '8-12 min', completed: false },
            { id: 'kinetics_2', title: 'Work and Energy', difficulty: 'medium', timeEstimate: '15-22 min', completed: false },
            { id: 'kinetics_3', title: 'Impulse and Momentum', difficulty: 'hard', timeEstimate: '25-35 min', completed: false }
          ]
        }
      ]
    },
    {
      id: 'thermodynamics',
      name: 'Thermodynamics',
      icon: Target,
      color: 'red',
      topics: [
        {
          id: 'energy_analysis',
          name: 'Energy Analysis',
          problems: [
            { id: 'energy_1', title: 'First Law Applications', difficulty: 'easy', timeEstimate: '10-15 min', completed: false },
            { id: 'energy_2', title: 'Heat Engines', difficulty: 'medium', timeEstimate: '18-25 min', completed: false },
            { id: 'energy_3', title: 'Entropy Analysis', difficulty: 'hard', timeEstimate: '30-40 min', completed: false }
          ]
        }
      ]
    }
  ]

  const difficulties = [
    { id: 'all', name: 'All Levels', color: 'gray' },
    { id: 'easy', name: 'Beginner', color: 'green' },
    { id: 'medium', name: 'Intermediate', color: 'yellow' },
    { id: 'hard', name: 'Advanced', color: 'red' }
  ]

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'text-green-600 bg-green-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'hard': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getDifficultyIcon = (difficulty) => {
    switch (difficulty) {
      case 'easy': return <Star size={12} className="text-green-600" />
      case 'medium': return <Star size={12} className="text-yellow-600" />
      case 'hard': return <Star size={12} className="text-red-600" />
      default: return <Star size={12} className="text-gray-600" />
    }
  }

  const getSubjectColor = (subjectId) => {
    const subject = subjects.find(s => s.id === subjectId)
    return subject?.color || 'gray'
  }

  const filteredProblems = () => {
    const subject = subjects.find(s => s.id === selectedSubject)
    if (!subject) return []

    let problems = []
    subject.topics.forEach(topic => {
      problems.push(...topic.problems.map(problem => ({
        ...problem,
        topic: topic.name,
        topicId: topic.id
      })))
    })

    // Filter by difficulty
    if (selectedDifficulty !== 'all') {
      problems = problems.filter(p => p.difficulty === selectedDifficulty)
    }

    // Filter by search query
    if (searchQuery) {
      problems = problems.filter(p => 
        p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.topic.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    return problems
  }

  const handleProblemSelect = (problemId) => {
    navigate(`/problem/${problemId}`)
  }

  const getProgressStats = () => {
    const subject = subjects.find(s => s.id === selectedSubject)
    if (!subject) return { total: 0, completed: 0, percentage: 0 }

    let total = 0
    let completed = 0

    subject.topics.forEach(topic => {
      topic.problems.forEach(problem => {
        total++
        if (problem.completed) completed++
      })
    })

    return {
      total,
      completed,
      percentage: total > 0 ? Math.round((completed / total) * 100) : 0
    }
  }

  const progressStats = getProgressStats()

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Problem Library</h1>
        <p className="text-gray-600">Select a problem to practice with AI tutoring</p>
      </div>

      {/* Subject Selection */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {subjects.map((subject) => (
          <button
            key={subject.id}
            onClick={() => setSelectedSubject(subject.id)}
            className={`p-4 rounded-lg border-2 transition-all ${
              selectedSubject === subject.id
                ? `border-${subject.color}-500 bg-${subject.color}-50`
                : 'border-gray-200 hover:border-gray-300 bg-white'
            }`}
          >
            <div className="flex items-center space-x-3">
              <subject.icon size={24} className={`text-${subject.color}-600`} />
              <div className="text-left">
                <div className="font-medium text-gray-900">{subject.name}</div>
                <div className="text-sm text-gray-500">
                  {subject.topics.reduce((acc, topic) => acc + topic.problems.length, 0)} problems
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* Filters and Search */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search problems..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input-field"
          />
        </div>
        
        <div className="flex gap-2">
          {difficulties.map((difficulty) => (
            <button
              key={difficulty.id}
              onClick={() => setSelectedDifficulty(difficulty.id)}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedDifficulty === difficulty.id
                  ? `bg-${difficulty.color}-100 text-${difficulty.color}-700`
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {difficulty.name}
            </button>
          ))}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Progress</span>
          <span className="text-sm text-gray-500">
            {progressStats.completed} of {progressStats.total} completed
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progressStats.percentage}%` }}
          ></div>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          {progressStats.percentage}% complete
        </div>
      </div>

      {/* Problems Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredProblems().map((problem) => (
          <div
            key={problem.id}
            className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-2">
                {getDifficultyIcon(problem.difficulty)}
                <span className={`text-xs font-medium px-2 py-1 rounded ${getDifficultyColor(problem.difficulty)}`}>
                  {problem.difficulty}
                </span>
              </div>
              
              {problem.completed ? (
                <CheckCircle size={16} className="text-green-500" />
              ) : (
                <Lock size={16} className="text-gray-400" />
              )}
            </div>
            
            <h3 className="font-medium text-gray-900 mb-2">{problem.title}</h3>
            <p className="text-sm text-gray-600 mb-3">{problem.topic}</p>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-1 text-xs text-gray-500">
                <Clock size={12} />
                <span>{problem.timeEstimate}</span>
              </div>
              
              <button
                onClick={() => handleProblemSelect(problem.id)}
                disabled={problem.completed}
                className="btn-primary text-xs px-3 py-1 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {problem.completed ? 'Completed' : 'Start'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredProblems().length === 0 && (
        <div className="text-center py-12">
          <Award size={48} className="mx-auto mb-4 text-gray-300" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No problems found</h3>
          <p className="text-gray-600">
            Try adjusting your filters or search terms
          </p>
        </div>
      )}
    </div>
  )
}

export default ProblemSelector 