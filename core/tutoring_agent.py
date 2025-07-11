"""
Main Tutoring Agent Module

This module orchestrates all the components of the tutoring system:
- Problem Injection
- Misconception Detection
- Socratic Questioning
- Visual Scaffolding
- Dialog State Management

It provides the primary interface for conducting tutoring sessions.
"""

from typing import List, Dict, Any, Optional
from .models import (
    ProblemInstance, StudentResponse, AgentResponse, TutoringSession,
    Misconception, SocraticQuestion, VisualSuggestion
)
from .problem_injection import ProblemInjection
from .misconception_detector import MisconceptionDetector
from .socratic_engine import SocraticEngine
from .visual_scaffolding import VisualScaffolding
from .dialog_state import DialogStateTracker


class TutoringAgent:
    """
    Main tutoring agent that orchestrates all system components.
    
    This agent:
    - Manages tutoring sessions
    - Coordinates between different modules
    - Provides a unified interface for tutoring interactions
    - Adapts strategies based on student progress
    """
    
    def __init__(self):
        self.problem_injection = ProblemInjection()
        self.misconception_detector = MisconceptionDetector()
        self.socratic_engine = SocraticEngine()
        self.visual_scaffolding = VisualScaffolding()
        self.active_sessions: Dict[str, TutoringSession] = {}
    
    def start_session(self, problem_instance: ProblemInstance) -> TutoringSession:
        """
        Start a new tutoring session for a given problem.
        
        Args:
            problem_instance: The problem to work on
            
        Returns:
            TutoringSession object representing the active session
        """
        # Create dialog state tracker
        dialog_tracker = DialogStateTracker(problem_instance)
        
        # Create tutoring session
        session = TutoringSession(
            session_id=dialog_tracker.dialog_state.session_id,
            dialog_state=dialog_tracker.dialog_state
        )
        
        # Store session
        self.active_sessions[session.session_id] = session
        
        return session
    
    def process_student_input(self, session_id: str, student_input: str,
                            mathematical_expressions: Optional[List[str]] = None,
                            sketches: Optional[List[str]] = None,
                            confidence_indicator: Optional[str] = None) -> AgentResponse:
        """
        Process a student's input and generate an appropriate response.
        
        Args:
            session_id: ID of the active session
            student_input: Text input from the student
            mathematical_expressions: Optional mathematical expressions
            sketches: Optional sketch data
            confidence_indicator: Optional confidence level indicator
            
        Returns:
            AgentResponse with appropriate tutoring response
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        dialog_tracker = DialogStateTracker(session.dialog_state.problem_instance)
        dialog_tracker.dialog_state = session.dialog_state
        
        # Create student response object
        student_response = StudentResponse(
            text=student_input,
            mathematical_expressions=mathematical_expressions or [],
            sketches=sketches or [],
            confidence_indicator=confidence_indicator
        )
        
        # Detect misconceptions
        misconceptions = self.misconception_detector.detect_misconceptions(
            student_response,
            session.dialog_state.problem_instance.subject,
            session.dialog_state.problem_instance.topic
        )
        
        # Get current stage
        current_stage = dialog_tracker.get_current_stage()
        
        # Generate Socratic question
        question = self.socratic_engine.generate_question(
            problem_subject=session.dialog_state.problem_instance.subject,
            problem_topic=session.dialog_state.problem_instance.topic,
            detected_misconceptions=misconceptions,
            conversation_history=dialog_tracker.dialog_state.conversation_history,
            current_stage=current_stage
        )
        
        # Check if visual scaffolding is needed
        visual_suggestion = None
        if dialog_tracker.should_suggest_visual():
            visual_suggestion = self.visual_scaffolding.generate_visual_suggestion(
                problem_subject=session.dialog_state.problem_instance.subject,
                problem_topic=session.dialog_state.problem_instance.topic,
                detected_misconceptions=misconceptions,
                current_stage=current_stage
            )
        
        # Create agent response
        agent_response = self._create_agent_response(
            question, visual_suggestion, misconceptions, current_stage
        )
        
        # Update dialog state
        dialog_tracker.add_student_response(
            student_input, misconceptions, agent_response.__dict__
        )
        
        # Update session
        session.dialog_state = dialog_tracker.dialog_state
        
        return agent_response
    
    def _create_agent_response(self, question: SocraticQuestion,
                             visual_suggestion: Optional[VisualSuggestion],
                             misconceptions: List[Misconception],
                             current_stage: str) -> AgentResponse:
        """Create a structured agent response."""
        
        # Determine response type and content
        if misconceptions and any(m.severity.value == "critical" for m in misconceptions):
            response_type = "misconception_correction"
            content = self._format_misconception_response(question, misconceptions)
        elif visual_suggestion:
            response_type = "visual_scaffolding"
            content = visual_suggestion
        else:
            response_type = "socratic_question"
            content = question
        
        # Generate suggested actions
        suggested_actions = self._generate_suggested_actions(
            misconceptions, current_stage, visual_suggestion
        )
        
        return AgentResponse(
            response_type=response_type,
            content=content,
            detected_misconceptions=misconceptions,
            suggested_actions=suggested_actions,
            confidence=1.0,
            metadata={
                "current_stage": current_stage,
                "question_type": question.question_type.value if hasattr(question, 'question_type') else None
            }
        )
    
    def _format_misconception_response(self, question: SocraticQuestion,
                                     misconceptions: List[Misconception]) -> str:
        """Format a response that addresses misconceptions."""
        
        critical_misconceptions = [m for m in misconceptions if m.severity.value == "critical"]
        
        if critical_misconceptions:
            response = "I notice there might be a misunderstanding here. "
            response += question.question_text
            response += "\n\nThis will help us clarify the concept."
        else:
            response = question.question_text
        
        return response
    
    def _generate_suggested_actions(self, misconceptions: List[Misconception],
                                  current_stage: str,
                                  visual_suggestion: Optional[VisualSuggestion]) -> List[str]:
        """Generate suggested actions for the student."""
        
        actions = []
        
        # Add actions based on misconceptions
        for misconception in misconceptions:
            if misconception.severity.value == "critical":
                actions.append("Take time to think about this step carefully")
                actions.append("Consider drawing a diagram to visualize the situation")
        
        # Add actions based on current stage
        if current_stage == "initial":
            actions.append("Start by understanding what the problem is asking")
            actions.append("Identify the key concepts involved")
        elif current_stage == "exploration":
            actions.append("Try to break down the problem into smaller parts")
            actions.append("Think about what you already know that might apply")
        
        # Add visual actions if visual suggestion is provided
        if visual_suggestion:
            actions.append("Use the suggested visual aid to help your understanding")
        
        return actions
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of the tutoring session."""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        dialog_tracker = DialogStateTracker(session.dialog_state.problem_instance)
        dialog_tracker.dialog_state = session.dialog_state
        
        return dialog_tracker.get_conversation_summary()
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End a tutoring session and return final summary."""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        session.end_session()
        
        # Get final summary
        dialog_tracker = DialogStateTracker(session.dialog_state.problem_instance)
        dialog_tracker.dialog_state = session.dialog_state
        
        final_summary = {
            "session_id": session_id,
            "problem": {
                "subject": session.dialog_state.problem_instance.subject.value,
                "topic": session.dialog_state.problem_instance.topic,
                "difficulty": session.dialog_state.problem_instance.difficulty.value
            },
            "session_metrics": dialog_tracker.get_conversation_summary(),
            "concept_progress": {
                "resolved": dialog_tracker.get_resolved_concepts(),
                "pending": dialog_tracker.get_unresolved_concepts()
            },
            "misconceptions_addressed": len(session.dialog_state.detected_misconceptions),
            "session_duration": session.session_metadata.get("end_time") - session.dialog_state.session_start_time
        }
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        return final_summary
    
    def get_adaptive_suggestions(self, session_id: str) -> List[str]:
        """Get suggestions for adapting the tutoring approach."""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        dialog_tracker = DialogStateTracker(session.dialog_state.problem_instance)
        dialog_tracker.dialog_state = session.dialog_state
        
        return dialog_tracker.get_adaptive_suggestions()
    
    def create_beam_problem_example(self) -> ProblemInstance:
        """Create an example beam problem for testing."""
        return self.problem_injection.create_beam_problem_example()
    
    def export_session_data(self, session_id: str) -> Dict[str, Any]:
        """Export complete session data for analysis."""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        dialog_tracker = DialogStateTracker(session.dialog_state.problem_instance)
        dialog_tracker.dialog_state = session.dialog_state
        
        return dialog_tracker.export_session_data()
    
    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active tutoring sessions."""
        
        sessions = []
        for session_id, session in self.active_sessions.items():
            sessions.append({
                "session_id": session_id,
                "problem_topic": session.dialog_state.problem_instance.topic,
                "subject": session.dialog_state.problem_instance.subject.value,
                "start_time": session.dialog_state.session_start_time,
                "conversation_length": len(session.dialog_state.conversation_history)
            })
        
        return sessions 