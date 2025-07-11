"""
Socratic Engine Module

This module generates progressive questioning sequences that guide students toward
self-discovery without providing direct answers. It follows branching logic trees
to challenge faulty reasoning and build conceptual understanding.
"""

import uuid
from typing import List, Dict, Any, Optional
from .models import SocraticQuestion, QuestionType, Difficulty, Misconception, Subject


class SocraticEngine:
    """
    Generates Socratic questions to guide student learning.
    
    This engine:
    - Creates progressive questioning sequences
    - Follows branching logic based on student responses
    - Challenges assumptions without giving answers
    - Adapts question difficulty based on student progress
    """
    
    def __init__(self):
        self.question_templates = self._initialize_question_templates()
        self.question_sequences = self._initialize_question_sequences()
        self.follow_up_strategies = self._initialize_follow_up_strategies()
    
    def generate_question(self, 
                         problem_subject: Subject,
                         problem_topic: str,
                         detected_misconceptions: List[Misconception],
                         conversation_history: List[Dict[str, Any]],
                         current_stage: str = "initial") -> SocraticQuestion:
        """
        Generate a Socratic question based on the current context.
        
        Args:
            problem_subject: The subject being studied
            problem_topic: The specific topic within the subject
            detected_misconceptions: Any misconceptions detected in student response
            conversation_history: Previous conversation turns
            current_stage: Current stage in the problem-solving process
            
        Returns:
            A Socratic question designed to guide the student
        """
        # Determine question type based on context
        question_type = self._determine_question_type(
            detected_misconceptions, current_stage, conversation_history
        )
        
        # Generate question text
        question_text = self._generate_question_text(
            question_type, problem_subject, problem_topic, detected_misconceptions
        )
        
        # Determine target concept
        target_concept = self._determine_target_concept(
            detected_misconceptions, current_stage, problem_topic
        )
        
        # Generate follow-up questions
        follow_up_questions = self._generate_follow_up_questions(
            question_type, problem_subject, problem_topic
        )
        
        # Determine expected insights
        expected_insights = self._determine_expected_insights(
            question_type, target_concept, detected_misconceptions
        )
        
        return SocraticQuestion(
            id=str(uuid.uuid4()),
            question_text=question_text,
            question_type=question_type,
            target_concept=target_concept,
            follow_up_questions=follow_up_questions,
            expected_insights=expected_insights,
            difficulty_level=self._determine_difficulty_level(conversation_history)
        )
    
    def _initialize_question_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize question templates for different subjects and topics."""
        return {
            Subject.STATICS: {
                "distributed_loads": {
                    QuestionType.CLARIFICATION: [
                        "What forces are acting on the beam?",
                        "How would you represent the distributed load in a free body diagram?",
                        "What do you think happens to the distributed load when calculating reactions?"
                    ],
                    QuestionType.ASSUMPTION_CHALLENGE: [
                        "Why do you think the reaction force is in that direction?",
                        "What assumptions are you making about the load distribution?",
                        "How do you know that's the correct sign convention?"
                    ],
                    QuestionType.CONCEPTUAL: [
                        "What is the difference between a point load and a distributed load?",
                        "How does the location of the equivalent point load affect the moment calculation?",
                        "What would happen if the distributed load wasn't uniform?"
                    ],
                    QuestionType.CALCULATION_CHECK: [
                        "How did you arrive at that value for the reaction force?",
                        "What units are you using in your calculations?",
                        "Can you walk through your integration step by step?"
                    ],
                    QuestionType.VISUAL_AID: [
                        "Can you sketch a free body diagram showing all the forces?",
                        "Where would you place the equivalent point load on your diagram?",
                        "How would you represent the distributed load visually?"
                    ]
                },
                "general_statics": {
                    QuestionType.CLARIFICATION: [
                        "What are the conditions for static equilibrium?",
                        "Which forces are external and which are internal?",
                        "What coordinate system are you using?"
                    ],
                    QuestionType.ASSUMPTION_CHALLENGE: [
                        "Why do you think the system is in equilibrium?",
                        "What assumptions are you making about the supports?",
                        "How do you know that force balance is sufficient?"
                    ]
                }
            },
            Subject.CIRCUIT_ANALYSIS: {
                "kirchhoff_laws": {
                    QuestionType.CLARIFICATION: [
                        "What is the current flowing into and out of this node?",
                        "How many independent loops can you identify in this circuit?",
                        "What is the voltage drop across each component?"
                    ],
                    QuestionType.ASSUMPTION_CHALLENGE: [
                        "Why did you choose that direction for the current?",
                        "What assumptions are you making about the voltage polarities?",
                        "How do you know that's the correct reference direction?"
                    ],
                    QuestionType.CONCEPTUAL: [
                        "What does Kirchhoff's Current Law tell us about node currents?",
                        "How does Kirchhoff's Voltage Law apply to this loop?",
                        "What is the relationship between current and voltage in a resistor?"
                    ]
                }
            }
        }
    
    def _initialize_question_sequences(self) -> Dict[str, List[str]]:
        """Initialize logical sequences of questions for different scenarios."""
        return {
            "force_direction_error": [
                "clarification",
                "assumption_challenge", 
                "visual_aid",
                "conceptual"
            ],
            "missing_reactions": [
                "clarification",
                "visual_aid",
                "conceptual",
                "calculation_check"
            ],
            "sign_convention_error": [
                "clarification",
                "assumption_challenge",
                "conceptual"
            ],
            "integration_error": [
                "clarification",
                "conceptual",
                "calculation_check"
            ]
        }
    
    def _initialize_follow_up_strategies(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize follow-up strategies for different question types."""
        return {
            QuestionType.CLARIFICATION: {
                "if_unclear": [
                    "Can you be more specific about what you mean?",
                    "What exactly are you referring to when you say that?",
                    "Could you give me an example of what you're thinking?"
                ],
                "if_incorrect": [
                    "Let me ask this differently...",
                    "What if we looked at it from another angle?",
                    "Have you considered what happens if..."
                ]
            },
            QuestionType.ASSUMPTION_CHALLENGE: {
                "if_defensive": [
                    "I'm not saying you're wrong, I'm just curious about your reasoning...",
                    "What evidence supports that assumption?",
                    "How could we test whether that assumption is valid?"
                ],
                "if_uncertain": [
                    "What makes you think that might be the case?",
                    "What would happen if that assumption wasn't true?",
                    "Can you think of a situation where that might not apply?"
                ]
            }
        }
    
    def _determine_question_type(self, misconceptions: List[Misconception], 
                               current_stage: str, 
                               conversation_history: List[Dict[str, Any]]) -> QuestionType:
        """Determine the most appropriate question type based on context."""
        
        # If there are critical misconceptions, focus on clarification and assumption challenge
        critical_misconceptions = [m for m in misconceptions if m.severity.value == "critical"]
        if critical_misconceptions:
            return QuestionType.ASSUMPTION_CHALLENGE
        
        # If student seems confused, start with clarification
        if current_stage == "initial" or len(conversation_history) < 2:
            return QuestionType.CLARIFICATION
        
        # If previous question was clarification, move to conceptual
        if conversation_history and "question_type" in conversation_history[-1]:
            last_question_type = conversation_history[-1]["question_type"]
            if last_question_type == QuestionType.CLARIFICATION:
                return QuestionType.CONCEPTUAL
        
        # Default to conceptual questions
        return QuestionType.CONCEPTUAL
    
    def _generate_question_text(self, question_type: QuestionType, 
                              subject: Subject, topic: str, 
                              misconceptions: List[Misconception]) -> str:
        """Generate the actual question text based on type and context."""
        
        if subject in self.question_templates and topic in self.question_templates[subject]:
            topic_templates = self.question_templates[subject][topic]
            
            if question_type in topic_templates:
                templates = topic_templates[question_type]
                
                # For now, return the first template. In a real implementation,
                # this would use more sophisticated selection logic
                return templates[0]
        
        # Fallback templates
        fallback_templates = {
            QuestionType.CLARIFICATION: "Can you explain your approach to this problem?",
            QuestionType.ASSUMPTION_CHALLENGE: "What assumptions are you making in your analysis?",
            QuestionType.CONCEPTUAL: "What fundamental principles apply to this situation?",
            QuestionType.CALCULATION_CHECK: "How did you arrive at that result?",
            QuestionType.VISUAL_AID: "Can you draw a diagram to help visualize this?"
        }
        
        return fallback_templates.get(question_type, "What do you think about this?")
    
    def _determine_target_concept(self, misconceptions: List[Misconception], 
                                current_stage: str, topic: str) -> str:
        """Determine which concept the question should target."""
        
        if misconceptions:
            # Target the most critical misconception
            critical_misconceptions = [m for m in misconceptions if m.severity.value == "critical"]
            if critical_misconceptions:
                return critical_misconceptions[0].related_concepts[0]
        
        # Default to the current topic
        return topic
    
    def _generate_follow_up_questions(self, question_type: QuestionType, 
                                    subject: Subject, topic: str) -> List[str]:
        """Generate potential follow-up questions."""
        
        if question_type in self.follow_up_strategies:
            strategies = self.follow_up_strategies[question_type]
            follow_ups = []
            
            for strategy, questions in strategies.items():
                follow_ups.extend(questions[:1])  # Take first question from each strategy
            
            return follow_ups
        
        return []
    
    def _determine_expected_insights(self, question_type: QuestionType, 
                                   target_concept: str, 
                                   misconceptions: List[Misconception]) -> List[str]:
        """Determine what insights the student should gain from the question."""
        
        insights = []
        
        if question_type == QuestionType.CLARIFICATION:
            insights.append(f"Student should articulate their understanding of {target_concept}")
        
        elif question_type == QuestionType.ASSUMPTION_CHALLENGE:
            insights.append("Student should question their initial assumptions")
            insights.append("Student should consider alternative approaches")
        
        elif question_type == QuestionType.CONCEPTUAL:
            insights.append(f"Student should connect {target_concept} to fundamental principles")
            insights.append("Student should recognize underlying patterns")
        
        elif question_type == QuestionType.CALCULATION_CHECK:
            insights.append("Student should verify their mathematical approach")
            insights.append("Student should check units and signs")
        
        elif question_type == QuestionType.VISUAL_AID:
            insights.append("Student should create a visual representation")
            insights.append("Student should identify key elements in the diagram")
        
        return insights
    
    def _determine_difficulty_level(self, conversation_history: List[Dict[str, Any]]) -> Difficulty:
        """Determine appropriate difficulty level based on conversation history."""
        
        if len(conversation_history) < 2:
            return Difficulty.BEGINNER
        
        # Check if student is struggling
        recent_responses = conversation_history[-3:]  # Last 3 responses
        struggling_indicators = ["unsure", "confused", "don't know", "not sure"]
        
        for response in recent_responses:
            if "student_input" in response:
                student_text = response["student_input"].lower()
                if any(indicator in student_text for indicator in struggling_indicators):
                    return Difficulty.BEGINNER
        
        # Check if student is making progress
        if len(conversation_history) > 5:
            return Difficulty.INTERMEDIATE
        
        return Difficulty.BEGINNER
    
    def adapt_question_strategy(self, student_response: str, 
                              previous_question: SocraticQuestion) -> QuestionType:
        """Adapt the questioning strategy based on student response."""
        
        response_lower = student_response.lower()
        
        # If student is defensive or confused, use clarification
        if any(word in response_lower for word in ["don't know", "confused", "not sure"]):
            return QuestionType.CLARIFICATION
        
        # If student is confident but wrong, challenge assumptions
        if any(word in response_lower for word in ["obviously", "clearly", "definitely"]):
            return QuestionType.ASSUMPTION_CHALLENGE
        
        # If student shows understanding, move to conceptual
        if any(word in response_lower for word in ["because", "since", "therefore"]):
            return QuestionType.CONCEPTUAL
        
        # Default to previous question type
        return previous_question.question_type 