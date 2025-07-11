"""
Smart Whiteboard Integration Module
Connects the Streamlit whiteboard interface to the tutoring agent architecture.
"""

import sys
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from PIL import Image
import numpy as np

# Add the core modules to the path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

try:
    from core.misconception_detector import MisconceptionDetector
    from core.socratic_engine import SocraticEngine
    from core.visual_scaffolding import VisualScaffoldingGenerator
    from core.dialog_state_tracker import DialogStateTracker
    from core.problem_injection import ProblemInjector
    from subjects.statics import StaticsModule
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some tutoring agent modules not available: {e}")
    INTEGRATION_AVAILABLE = False
    # Create dummy classes for fallback
    class MisconceptionDetector:
        def __init__(self): pass
    class SocraticEngine:
        def __init__(self): pass
    class VisualScaffoldingGenerator:
        def __init__(self): pass
    class DialogStateTracker:
        def __init__(self): pass
        def update_state(self, *args): pass
    class ProblemInjector:
        def __init__(self): pass
    class StaticsModule:
        def __init__(self): pass

@dataclass
class DrawingAnalysis:
    """Analysis results from a student's drawing."""
    content_type: str  # "equation", "diagram", "sketch", "mixed"
    detected_elements: List[str]
    confidence: float
    misconceptions: List[str]
    suggestions: List[str]
    next_question: str
    visual_scaffolding: Optional[str] = None

