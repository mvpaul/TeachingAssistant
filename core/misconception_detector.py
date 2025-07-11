"""
Misconception Detector Module

This module analyzes student responses to detect conceptual errors and misconceptions.
It uses pattern matching, mathematical analysis, and subject-specific logic to identify
"red zone" errors that need immediate attention.
"""

import re
import uuid
from typing import List, Dict, Any, Optional, Tuple
from .models import Misconception, ErrorSeverity, Subject, StudentResponse


class MisconceptionDetector:
    """
    Detects conceptual errors and misconceptions in student responses.
    
    This module analyzes:
    - Text responses for conceptual misunderstandings
    - Mathematical expressions for calculation errors
    - Sketches for visual misconceptions
    - Patterns that indicate common student mistakes
    """
    
    def __init__(self):
        self.error_patterns = self._initialize_error_patterns()
        self.mathematical_errors = self._initialize_mathematical_errors()
        self.visual_misconceptions = self._initialize_visual_misconceptions()
    
    def detect_misconceptions(self, student_response: StudentResponse, 
                            problem_subject: Subject, 
                            problem_topic: str) -> List[Misconception]:
        """
        Analyze a student response and detect any misconceptions.
        
        Args:
            student_response: The student's response to analyze
            problem_subject: The subject of the problem
            problem_topic: The specific topic within the subject
            
        Returns:
            List of detected misconceptions
        """
        misconceptions = []
        
        # Analyze text response
        text_misconceptions = self._analyze_text_response(
            student_response.text, problem_subject, problem_topic
        )
        misconceptions.extend(text_misconceptions)
        
        # Analyze mathematical expressions
        math_misconceptions = self._analyze_mathematical_expressions(
            student_response.mathematical_expressions, problem_subject, problem_topic
        )
        misconceptions.extend(math_misconceptions)
        
        # Analyze sketches if provided
        if student_response.sketches:
            sketch_misconceptions = self._analyze_sketches(
                student_response.sketches, problem_subject, problem_topic
            )
            misconceptions.extend(sketch_misconceptions)
        
        # Check for confidence-related issues
        confidence_misconceptions = self._analyze_confidence_indicators(
            student_response.confidence_indicator, misconceptions
        )
        misconceptions.extend(confidence_misconceptions)
        
        return misconceptions
    
    def _initialize_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize patterns for detecting text-based misconceptions."""
        return {
            Subject.STATICS: {
                "distributed_loads": {
                    "force_direction_errors": {
                        "patterns": [
                            r"force.*downward",
                            r"reaction.*upward",
                            r"load.*negative"
                        ],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Incorrect force direction assumption"
                    },
                    "missing_reactions": {
                        "patterns": [
                            r"only.*one.*reaction",
                            r"no.*moment.*reaction",
                            r"forgot.*support"
                        ],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Missing reaction forces in analysis"
                    },
                    "sign_convention_errors": {
                        "patterns": [
                            r"negative.*moment",
                            r"positive.*shear",
                            r"wrong.*sign"
                        ],
                        "severity": ErrorSeverity.MODERATE,
                        "description": "Incorrect sign convention usage"
                    }
                },
                "general_statics": {
                    "equilibrium_errors": {
                        "patterns": [
                            r"forces.*don't.*balance",
                            r"unbalanced.*system",
                            r"missing.*equilibrium"
                        ],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Failure to apply equilibrium conditions"
                    }
                }
            },
            Subject.CIRCUIT_ANALYSIS: {
                "kirchhoff_laws": {
                    "current_direction_errors": {
                        "patterns": [
                            r"current.*wrong.*direction",
                            r"flow.*backward",
                            r"negative.*current"
                        ],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Incorrect current direction convention"
                    },
                    "voltage_polarity_errors": {
                        "patterns": [
                            r"voltage.*polarity.*wrong",
                            r"positive.*negative.*confused",
                            r"sign.*voltage.*error"
                        ],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Incorrect voltage polarity assignment"
                    }
                }
            }
        }
    
    def _initialize_mathematical_errors(self) -> Dict[str, Dict[str, Any]]:
        """Initialize patterns for detecting mathematical errors."""
        return {
            Subject.STATICS: {
                "distributed_loads": {
                    "integration_errors": {
                        "patterns": [
                            r"∫.*w.*dx.*=.*w",  # Missing integration
                            r"force.*=.*w.*L",  # Wrong integration result
                        ],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Incorrect integration of distributed load"
                    },
                    "centroid_errors": {
                        "patterns": [
                            r"centroid.*=.*L",  # Wrong centroid location
                            r"moment.*=.*F.*L",  # Wrong moment arm
                        ],
                        "severity": ErrorSeverity.MODERATE,
                        "description": "Incorrect centroid calculation"
                    }
                }
            },
            Subject.CIRCUIT_ANALYSIS: {
                "kirchhoff_laws": {
                    "current_conservation_errors": {
                        "patterns": [
                            r"I1.*=.*I2.*=.*I3",  # Assuming all currents equal
                            r"current.*sum.*=.*0",  # Wrong current conservation
                        ],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Incorrect current conservation at nodes"
                    }
                }
            }
        }
    
    def _initialize_visual_misconceptions(self) -> Dict[str, Dict[str, Any]]:
        """Initialize patterns for detecting visual misconceptions."""
        return {
            Subject.STATICS: {
                "distributed_loads": {
                    "fbd_errors": {
                        "missing_elements": ["reaction forces", "distributed load representation"],
                        "wrong_directions": ["force arrows", "moment arrows"],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Incorrect free body diagram"
                    }
                }
            },
            Subject.CIRCUIT_ANALYSIS: {
                "kirchhoff_laws": {
                    "circuit_errors": {
                        "missing_elements": ["current arrows", "voltage polarities"],
                        "wrong_connections": ["node connections", "component placement"],
                        "severity": ErrorSeverity.CRITICAL,
                        "description": "Incorrect circuit schematic"
                    }
                }
            }
        }
    
    def _analyze_text_response(self, text: str, subject: Subject, topic: str) -> List[Misconception]:
        """Analyze text response for misconceptions."""
        misconceptions = []
        text_lower = text.lower()
        
        if subject in self.error_patterns and topic in self.error_patterns[subject]:
            topic_patterns = self.error_patterns[subject][topic]
            
            for error_type, error_info in topic_patterns.items():
                for pattern in error_info["patterns"]:
                    if re.search(pattern, text_lower):
                        misconception = Misconception(
                            id=str(uuid.uuid4()),
                            description=error_info["description"],
                            severity=error_info["severity"],
                            detected_patterns=[pattern],
                            related_concepts=[topic],
                            confidence=0.8  # High confidence for pattern matches
                        )
                        misconceptions.append(misconception)
        
        return misconceptions
    
    def _analyze_mathematical_expressions(self, expressions: List[str], 
                                       subject: Subject, topic: str) -> List[Misconception]:
        """Analyze mathematical expressions for errors."""
        misconceptions = []
        
        if subject in self.mathematical_errors and topic in self.mathematical_errors[subject]:
            topic_errors = self.mathematical_errors[subject][topic]
            
            for expression in expressions:
                for error_type, error_info in topic_errors.items():
                    for pattern in error_info["patterns"]:
                        if re.search(pattern, expression):
                            misconception = Misconception(
                                id=str(uuid.uuid4()),
                                description=error_info["description"],
                                severity=error_info["severity"],
                                detected_patterns=[pattern],
                                related_concepts=[topic],
                                confidence=0.9  # Very high confidence for math errors
                            )
                            misconceptions.append(misconception)
        
        return misconceptions
    
    def _analyze_sketches(self, sketches: List[str], subject: Subject, topic: str) -> List[Misconception]:
        """Analyze sketches for visual misconceptions."""
        misconceptions = []
        
        # For now, this is a placeholder. In a real implementation, this would:
        # 1. Parse sketch data (SVG, image analysis, etc.)
        # 2. Extract visual elements
        # 3. Compare against expected visual patterns
        
        if subject in self.visual_misconceptions and topic in self.visual_misconceptions[subject]:
            topic_errors = self.visual_misconceptions[subject][topic]
            
            for error_type, error_info in topic_errors.items():
                # Placeholder logic - in reality, this would analyze actual sketch content
                if "missing_elements" in error_info:
                    misconception = Misconception(
                        id=str(uuid.uuid4()),
                        description=error_info["description"],
                        severity=error_info["severity"],
                        detected_patterns=["visual_analysis"],
                        related_concepts=[topic],
                        confidence=0.7  # Moderate confidence for visual analysis
                    )
                    misconceptions.append(misconception)
        
        return misconceptions
    
    def _analyze_confidence_indicators(self, confidence: Optional[str], 
                                    existing_misconceptions: List[Misconception]) -> List[Misconception]:
        """Analyze confidence indicators for potential issues."""
        misconceptions = []
        
        if confidence == "unsure" and not existing_misconceptions:
            # Student is unsure but no obvious errors detected - might need scaffolding
            misconception = Misconception(
                id=str(uuid.uuid4()),
                description="Student lacks confidence in approach",
                severity=ErrorSeverity.MINOR,
                detected_patterns=["low_confidence"],
                related_concepts=["general_approach"],
                confidence=0.6
            )
            misconceptions.append(misconception)
        
        elif confidence == "confident" and existing_misconceptions:
            # Student is confident but has errors - potential overconfidence
            misconception = Misconception(
                id=str(uuid.uuid4()),
                description="Overconfidence despite conceptual errors",
                severity=ErrorSeverity.MODERATE,
                detected_patterns=["overconfidence"],
                related_concepts=["self_assessment"],
                confidence=0.7
            )
            misconceptions.append(misconception)
        
        return misconceptions
    
    def get_critical_misconceptions(self, misconceptions: List[Misconception]) -> List[Misconception]:
        """Filter for critical (red zone) misconceptions that need immediate attention."""
        return [m for m in misconceptions if m.severity == ErrorSeverity.CRITICAL]
    
    def suggest_remediation_strategies(self, misconception: Misconception) -> List[str]:
        """Suggest remediation strategies for a detected misconception."""
        strategies = []
        
        if misconception.severity == ErrorSeverity.CRITICAL:
            strategies.append("Immediate conceptual clarification needed")
            strategies.append("Use visual scaffolding to correct understanding")
            strategies.append("Break down the problem into smaller steps")
        
        elif misconception.severity == ErrorSeverity.MODERATE:
            strategies.append("Provide guided practice with similar problems")
            strategies.append("Use Socratic questioning to challenge assumptions")
        
        else:  # MINOR
            strategies.append("Gentle correction with positive reinforcement")
            strategies.append("Provide additional examples")
        
        return strategies 