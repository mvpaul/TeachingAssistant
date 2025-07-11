/**
 * AI Engine Wrapper
 * Handles communication with OpenAI/Claude APIs and integrates with tutoring system
 */

import { misconceptionDetector } from '../utils/misconceptionDetector.js'
import { socraticFlowEngine } from '../utils/socraticFlowEngine.js'
import { sessionTracker } from '../utils/sessionTracker.js'

export class AIEngine {
  constructor(config = {}) {
    this.config = {
      apiEndpoint: config.apiEndpoint || '/api/ai',
      model: config.model || 'gpt-4o',
      maxTokens: config.maxTokens || 1000,
      temperature: config.temperature || 0.7,
      ...config
    }
    
    this.isProcessing = false
    this.retryCount = 0
    this.maxRetries = 3
  }

  /**
   * Analyze drawing using AI
   * @param {Object} drawingData - Canvas drawing data
   * @param {Object} context - Additional context (subject, topic, etc.)
   * @returns {Promise<Object>} Analysis result
   */
  async analyzeDrawing(drawingData, context = {}) {
    try {
      this.isProcessing = true
      
      // First, use local misconception detection
      const localAnalysis = misconceptionDetector.analyzeDrawing(
        drawingData, 
        context.subject || 'statics', 
        context.topic || 'free_body_diagrams'
      )

      // Record drawing submission
      sessionTracker.recordDrawingSubmission(drawingData)

      // If we have misconceptions, add them to session
      if (localAnalysis.length > 0) {
        sessionTracker.addMisconceptions(localAnalysis)
      }

      // Generate initial question
      const initialQuestion = socraticFlowEngine.generateInitialQuestion(
        context.subject || 'statics',
        context.topic || 'free_body_diagrams'
      )

      // Prepare for AI analysis if available
      const aiAnalysis = await this.callAI({
        type: 'analyze_drawing',
        drawingData,
        context,
        localAnalysis
      })

      return {
        success: true,
        misconceptions: localAnalysis,
        question: initialQuestion,
        aiAnalysis,
        confidence: misconceptionDetector.calculateConfidence(localAnalysis),
        suggestions: misconceptionDetector.getSuggestions(localAnalysis)
      }

    } catch (error) {
      console.error('Error analyzing drawing:', error)
      return {
        success: false,
        error: error.message,
        misconceptions: [],
        question: "I'm having trouble analyzing your drawing. Can you tell me what you're trying to represent?",
        confidence: 0
      }
    } finally {
      this.isProcessing = false
    }
  }

  /**
   * Process student response and generate follow-up
   * @param {string} response - Student's text response
   * @param {Object} context - Additional context
   * @returns {Promise<Object>} Response with follow-up question
   */
  async processResponse(response, context = {}) {
    try {
      this.isProcessing = true

      // Add user message to session
      sessionTracker.addMessage({
        type: 'user',
        content: response
      })

      // Analyze response for misconceptions
      const misconceptions = misconceptionDetector.analyzeTextResponse(
        response,
        context.subject || 'statics',
        context.topic || 'free_body_diagrams'
      )

      // Add new misconceptions to session
      if (misconceptions.length > 0) {
        sessionTracker.addMisconceptions(misconceptions)
      }

      // Generate follow-up question
      const questionStrategy = socraticFlowEngine.analyzeResponse(
        response,
        misconceptions,
        context.subject || 'statics',
        context.topic || 'free_body_diagrams'
      )

      // Get AI response if available
      const aiResponse = await this.callAI({
        type: 'process_response',
        response,
        misconceptions,
        questionStrategy,
        context
      })

      // Add AI message to session
      sessionTracker.addMessage({
        type: 'ai',
        content: aiResponse?.question || questionStrategy.question,
        data: {
          strategy: questionStrategy.strategy,
          misconceptions: misconceptions
        }
      })

      return {
        success: true,
        question: aiResponse?.question || questionStrategy.question,
        feedback: aiResponse?.feedback || socraticFlowEngine.generateFeedback(response, misconceptions),
        misconceptions,
        strategy: questionStrategy.strategy,
        confidence: misconceptionDetector.calculateConfidence(misconceptions)
      }

    } catch (error) {
      console.error('Error processing response:', error)
      return {
        success: false,
        error: error.message,
        question: "I'm having trouble processing your response. Can you try rephrasing?",
        misconceptions: []
      }
    } finally {
      this.isProcessing = false
    }
  }

