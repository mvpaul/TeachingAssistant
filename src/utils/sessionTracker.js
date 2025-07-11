/**
 * Session Tracker
 * Maintains conversation state and tracks student progress
 */

export class SessionTracker {
  constructor() {
    this.sessions = new Map()
    this.currentSessionId = null
  }

  /**
   * Create a new session
   * @param {string} sessionId - Unique session identifier
   * @param {Object} config - Session configuration
   * @returns {Object} Session object
   */
  createSession(sessionId, config = {}) {
    const session = {
      id: sessionId,
      createdAt: new Date(),
      lastActivity: new Date(),
      subject: config.subject || 'statics',
      topic: config.topic || 'free_body_diagrams',
      messages: [],
      misconceptions: [],
      progress: {
        questionsAnswered: 0,
        misconceptionsAddressed: 0,
        drawingsSubmitted: 0,
        timeSpent: 0
      },
      state: {
        currentStep: 'initial',
        confidence: 0,
        difficulty: 'medium'
      },
      metadata: {
        userAgent: navigator.userAgent,
        screenSize: `${window.screen.width}x${window.screen.height}`,
        ...config.metadata
      }
    }

    this.sessions.set(sessionId, session)
    this.currentSessionId = sessionId
    return session
  }

  /**
   * Get current session
   * @returns {Object|null} Current session or null
   */
  getCurrentSession() {
    if (!this.currentSessionId) return null
    return this.sessions.get(this.currentSessionId)
  }

  /**
   * Add a message to the current session
   * @param {Object} message - Message object
   */
  addMessage(message) {
    const session = this.getCurrentSession()
    if (!session) return

    const messageWithMetadata = {
      ...message,
      timestamp: new Date(),
      id: `${session.id}-${session.messages.length + 1}`
    }

    session.messages.push(messageWithMetadata)
    session.lastActivity = new Date()
    session.progress.questionsAnswered += message.type === 'user' ? 1 : 0
  }

  /**
   * Add misconceptions to the session
   * @param {Array} misconceptions - Array of misconception objects
   */
  addMisconceptions(misconceptions) {
    const session = this.getCurrentSession()
    if (!session) return

    session.misconceptions.push(...misconceptions.map(m => ({
      ...m,
      timestamp: new Date(),
      addressed: false
    })))

    session.progress.misconceptionsAddressed += misconceptions.length
  }

  /**
   * Mark misconceptions as addressed
   * @param {Array} misconceptionIds - Array of misconception IDs to mark as addressed
   */
  markMisconceptionsAddressed(misconceptionIds) {
    const session = this.getCurrentSession()
    if (!session) return

    session.misconceptions.forEach(misconception => {
      if (misconceptionIds.includes(misconception.id)) {
        misconception.addressed = true
        misconception.addressedAt = new Date()
      }
    })
  }

  /**
   * Update session state
   * @param {Object} stateUpdate - State update object
   */
  updateState(stateUpdate) {
    const session = this.getCurrentSession()
    if (!session) return

    session.state = { ...session.state, ...stateUpdate }
    session.lastActivity = new Date()
  }

  /**
   * Record drawing submission
   * @param {Object} drawingData - Drawing data object
   */
  recordDrawingSubmission(drawingData) {
    const session = this.getCurrentSession()
    if (!session) return

    session.progress.drawingsSubmitted += 1
    
    this.addMessage({
      type: 'system',
      content: 'Drawing submitted for analysis',
      data: {
        drawingObjects: drawingData.objects?.length || 0,
        drawingType: this.classifyDrawing(drawingData)
      }
    })
  }

  /**
   * Classify drawing type based on content
   * @param {Object} drawingData - Drawing data
   * @returns {string} Drawing classification
   */
  classifyDrawing(drawingData) {
    if (!drawingData.objects) return 'empty'

    const objects = drawingData.objects
    const lineCount = objects.filter(obj => obj.type === 'line').length
    const circleCount = objects.filter(obj => obj.type === 'circle').length
    const rectCount = objects.filter(obj => obj.type === 'rect').length
    const textCount = objects.filter(obj => obj.type === 'text').length

    if (textCount > 0) return 'text_and_diagram'
    if (lineCount > 5) return 'complex_diagram'
    if (lineCount > 2) return 'simple_diagram'
    if (circleCount > 0 || rectCount > 0) return 'geometric'
    
    return 'sketch'
  }

