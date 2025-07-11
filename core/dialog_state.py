"""
Dialog State Tracker Module

This module maintains conversational memory of what has been asked, what stage the user
is at, and what hasn't been understood yet. It tracks the overall progress of the
tutoring session.
"""

import uuid
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from .models import DialogState, ProblemInstance, Misconception, SocraticQuestion, VisualSuggestion


class DialogStateTracker:
    """
    Tracks the state of the tutoring conversation and student progress.
    
    This module:
    - Maintains conversation history
    - Tracks detected misconceptions
    - Monitors resolved vs pending concepts
    - Manages session state and timing
    - Provides insights for adaptive tutoring
    """
    
    def __init__(self, problem_instance: ProblemInstance):
        self.dialog_state = DialogState(
            session_id=str(uuid.uuid4()),
            problem_instance=problem_instance,
            pending_concepts=problem_instance.expected_concepts.copy()
        )
        self.concept_progress = {}  # Track progress on each concept
        self.misconception_history = []  # Track misconception evolution
        self.question_effectiveness = {}  # Track which questions work best
    
    def add_student_response(self, student_input: str, 
                           detected_misconceptions: List[Misconception],
                           agent_response: Dict[str, Any]) -> None:
        """
        Add a new student response and update the dialog state.
        
        Args:
            student_input: The student's response text
            detected_misconceptions: Any misconceptions detected
            agent_response: The agent's response to the student
        """
        # Add to conversation history
        self.dialog_state.add_interaction(student_input, agent_response)
        
        # Update misconceptions
        self._update_misconceptions(detected_misconceptions)
        
        # Update concept progress
        self._update_concept_progress(student_input, detected_misconceptions)
        
        # Track question effectiveness
        if "question" in agent_response:
            self._track_question_effectiveness(agent_response["question"], student_input)
    
    def get_current_stage(self) -> str:
        """Determine the current stage of the problem-solving process."""
        
        conversation_length = len(self.dialog_state.conversation_history)
        
        if conversation_length == 0:
            return "initial"
        elif conversation_length < 3:
            return "exploration"
        elif conversation_length < 8:
            return "analysis"
        elif conversation_length < 15:
            return "synthesis"
        else:
            return "refinement"
    
    def get_unresolved_concepts(self) -> List[str]:
        """Get concepts that still need to be addressed."""
        return self.dialog_state.pending_concepts.copy()
    
    def get_resolved_concepts(self) -> List[str]:
        """Get concepts that have been successfully addressed."""
        return self.dialog_state.resolved_concepts.copy()
    
    def get_critical_misconceptions(self) -> List[Misconception]:
        """Get critical misconceptions that need immediate attention."""
        return [m for m in self.dialog_state.detected_misconceptions 
                if m.severity.value == "critical"]
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation progress."""
        return {
            "session_id": self.dialog_state.session_id,
            "current_stage": self.get_current_stage(),
            "conversation_length": len(self.dialog_state.conversation_history),
            "resolved_concepts": len(self.dialog_state.resolved_concepts),
            "pending_concepts": len(self.dialog_state.pending_concepts),
            "critical_misconceptions": len(self.get_critical_misconceptions()),
            "session_duration": datetime.now() - self.dialog_state.session_start_time,
            "last_activity": self.dialog_state.last_activity
        }
    
    def should_suggest_visual(self) -> bool:
        """Determine if a visual suggestion should be made."""
        
        # Suggest visual if there are critical misconceptions
        if self.get_critical_misconceptions():
            return True
        
        # Suggest visual if student seems stuck
        recent_responses = self.dialog_state.conversation_history[-3:]
        stuck_indicators = ["don't know", "confused", "not sure", "can't see"]
        
        for response in recent_responses:
            if "student_input" in response:
                student_text = response["student_input"].lower()
                if any(indicator in student_text for indicator in stuck_indicators):
                    return True
        
        # Suggest visual if in early stages
        if self.get_current_stage() in ["initial", "exploration"]:
            return True
        
        return False
    
    def should_change_strategy(self) -> bool:
        """Determine if the tutoring strategy should be changed."""
        
        # Change strategy if no progress in last 5 responses
        if len(self.dialog_state.conversation_history) >= 5:
            recent_progress = self._assess_recent_progress()
            if recent_progress < 0.2:  # Less than 20% progress
                return True
        
        # Change strategy if student is frustrated
        recent_responses = self.dialog_state.conversation_history[-3:]
        frustration_indicators = ["frustrated", "angry", "give up", "this is too hard"]
        
        for response in recent_responses:
            if "student_input" in response:
                student_text = response["student_input"].lower()
                if any(indicator in student_text for indicator in frustration_indicators):
                    return True
        
        return False
    
    def get_adaptive_suggestions(self) -> List[str]:
        """Get suggestions for adapting the tutoring approach."""
        
        suggestions = []
        
        # Check for lack of progress
        if len(self.dialog_state.conversation_history) > 5:
            progress = self._assess_recent_progress()
            if progress < 0.3:
                suggestions.append("Consider breaking down the problem into smaller steps")
                suggestions.append("Use more visual scaffolding")
                suggestions.append("Focus on fundamental concepts first")
        
        # Check for misconceptions
        critical_misconceptions = self.get_critical_misconceptions()
        if critical_misconceptions:
            suggestions.append("Address critical misconceptions before proceeding")
            suggestions.append("Use concrete examples to illustrate concepts")
        
        # Check for student confidence
        if self._assess_student_confidence() < 0.5:
            suggestions.append("Provide more positive reinforcement")
            suggestions.append("Use simpler language and shorter questions")
        
        return suggestions
    
    def _update_misconceptions(self, new_misconceptions: List[Misconception]) -> None:
        """Update the list of detected misconceptions."""
        
        # Add new misconceptions
        for misconception in new_misconceptions:
            if misconception not in self.dialog_state.detected_misconceptions:
                self.dialog_state.detected_misconceptions.append(misconception)
                self.misconception_history.append({
                    "timestamp": datetime.now(),
                    "misconception": misconception,
                    "action": "detected"
                })
        
        # Check if any misconceptions have been resolved
        resolved_misconceptions = []
        for misconception in self.dialog_state.detected_misconceptions:
            if self._is_misconception_resolved(misconception):
                resolved_misconceptions.append(misconception)
                self.misconception_history.append({
                    "timestamp": datetime.now(),
                    "misconception": misconception,
                    "action": "resolved"
                })
        
        # Remove resolved misconceptions
        for misconception in resolved_misconceptions:
            self.dialog_state.detected_misconceptions.remove(misconception)
    
    def _update_concept_progress(self, student_input: str, 
                               misconceptions: List[Misconception]) -> None:
        """Update progress on expected concepts."""
        
        # Check if any concepts have been demonstrated
        for concept in self.dialog_state.pending_concepts:
            if self._concept_demonstrated(concept, student_input, misconceptions):
                self.dialog_state.pending_concepts.remove(concept)
                self.dialog_state.resolved_concepts.append(concept)
                self.concept_progress[concept] = {
                    "resolved_at": datetime.now(),
                    "demonstrated_in": student_input
                }
    
    def _track_question_effectiveness(self, question: SocraticQuestion, 
                                    student_response: str) -> None:
        """Track how effective different types of questions are."""
        
        question_id = question.id
        if question_id not in self.question_effectiveness:
            self.question_effectiveness[question_id] = {
                "question_type": question.question_type,
                "target_concept": question.target_concept,
                "responses": [],
                "effectiveness_score": 0.0
            }
        
        # Analyze response quality
        effectiveness = self._assess_response_quality(student_response, question)
        self.question_effectiveness[question_id]["responses"].append({
            "response": student_response,
            "effectiveness": effectiveness,
            "timestamp": datetime.now()
        })
        
        # Update overall effectiveness score
        responses = self.question_effectiveness[question_id]["responses"]
        self.question_effectiveness[question_id]["effectiveness_score"] = sum(
            r["effectiveness"] for r in responses
        ) / len(responses)
    
    def _is_misconception_resolved(self, misconception: Misconception) -> bool:
        """Check if a misconception has been resolved."""
        
        # Check recent responses for evidence of resolution
        recent_responses = self.dialog_state.conversation_history[-3:]
        
        for response in recent_responses:
            if "student_input" in response:
                student_text = response["student_input"].lower()
                
                # Look for positive indicators
                positive_indicators = [
                    "i understand now",
                    "that makes sense",
                    "i see the mistake",
                    "corrected",
                    "fixed"
                ]
                
                if any(indicator in student_text for indicator in positive_indicators):
                    return True
        
        return False
    
    def _concept_demonstrated(self, concept: str, student_input: str, 
                            misconceptions: List[Misconception]) -> bool:
        """Check if a concept has been demonstrated in the student's response."""
        
        # Check for concept-specific keywords
        concept_keywords = self._get_concept_keywords(concept)
        student_text_lower = student_input.lower()
        
        # Must have relevant keywords and no critical misconceptions
        has_keywords = any(keyword in student_text_lower for keyword in concept_keywords)
        no_critical_misconceptions = not any(
            m.severity.value == "critical" for m in misconceptions
        )
        
        return has_keywords and no_critical_misconceptions
    
    def _get_concept_keywords(self, concept: str) -> List[str]:
        """Get keywords that indicate understanding of a concept."""
        
        concept_keywords = {
            "force_equilibrium": ["force", "equilibrium", "balance", "sum of forces"],
            "moment_equilibrium": ["moment", "torque", "rotation", "moment equilibrium"],
            "free_body_diagrams": ["free body", "fbd", "diagram", "forces acting"],
            "distributed_load_integration": ["integrate", "area", "distributed", "equivalent"],
            "equivalent_point_load": ["equivalent", "point load", "centroid", "middle"],
            "centroid_calculation": ["centroid", "center", "middle", "average"],
            "current_conservation": ["current", "conservation", "node", "kirchhoff"],
            "voltage_conservation": ["voltage", "loop", "kirchhoff", "conservation"]
        }
        
        return concept_keywords.get(concept, [concept])
    
    def _assess_response_quality(self, student_response: str, 
                               question: SocraticQuestion) -> float:
        """Assess the quality of a student's response to a question."""
        
        response_lower = student_response.lower()
        quality_score = 0.0
        
        # Length indicator (longer responses often show more thought)
        if len(student_response.split()) > 10:
            quality_score += 0.2
        
        # Evidence of reasoning
        reasoning_indicators = ["because", "since", "therefore", "thus", "so"]
        if any(indicator in response_lower for indicator in reasoning_indicators):
            quality_score += 0.3
        
        # Specificity
        if any(word in response_lower for word in question.target_concept.split("_")):
            quality_score += 0.2
        
        # Confidence (but not overconfidence)
        if "i think" in response_lower or "maybe" in response_lower:
            quality_score += 0.1
        elif "definitely" in response_lower or "obviously" in response_lower:
            quality_score -= 0.1
        
        # Avoidance of misconceptions
        misconception_indicators = ["wrong", "incorrect", "mistake", "error"]
        if not any(indicator in response_lower for indicator in misconception_indicators):
            quality_score += 0.2
        
        return min(1.0, max(0.0, quality_score))
    
    def _assess_recent_progress(self) -> float:
        """Assess progress in recent responses."""
        
        if len(self.dialog_state.conversation_history) < 3:
            return 0.0
        
        recent_responses = self.dialog_state.conversation_history[-3:]
        progress_score = 0.0
        
        for response in recent_responses:
            if "student_input" in response:
                student_text = response["student_input"].lower()
                
                # Positive progress indicators
                positive_indicators = ["understand", "see", "correct", "right", "yes"]
                negative_indicators = ["don't know", "confused", "wrong", "no", "unsure"]
                
                positive_count = sum(1 for indicator in positive_indicators 
                                   if indicator in student_text)
                negative_count = sum(1 for indicator in negative_indicators 
                                   if indicator in student_text)
                
                if positive_count > negative_count:
                    progress_score += 0.33
                elif positive_count == negative_count:
                    progress_score += 0.17
        
        return progress_score
    
    def _assess_student_confidence(self) -> float:
        """Assess the student's current confidence level."""
        
        if not self.dialog_state.conversation_history:
            return 0.5  # Neutral confidence
        
        recent_responses = self.dialog_state.conversation_history[-3:]
        confidence_score = 0.0
        
        for response in recent_responses:
            if "student_input" in response:
                student_text = response["student_input"].lower()
                
                # High confidence indicators
                high_confidence = ["confident", "sure", "definitely", "obviously", "clearly"]
                low_confidence = ["unsure", "maybe", "think", "guess", "not sure"]
                
                high_count = sum(1 for indicator in high_confidence 
                               if indicator in student_text)
                low_count = sum(1 for indicator in low_confidence 
                              if indicator in student_text)
                
                if high_count > low_count:
                    confidence_score += 0.33
                elif high_count == low_count:
                    confidence_score += 0.17
        
        return min(1.0, max(0.0, confidence_score))
    
    def export_session_data(self) -> Dict[str, Any]:
        """Export session data for analysis and improvement."""
        
        return {
            "session_id": self.dialog_state.session_id,
            "problem_instance": {
                "subject": self.dialog_state.problem_instance.subject.value,
                "topic": self.dialog_state.problem_instance.topic,
                "difficulty": self.dialog_state.problem_instance.difficulty.value
            },
            "conversation_history": self.dialog_state.conversation_history,
            "misconception_history": self.misconception_history,
            "concept_progress": self.concept_progress,
            "question_effectiveness": self.question_effectiveness,
            "session_metrics": self.get_conversation_summary()
        } 