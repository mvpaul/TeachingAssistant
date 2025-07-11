"""
Problem Injection Module

This module is responsible for parsing structured problem prompts and converting them
into ProblemInstance objects that the tutoring agent can reason over.
"""

import re
import uuid
from typing import Dict, List, Any, Optional
from .models import ProblemInstance, Subject, Difficulty


class ProblemInjection:
    """
    Handles the parsing and structuring of problem prompts.
    
    This module takes raw problem descriptions and extracts:
    - Subject and topic classification
    - Difficulty assessment
    - Known misconceptions to watch for
    - Expected concepts and learning objectives
    - Visual hints and scaffolding opportunities
    """
    
    def __init__(self):
        self.subject_keywords = {
            Subject.STATICS: [
                "force", "moment", "equilibrium", "free body diagram", "reaction",
                "beam", "truss", "distributed load", "point load", "support"
            ],
            Subject.CIRCUIT_ANALYSIS: [
                "voltage", "current", "resistance", "circuit", "node", "mesh",
                "kirchhoff", "ohm's law", "power", "capacitor", "inductor"
            ]
        }
        
        self.difficulty_indicators = {
            Difficulty.BEGINNER: [
                "simple", "basic", "fundamental", "single", "one", "first"
            ],
            Difficulty.INTERMEDIATE: [
                "multiple", "combined", "system", "analysis", "determine"
            ],
            Difficulty.ADVANCED: [
                "complex", "advanced", "challenging", "optimization", "design"
            ]
        }
    
    def parse_problem(self, problem_description: str, metadata: Optional[Dict[str, Any]] = None) -> ProblemInstance:
        """
        Parse a problem description and create a structured ProblemInstance.
        
        Args:
            problem_description: Raw problem text
            metadata: Optional additional metadata
            
        Returns:
            ProblemInstance with structured data
        """
        if metadata is None:
            metadata = {}
        
        # Extract subject
        subject = self._classify_subject(problem_description)
        
        # Extract topic
        topic = self._extract_topic(problem_description, subject)
        
        # Assess difficulty
        difficulty = self._assess_difficulty(problem_description)
        
        # Extract known misconceptions
        known_misconceptions = self._extract_known_misconceptions(problem_description, subject, topic)
        
        # Extract expected concepts
        expected_concepts = self._extract_expected_concepts(problem_description, subject, topic)
        
        # Extract visual hints
        visual_hints = self._extract_visual_hints(problem_description, subject, topic)
        
        return ProblemInstance(
            id=str(uuid.uuid4()),
            subject=subject,
            topic=topic,
            difficulty=difficulty,
            description=problem_description,
            metadata=metadata,
            known_misconceptions=known_misconceptions,
            expected_concepts=expected_concepts,
            visual_hints=visual_hints
        )
    
    def _classify_subject(self, description: str) -> Subject:
        """Classify the subject based on keywords in the description."""
        description_lower = description.lower()
        
        subject_scores = {}
        for subject, keywords in self.subject_keywords.items():
            score = sum(1 for keyword in keywords if keyword in description_lower)
            subject_scores[subject] = score
        
        # Return the subject with the highest score
        return max(subject_scores.items(), key=lambda x: x[1])[0]
    
    def _extract_topic(self, description: str, subject: Subject) -> str:
        """Extract the specific topic within the subject."""
        description_lower = description.lower()
        
        if subject == Subject.STATICS:
            if "distributed load" in description_lower or "uniform load" in description_lower:
                return "distributed_loads"
            elif "truss" in description_lower:
                return "truss_analysis"
            elif "beam" in description_lower:
                return "beam_analysis"
            elif "equilibrium" in description_lower:
                return "equilibrium"
            else:
                return "general_statics"
        
        elif subject == Subject.CIRCUIT_ANALYSIS:
            if "kirchhoff" in description_lower:
                return "kirchhoff_laws"
            elif "node" in description_lower and "analysis" in description_lower:
                return "nodal_analysis"
            elif "mesh" in description_lower and "analysis" in description_lower:
                return "mesh_analysis"
            elif "thevenin" in description_lower:
                return "thevenin_equivalent"
            else:
                return "general_circuits"
        
        return "general"
    
    def _assess_difficulty(self, description: str) -> Difficulty:
        """Assess the difficulty level based on problem characteristics."""
        description_lower = description.lower()
        
        difficulty_scores = {}
        for difficulty, indicators in self.difficulty_indicators.items():
            score = sum(1 for indicator in indicators if indicator in description_lower)
            difficulty_scores[difficulty] = score
        
        # Additional heuristics
        if len(description.split()) > 100:  # Long description often means complex
            difficulty_scores[Difficulty.ADVANCED] += 1
        
        if any(word in description_lower for word in ["find", "determine", "calculate"]):
            difficulty_scores[Difficulty.INTERMEDIATE] += 1
        
        return max(difficulty_scores.items(), key=lambda x: x[1])[0]
    
    def _extract_known_misconceptions(self, description: str, subject: Subject, topic: str) -> List[str]:
        """Extract known misconceptions to watch for based on subject and topic."""
        misconceptions = []
        
        if subject == Subject.STATICS:
            if topic == "distributed_loads":
                misconceptions.extend([
                    "confusing distributed load with point load",
                    "incorrect force direction in free body diagram",
                    "missing reaction forces",
                    "wrong sign conventions"
                ])
            elif topic == "truss_analysis":
                misconceptions.extend([
                    "assuming all members are in tension",
                    "incorrect joint equilibrium",
                    "missing zero-force members"
                ])
        
        elif subject == Subject.CIRCUIT_ANALYSIS:
            if topic == "kirchhoff_laws":
                misconceptions.extend([
                    "wrong current direction convention",
                    "incorrect voltage polarity",
                    "missing current conservation at nodes"
                ])
        
        return misconceptions
    
    def _extract_expected_concepts(self, description: str, subject: Subject, topic: str) -> List[str]:
        """Extract expected concepts that should be demonstrated."""
        concepts = []
        
        if subject == Subject.STATICS:
            concepts.extend([
                "force equilibrium",
                "moment equilibrium",
                "free body diagrams"
            ])
            
            if topic == "distributed_loads":
                concepts.extend([
                    "distributed load integration",
                    "equivalent point load",
                    "centroid calculation"
                ])
        
        elif subject == Subject.CIRCUIT_ANALYSIS:
            concepts.extend([
                "voltage and current relationships",
                "power calculations"
            ])
            
            if topic == "kirchhoff_laws":
                concepts.extend([
                    "current conservation",
                    "voltage conservation",
                    "loop analysis"
                ])
        
        return concepts
    
    def _extract_visual_hints(self, description: str, subject: Subject, topic: str) -> List[str]:
        """Extract visual hints that could help the student."""
        hints = []
        
        if subject == Subject.STATICS:
            hints.append("Draw a free body diagram")
            
            if topic == "distributed_loads":
                hints.extend([
                    "Show the distributed load as a trapezoid or rectangle",
                    "Mark the centroid of the distributed load",
                    "Include all reaction forces"
                ])
        
        elif subject == Subject.CIRCUIT_ANALYSIS:
            hints.append("Draw the circuit schematic")
            
            if topic == "kirchhoff_laws":
                hints.extend([
                    "Mark current directions with arrows",
                    "Label voltage polarities",
                    "Identify independent loops"
                ])
        
        return hints
    
    def create_beam_problem_example(self) -> ProblemInstance:
        """Create an example beam problem for testing."""
        description = """
        A simply supported beam of length 6m carries a uniformly distributed load 
        of 2 kN/m over its entire length. The beam has a rectangular cross-section 
        with width 200mm and depth 300mm. Determine the maximum bending moment 
        and the maximum shear force in the beam.
        """
        
        return self.parse_problem(description, {
            "problem_type": "beam_analysis",
            "load_type": "uniform_distributed",
            "support_type": "simple_supports"
        }) 