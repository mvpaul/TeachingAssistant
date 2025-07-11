/**
 * Misconception Detection Engine
 * Analyzes drawings and student responses to identify common misconceptions
 */

export class MisconceptionDetector {
  constructor() {
    this.misconceptions = {
      statics: {
        'missing_force_vectors': {
          pattern: /force|vector|arrow/i,
          severity: 'high',
          message: 'Missing force vectors in free body diagram',
          suggestion: 'Draw arrows to represent each force acting on the object'
        },
        'missing_normal_force': {
          pattern: /normal|contact|surface/i,
          severity: 'medium',
          message: 'Missing normal force from surface contact',
          suggestion: 'Include the normal force perpendicular to the surface'
        },
        'incorrect_force_direction': {
          pattern: /direction|pointing|arrow/i,
          severity: 'high',
          message: 'Incorrect force direction',
          suggestion: 'Check the direction of each force vector'
        },
        'overcomplicated_diagram': {
          pattern: /too many|complicated|complex/i,
          severity: 'low',
          message: 'Overcomplicated free body diagram',
          suggestion: 'Focus on essential forces only'
        }
      },
      dynamics: {
        'missing_acceleration': {
          pattern: /acceleration|motion|movement/i,
          severity: 'high',
          message: 'Missing acceleration consideration',
          suggestion: 'Consider the object\'s acceleration in your analysis'
        },
        'ignoring_friction': {
          pattern: /friction|smooth|frictionless/i,
          severity: 'medium',
          message: 'Ignoring friction effects',
          suggestion: 'Include friction forces if they are significant'
        }
      }
    }
  }

  /**
   * Analyze drawing data for misconceptions
   * @param {Object} drawingData - Canvas drawing data
   * @param {string} subject - Subject area (statics, dynamics, etc.)
   * @param {string} topic - Specific topic
   * @returns {Array} Array of detected misconceptions
   */
  analyzeDrawing(drawingData, subject = 'statics', topic = 'free_body_diagrams') {
    const detected = []
    const subjectMisconceptions = this.misconceptions[subject] || {}

    // Analyze drawing characteristics
    const characteristics = this.extractDrawingCharacteristics(drawingData)
    
    // Check for missing force vectors
    if (characteristics.lineCount < 2 && subject === 'statics') {
      detected.push({
        type: 'missing_force_vectors',
        ...subjectMisconceptions['missing_force_vectors'],
        confidence: 0.8
      })
    }

    // Check for missing object boundary
    if (characteristics.circleCount === 0 && characteristics.rectCount === 0) {
      detected.push({
        type: 'missing_object_boundary',
        severity: 'medium',
        message: 'Missing object boundary definition',
        suggestion: 'Clearly define the object\'s boundary',
        confidence: 0.7
      })
    }

    // Check for overcomplicated diagrams
    if (characteristics.totalObjects > 10) {
      detected.push({
        type: 'overcomplicated_diagram',
        ...subjectMisconceptions['overcomplicated_diagram'],
        confidence: 0.6
      })
    }

    return detected
  }

  /**
   * Analyze text response for misconceptions
   * @param {string} response - Student's text response
   * @param {string} subject - Subject area
   * @param {string} topic - Specific topic
   * @returns {Array} Array of detected misconceptions
   */
  analyzeTextResponse(response, subject = 'statics', topic = 'free_body_diagrams') {
    const detected = []
    const subjectMisconceptions = this.misconceptions[subject] || {}
    const lowerResponse = response.toLowerCase()

    // Check each misconception pattern
    Object.entries(subjectMisconceptions).forEach(([key, misconception]) => {
      if (misconception.pattern.test(lowerResponse)) {
        detected.push({
          type: key,
          ...misconception,
          confidence: 0.7
        })
      }
    })

    return detected
  }

  /**
   * Extract characteristics from drawing data
   * @param {Object} drawingData - Canvas drawing data
   * @returns {Object} Drawing characteristics
   */
  extractDrawingCharacteristics(drawingData) {
    if (!drawingData || !drawingData.objects) {
      return {
        lineCount: 0,
        circleCount: 0,
        rectCount: 0,
        textCount: 0,
        totalObjects: 0
      }
    }

    const objects = drawingData.objects
    return {
      lineCount: objects.filter(obj => obj.type === 'line').length,
      circleCount: objects.filter(obj => obj.type === 'circle').length,
      rectCount: objects.filter(obj => obj.type === 'rect').length,
      textCount: objects.filter(obj => obj.type === 'text').length,
      totalObjects: objects.length
    }
  }

  /**
   * Get suggestions for addressing misconceptions
   * @param {Array} misconceptions - Array of detected misconceptions
   * @returns {Array} Array of suggestions
   */
  getSuggestions(misconceptions) {
    return misconceptions.map(misconception => ({
      type: misconception.type,
      message: misconception.message,
      suggestion: misconception.suggestion,
      severity: misconception.severity
    }))
  }

  /**
   * Calculate overall confidence in misconception detection
   * @param {Array} misconceptions - Array of detected misconceptions
   * @returns {number} Confidence score (0-1)
   */
  calculateConfidence(misconceptions) {
    if (misconceptions.length === 0) return 0
    
    const totalConfidence = misconceptions.reduce((sum, m) => sum + (m.confidence || 0.5), 0)
    return Math.min(totalConfidence / misconceptions.length, 1)
  }
}

// Export singleton instance
export const misconceptionDetector = new MisconceptionDetector() 