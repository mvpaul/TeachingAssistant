/**
 * Socratic Flow Engine
 * Generates contextual follow-up questions based on student responses and misconceptions
 */

export class SocraticFlowEngine {
  constructor() {
    this.questionTemplates = {
      statics: {
        free_body_diagrams: {
          initial: [
            "What forces are acting on this object?",
            "Can you identify all the forces in your diagram?",
            "What is the object you're analyzing?"
          ],
          follow_up: {
            missing_force_vectors: [
              "I notice you haven't drawn many force vectors. What forces do you think are acting on this object?",
              "Can you add arrows to represent the forces you mentioned?",
              "Which direction do you think each force is pointing?"
            ],
            missing_normal_force: [
              "Is the object in contact with any surface?",
              "What force prevents the object from falling through the surface?",
              "Can you draw the normal force from the surface?"
            ],
            incorrect_force_direction: [
              "Let's think about the direction of each force. Which way does gravity pull?",
              "If the object is on a surface, which way does the normal force point?",
              "Are you sure about the direction of that force vector?"
            ]
          },
          progression: [
            "Now that we have the forces, what is the net force?",
            "Is the object in equilibrium? How can you tell?",
            "What equations can you write to solve for the unknown forces?"
          ]
        },
        force_analysis: {
          initial: [
            "What is the magnitude of each force?",
            "Can you write the force balance equations?",
            "What is the direction of the net force?"
          ],
          follow_up: {
            missing_acceleration: [
              "Is the object moving or stationary?",
              "If it's moving, what about acceleration?",
              "How does acceleration affect the force balance?"
            ]
          }
        }
      },
      dynamics: {
        motion_analysis: {
          initial: [
            "What type of motion is this?",
            "Is there acceleration? In which direction?",
            "What forces cause this motion?"
          ]
        }
      }
    }

    this.responsePatterns = {
      force_mention: /force|weight|gravity|normal|friction/i,
      direction_mention: /direction|pointing|up|down|left|right/i,
      magnitude_mention: /magnitude|size|how much|calculate/i,
      equation_mention: /equation|formula|solve|calculate/i
    }
  }

  /**
   * Generate initial question based on subject and topic
   * @param {string} subject - Subject area
   * @param {string} topic - Specific topic
   * @returns {string} Initial question
   */
  generateInitialQuestion(subject = 'statics', topic = 'free_body_diagrams') {
    const templates = this.questionTemplates[subject]?.[topic]
    if (!templates || !templates.initial) {
      return "What are you trying to analyze in this diagram?"
    }

    const questions = templates.initial
    return questions[Math.floor(Math.random() * questions.length)]
  }

  /**
   * Generate follow-up question based on misconceptions
   * @param {Array} misconceptions - Detected misconceptions
   * @param {string} subject - Subject area
   * @param {string} topic - Specific topic
   * @returns {string} Follow-up question
   */
  generateFollowUpQuestion(misconceptions, subject = 'statics', topic = 'free_body_diagrams') {
    if (!misconceptions || misconceptions.length === 0) {
      return this.generateProgressionQuestion(subject, topic)
    }

    const templates = this.questionTemplates[subject]?.[topic]?.follow_up
    if (!templates) {
      return "Can you explain your reasoning a bit more?"
    }

    // Find the highest severity misconception
    const highestSeverity = misconceptions.reduce((highest, current) => {
      const severityOrder = { high: 3, medium: 2, low: 1 }
      return severityOrder[current.severity] > severityOrder[highest.severity] ? current : highest
    })

    const followUpQuestions = templates[highestSeverity.type]
    if (followUpQuestions && followUpQuestions.length > 0) {
      return followUpQuestions[Math.floor(Math.random() * followUpQuestions.length)]
    }

    return "Can you elaborate on that?"
  }

  /**
   * Generate progression question for advanced students
   * @param {string} subject - Subject area
   * @param {string} topic - Specific topic
   * @returns {string} Progression question
   */
  generateProgressionQuestion(subject = 'statics', topic = 'free_body_diagrams') {
    const templates = this.questionTemplates[subject]?.[topic]
    if (!templates || !templates.progression) {
      return "What's the next step in your analysis?"
    }

    const questions = templates.progression
    return questions[Math.floor(Math.random() * questions.length)]
  }

  /**
   * Analyze student response to determine next question type
   * @param {string} response - Student's text response
   * @param {Array} misconceptions - Previously detected misconceptions
   * @param {string} subject - Subject area
   * @param {string} topic - Specific topic
   * @returns {Object} Question generation strategy
   */
  analyzeResponse(response, misconceptions = [], subject = 'statics', topic = 'free_body_diagrams') {
    const lowerResponse = response.toLowerCase()
    
    // Check response patterns
    const patterns = {
      mentionsForces: this.responsePatterns.force_mention.test(lowerResponse),
      mentionsDirection: this.responsePatterns.direction_mention.test(lowerResponse),
      mentionsMagnitude: this.responsePatterns.magnitude_mention.test(lowerResponse),
      mentionsEquations: this.responsePatterns.equation_mention.test(lowerResponse)
    }

    // Determine question strategy
    if (misconceptions.length > 0) {
      return {
        type: 'follow_up',
        question: this.generateFollowUpQuestion(misconceptions, subject, topic),
        strategy: 'address_misconception'
      }
    }

    if (patterns.mentionsEquations) {
      return {
        type: 'progression',
        question: this.generateProgressionQuestion(subject, topic),
        strategy: 'advance_to_calculation'
      }
    }

    if (patterns.mentionsMagnitude) {
      return {
        type: 'progression',
        question: "Great! Now can you write the equations to solve for these magnitudes?",
        strategy: 'advance_to_equations'
      }
    }

    if (patterns.mentionsDirection) {
      return {
        type: 'progression',
        question: "Excellent! Now what about the magnitudes of these forces?",
        strategy: 'advance_to_magnitudes'
      }
    }

    if (patterns.mentionsForces) {
      return {
        type: 'progression',
        question: "Good! Now let's think about the direction of each force. Which way does each force point?",
        strategy: 'advance_to_directions'
      }
    }

    return {
      type: 'follow_up',
      question: "Can you tell me more about what you're thinking?",
      strategy: 'elicit_more_information'
    }
  }

  /**
   * Generate contextual feedback based on response quality
   * @param {string} response - Student's response
   * @param {Array} misconceptions - Detected misconceptions
   * @returns {string} Contextual feedback
   */
  generateFeedback(response, misconceptions = []) {
    if (misconceptions.length === 0) {
      return "Excellent work! Your analysis is on the right track."
    }

    const highSeverity = misconceptions.filter(m => m.severity === 'high')
    if (highSeverity.length > 0) {
      return "I see a few important points we should address. Let's work through this step by step."
    }

    return "Good start! There are a couple of things we can improve. Let's refine your approach."
  }

  /**
   * Get question bank for a specific topic
   * @param {string} subject - Subject area
   * @param {string} topic - Specific topic
   * @returns {Array} Array of question templates
   */
  getQuestionBank(subject = 'statics', topic = 'free_body_diagrams') {
    const templates = this.questionTemplates[subject]?.[topic]
    if (!templates) return []

    return {
      initial: templates.initial || [],
      followUp: templates.follow_up ? Object.values(templates.follow_up).flat() : [],
      progression: templates.progression || []
    }
  }
}

// Export singleton instance
export const socraticFlowEngine = new SocraticFlowEngine() 