class WhiteboardTutoringAgent:
    """
    Integrates the Smart Whiteboard with the tutoring agent architecture.
    Handles drawing analysis, misconception detection, and Socratic questioning.
    """
    
    def __init__(self):
        """Initialize the tutoring agent with all core modules."""
        self.misconception_detector = MisconceptionDetector()
        self.socratic_engine = SocraticEngine()
        self.visual_generator = VisualScaffoldingGenerator()
        self.dialog_tracker = DialogStateTracker()
        self.problem_injector = ProblemInjector()
        
        # Subject-specific modules
        self.statics_module = StaticsModule()
        
        # Current session state
        self.current_subject = "Statics"
        self.current_topic = "Free Body Diagrams"
        self.session_history = []
        
        # Check if full integration is available
        self.full_integration = INTEGRATION_AVAILABLE
    
    def analyze_drawing(self, canvas_data, subject: str = "Statics", topic: str = "Free Body Diagrams") -> DrawingAnalysis:
        """
        Analyze a student's drawing using AI and tutoring modules.
        
        Args:
            canvas_data: Canvas data from streamlit-drawable-canvas
            subject: Current subject being studied
            topic: Current topic being studied
            
        Returns:
            DrawingAnalysis: Comprehensive analysis of the drawing
        """
        # TODO: Integrate with actual handwriting recognition
        # For now, use placeholder analysis based on drawing characteristics
        
        # Extract drawing characteristics
        drawing_info = self._extract_drawing_characteristics(canvas_data)
        
        # Determine content type
        content_type = self._classify_content_type(drawing_info)
        
        # Detect potential misconceptions
        misconceptions = self._detect_misconceptions(drawing_info, subject, topic)
        
        # Generate Socratic questions
        next_question = self._generate_socratic_question(drawing_info, misconceptions, subject, topic)
        
        # Generate visual scaffolding suggestions
        visual_scaffolding = self._generate_visual_suggestions(drawing_info, misconceptions, subject, topic)
        
        # Calculate confidence based on drawing complexity
        confidence = self._calculate_confidence(drawing_info)
        
        return DrawingAnalysis(
            content_type=content_type,
            detected_elements=drawing_info.get("elements", []),
            confidence=confidence,
            misconceptions=misconceptions,
            suggestions=self._generate_suggestions(misconceptions, subject, topic),
            next_question=next_question,
            visual_scaffolding=visual_scaffolding
        )
    
    def _extract_drawing_characteristics(self, canvas_data) -> Dict[str, Any]:
        """Extract characteristics from the canvas drawing."""
        if canvas_data is None or canvas_data.json_data is None:
            return {"elements": [], "complexity": 0, "shapes": []}
        
        objects = canvas_data.json_data.get("objects", [])
        characteristics = {
            "elements": [],
            "complexity": len(objects),
            "shapes": [],
            "text_elements": [],
            "lines": [],
            "circles": [],
            "rectangles": []
        }
        
        for obj in objects:
            obj_type = obj.get("type", "unknown")
            characteristics["shapes"].append(obj_type)
            
            if obj_type == "line":
                characteristics["lines"].append(obj)
            elif obj_type == "circle":
                characteristics["circles"].append(obj)
            elif obj_type == "rect":
                characteristics["rectangles"].append(obj)
            elif obj_type == "freedraw":
                # Analyze freehand drawing patterns
                path_data = obj.get("path", [])
                if len(path_data) > 10:  # Complex freehand drawing
                    characteristics["elements"].append("complex_sketch")
                else:
                    characteristics["elements"].append("simple_sketch")
        
        return characteristics
    
    def _classify_content_type(self, drawing_info: Dict[str, Any]) -> str:
        """Classify the type of content drawn."""
        elements = drawing_info.get("elements", [])
        shapes = drawing_info.get("shapes", [])
        
        if "complex_sketch" in elements:
            return "diagram"
        elif len(shapes) > 5:
            return "mixed"
        elif "line" in shapes and len(shapes) > 2:
            return "diagram"
        else:
            return "sketch"
    
    def _detect_misconceptions(self, drawing_info: Dict[str, Any], subject: str, topic: str) -> List[str]:
        """Detect potential misconceptions in the drawing."""
        misconceptions = []
        
        if subject == "Statics" and topic == "Free Body Diagrams":
            # Check for common statics misconceptions
            lines = drawing_info.get("lines", [])
            circles = drawing_info.get("circles", [])
            
            if len(lines) < 2:
                misconceptions.append("missing_force_vectors")
            
            if len(circles) == 0:
                misconceptions.append("missing_object_boundary")
            
            if len(lines) > 10:
                misconceptions.append("overcomplicated_diagram")
        
        return misconceptions
    
    def _generate_socratic_question(self, drawing_info: Dict[str, Any], misconceptions: List[str], subject: str, topic: str) -> str:
        """Generate a Socratic question based on the drawing and misconceptions."""
        if not misconceptions:
            return "What forces are acting on the object in your diagram?"
        
        if "missing_force_vectors" in misconceptions:
            return "I notice you haven't drawn many force vectors. What forces do you think are acting on this object?"
        
        if "missing_object_boundary" in misconceptions:
            return "Can you clearly define the boundary of the object you're analyzing?"
        
        if "overcomplicated_diagram" in misconceptions:
            return "Your diagram has many elements. Can you simplify it to show only the essential forces?"
        
        return "What is the next step in analyzing this free body diagram?"
    
    def _generate_visual_suggestions(self, drawing_info: Dict[str, Any], misconceptions: List[str], subject: str, topic: str) -> Optional[str]:
        """Generate visual scaffolding suggestions."""
        if "missing_force_vectors" in misconceptions:
            return "Try drawing arrows to represent each force acting on the object"
        
        if "missing_object_boundary" in misconceptions:
            return "Draw a dashed line around the object to clearly define its boundary"
        
        return None
    
    def _calculate_confidence(self, drawing_info: Dict[str, Any]) -> float:
        """Calculate confidence in the analysis based on drawing characteristics."""
        complexity = drawing_info.get("complexity", 0)
        
        if complexity == 0:
            return 0.0
        elif complexity < 3:
            return 0.3
        elif complexity < 8:
            return 0.7
        else:
            return 0.9
    
    def _generate_suggestions(self, misconceptions: List[str], subject: str, topic: str) -> List[str]:
        """Generate helpful suggestions based on misconceptions."""
        suggestions = []
        
        if "missing_force_vectors" in misconceptions:
            suggestions.append("Draw arrows for each force (weight, normal force, friction, etc.)")
        
        if "missing_object_boundary" in misconceptions:
            suggestions.append("Clearly define the object's boundary with a dashed line")
        
        if "overcomplicated_diagram" in misconceptions:
            suggestions.append("Focus on the essential forces - you can add details later")
        
        return suggestions
    
    def process_student_response(self, response: str, analysis: DrawingAnalysis) -> str:
        """
        Process a student's text response to generate follow-up questions.
        
        Args:
            response: Student's text response
            analysis: Previous drawing analysis
            
        Returns:
            str: AI tutor's follow-up response
        """
        # Update dialog state
        self.dialog_tracker.update_state(response, analysis)
        
        # Generate contextual response
        if "force" in response.lower() or "weight" in response.lower():
            return "Good! Now let's think about the direction of these forces. Which way does each force point?"
        
        if "direction" in response.lower():
            return "Excellent! Now can you calculate the magnitude of the net force?"
        
        if "magnitude" in response.lower() or "calculate" in response.lower():
            return "Great progress! What equations will you use to solve for the unknown forces?"
        
        return "That's interesting! Can you explain your reasoning a bit more?"
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current tutoring session."""
        return {
            "subject": self.current_subject,
            "topic": self.current_topic,
            "session_length": len(self.session_history),
            "misconceptions_addressed": len([h for h in self.session_history if h.get("misconceptions")]),
            "questions_asked": len([h for h in self.session_history if h.get("type") == "ai_question"])
        }

# Global instance for easy access
tutoring_agent = WhiteboardTutoringAgent() 