  /**
   * Calculate session statistics
   * @param {string} sessionId - Session ID (optional, uses current if not provided)
   * @returns {Object} Session statistics
   */
  getSessionStats(sessionId = null) {
    const session = sessionId ? this.sessions.get(sessionId) : this.getCurrentSession()
    if (!session) return null

    const duration = new Date() - session.createdAt
    const userMessages = session.messages.filter(m => m.type === 'user')
    const aiMessages = session.messages.filter(m => m.type === 'ai')
    const addressedMisconceptions = session.misconceptions.filter(m => m.addressed)

    return {
      duration: Math.round(duration / 1000), // seconds
      messageCount: session.messages.length,
      userMessageCount: userMessages.length,
      aiMessageCount: aiMessages.length,
      misconceptionCount: session.misconceptions.length,
      addressedMisconceptionCount: addressedMisconceptions.length,
      drawingCount: session.progress.drawingsSubmitted,
      averageResponseTime: this.calculateAverageResponseTime(session),
      progress: session.progress,
      state: session.state
    }
  }

  /**
   * Calculate average response time between user and AI messages
   * @param {Object} session - Session object
   * @returns {number} Average response time in seconds
   */
  calculateAverageResponseTime(session) {
    const userMessages = session.messages.filter(m => m.type === 'user')
    const aiMessages = session.messages.filter(m => m.type === 'ai')
    
    if (userMessages.length === 0 || aiMessages.length === 0) return 0

    let totalTime = 0
    let responseCount = 0

    userMessages.forEach((userMsg, index) => {
      const nextAiMsg = aiMessages[index]
      if (nextAiMsg && nextAiMsg.timestamp > userMsg.timestamp) {
        totalTime += nextAiMsg.timestamp - userMsg.timestamp
        responseCount += 1
      }
    })

    return responseCount > 0 ? Math.round(totalTime / responseCount / 1000) : 0
  }

  /**
   * Get conversation history
   * @param {string} sessionId - Session ID (optional, uses current if not provided)
   * @returns {Array} Array of messages
   */
  getConversationHistory(sessionId = null) {
    const session = sessionId ? this.sessions.get(sessionId) : this.getCurrentSession()
    return session ? session.messages : []
  }

  /**
   * Get active misconceptions
   * @param {string} sessionId - Session ID (optional, uses current if not provided)
   * @returns {Array} Array of unaddressed misconceptions
   */
  getActiveMisconceptions(sessionId = null) {
    const session = sessionId ? this.sessions.get(sessionId) : this.getCurrentSession()
    return session ? session.misconceptions.filter(m => !m.addressed) : []
  }

  /**
   * Export session data
   * @param {string} sessionId - Session ID (optional, uses current if not provided)
   * @returns {Object} Session export data
   */
  exportSession(sessionId = null) {
    const session = sessionId ? this.sessions.get(sessionId) : this.getCurrentSession()
    if (!session) return null

    return {
      ...session,
      stats: this.getSessionStats(session.id),
      exportDate: new Date()
    }
  }

  /**
   * Clear session data
   * @param {string} sessionId - Session ID (optional, uses current if not provided)
   */
  clearSession(sessionId = null) {
    const id = sessionId || this.currentSessionId
    if (id) {
      this.sessions.delete(id)
      if (this.currentSessionId === id) {
        this.currentSessionId = null
      }
    }
  }

  /**
   * Get all sessions
   * @returns {Array} Array of all sessions
   */
  getAllSessions() {
    return Array.from(this.sessions.values())
  }
}

// Export singleton instance
export const sessionTracker = new SessionTracker() 