  /**
   * Call AI API with retry logic
   * @param {Object} payload - Request payload
   * @returns {Promise<Object>} AI response
   */
  async callAI(payload) {
    // For now, return null to use local processing
    // In production, this would make actual API calls
    return null

    // Example implementation for when API is available:
    /*
    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        const response = await fetch(this.config.apiEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.config.apiKey}`
          },
          body: JSON.stringify({
            model: this.config.model,
            max_tokens: this.config.maxTokens,
            temperature: this.config.temperature,
            ...payload
          })
        })

        if (!response.ok) {
          throw new Error(`API request failed: ${response.status}`)
        }

        const data = await response.json()
        this.retryCount = 0
        return data

      } catch (error) {
        this.retryCount = attempt + 1
        console.warn(`AI API attempt ${attempt + 1} failed:`, error)
        
        if (attempt === this.maxRetries - 1) {
          throw error
        }
        
        // Wait before retrying
        await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)))
      }
    }
    */
  }

  /**
   * Generate visual scaffolding suggestions
   * @param {Array} misconceptions - Detected misconceptions
   * @param {Object} context - Additional context
   * @returns {Promise<Object>} Visual suggestions
   */
  async generateVisualScaffolding(misconceptions, context = {}) {
    try {
      const suggestions = []

      misconceptions.forEach(misconception => {
        switch (misconception.type) {
          case 'missing_force_vectors':
            suggestions.push({
              type: 'drawing',
              instruction: 'Draw arrows to represent each force',
              example: 'Add force vectors pointing in the correct directions',
              priority: 'high'
            })
            break
          case 'missing_object_boundary':
            suggestions.push({
              type: 'drawing',
              instruction: 'Define the object boundary',
              example: 'Draw a dashed line around the object',
              priority: 'medium'
            })
            break
          case 'incorrect_force_direction':
            suggestions.push({
              type: 'feedback',
              instruction: 'Check force directions',
              example: 'Review the direction of each force vector',
              priority: 'high'
            })
            break
        }
      })

      return {
        success: true,
        suggestions,
        count: suggestions.length
      }

    } catch (error) {
      console.error('Error generating visual scaffolding:', error)
      return {
        success: false,
        error: error.message,
        suggestions: []
      }
    }
  }

  /**
   * Get session summary and recommendations
   * @returns {Object} Session summary with AI recommendations
   */
  getSessionSummary() {
    const session = sessionTracker.getCurrentSession()
    if (!session) return null

    const stats = sessionTracker.getSessionStats()
    const activeMisconceptions = sessionTracker.getActiveMisconceptions()

    return {
      sessionId: session.id,
      duration: stats.duration,
      progress: stats.progress,
      misconceptions: {
        total: stats.misconceptionCount,
        addressed: stats.addressedMisconceptionCount,
        active: activeMisconceptions.length
      },
      recommendations: this.generateRecommendations(stats, activeMisconceptions),
      nextSteps: this.suggestNextSteps(stats, activeMisconceptions)
    }
  }

  /**
   * Generate recommendations based on session data
   * @param {Object} stats - Session statistics
   * @param {Array} activeMisconceptions - Active misconceptions
   * @returns {Array} Array of recommendations
   */
  generateRecommendations(stats, activeMisconceptions) {
    const recommendations = []

    if (activeMisconceptions.length > 0) {
      recommendations.push({
        type: 'misconception',
        priority: 'high',
        message: `Address ${activeMisconceptions.length} remaining misconception(s)`,
        action: 'review_misconceptions'
      })
    }

    if (stats.drawingCount < 2) {
      recommendations.push({
        type: 'practice',
        priority: 'medium',
        message: 'Practice with more drawings to improve understanding',
        action: 'draw_more'
      })
    }

    if (stats.userMessageCount < 3) {
      recommendations.push({
        type: 'engagement',
        priority: 'medium',
        message: 'Engage more with the AI tutor for better learning',
        action: 'ask_questions'
      })
    }

    return recommendations
  }

  /**
   * Suggest next steps for the student
   * @param {Object} stats - Session statistics
   * @param {Array} activeMisconceptions - Active misconceptions
   * @returns {Array} Array of next steps
   */
  suggestNextSteps(stats, activeMisconceptions) {
    const steps = []

    if (activeMisconceptions.length > 0) {
      steps.push('Review and address misconceptions')
    }

    steps.push('Practice with similar problems')
    steps.push('Try more complex scenarios')

    return steps
  }

  /**
   * Check if AI engine is currently processing
   * @returns {boolean} Processing status
   */
  getProcessingStatus() {
    return this.isProcessing
  }

  /**
   * Reset retry count
   */
  resetRetryCount() {
    this.retryCount = 0
  }
}

// Export singleton instance
export const aiEngine = new AIEngine() 