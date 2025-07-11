"""
Visual Scaffolding Generator Module

This module suggests relevant diagrams, free body diagrams, circuit schematics, and other
visual aids to help students understand concepts. It can integrate with sketch-to-text
tools and whiteboard canvases.
"""

import uuid
from typing import List, Dict, Any, Optional
from .models import VisualSuggestion, Subject, Misconception


class VisualScaffolding:
    """
    Generates visual suggestions to support student learning.
    
    This module:
    - Suggests appropriate diagrams based on problem type
    - Provides visual hints for common misconceptions
    - Supports interactive visual elements
    - Integrates with external visualization tools
    """
    
    def __init__(self):
        self.visual_templates = self._initialize_visual_templates()
        self.misconception_visuals = self._initialize_misconception_visuals()
        self.interactive_elements = self._initialize_interactive_elements()
    
    def generate_visual_suggestion(self, 
                                 problem_subject: Subject,
                                 problem_topic: str,
                                 detected_misconceptions: List[Misconception],
                                 current_stage: str = "initial") -> Optional[VisualSuggestion]:
        """
        Generate a visual suggestion based on the current context.
        
        Args:
            problem_subject: The subject being studied
            problem_topic: The specific topic within the subject
            detected_misconceptions: Any misconceptions detected
            current_stage: Current stage in problem-solving
            
        Returns:
            Visual suggestion or None if no visual is needed
        """
        # Determine if visual scaffolding is needed
        if not self._needs_visual_scaffolding(detected_misconceptions, current_stage):
            return None
        
        # Generate visual suggestion
        visual_type = self._determine_visual_type(problem_subject, problem_topic, detected_misconceptions)
        title = self._generate_title(visual_type, problem_topic)
        description = self._generate_description(visual_type, problem_topic, detected_misconceptions)
        elements = self._generate_visual_elements(visual_type, problem_subject, problem_topic)
        hints = self._generate_visual_hints(visual_type, detected_misconceptions)
        is_interactive = self._should_be_interactive(visual_type, current_stage)
        
        return VisualSuggestion(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            visual_type=visual_type,
            elements=elements,
            hints=hints,
            is_interactive=is_interactive
        )
    
    def _initialize_visual_templates(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Initialize visual templates for different subjects and topics."""
        return {
            Subject.STATICS: {
                "distributed_loads": {
                    "free_body_diagram": {
                        "title": "Free Body Diagram for Distributed Load",
                        "description": "A diagram showing all forces acting on the beam",
                        "elements": [
                            {"type": "beam", "properties": {"length": "L", "position": "horizontal"}},
                            {"type": "distributed_load", "properties": {"magnitude": "w", "direction": "downward"}},
                            {"type": "reaction_forces", "properties": {"left": "R1", "right": "R2"}},
                            {"type": "coordinate_system", "properties": {"origin": "left_support"}}
                        ],
                        "hints": [
                            "Draw the beam as a horizontal line",
                            "Represent the distributed load as a rectangle",
                            "Show reaction forces at both supports",
                            "Use consistent units for all forces"
                        ]
                    },
                    "equivalent_point_load": {
                        "title": "Equivalent Point Load Representation",
                        "description": "Converting distributed load to equivalent point load",
                        "elements": [
                            {"type": "beam", "properties": {"length": "L"}},
                            {"type": "point_load", "properties": {"magnitude": "w*L", "position": "L/2"}},
                            {"type": "centroid_marker", "properties": {"position": "L/2"}}
                        ],
                        "hints": [
                            "The equivalent force equals the area under the distributed load",
                            "The force acts at the centroid of the distributed load",
                            "For uniform loads, the centroid is at the middle"
                        ]
                    }
                },
                "general_statics": {
                    "equilibrium_diagram": {
                        "title": "Static Equilibrium Analysis",
                        "description": "Showing force and moment equilibrium",
                        "elements": [
                            {"type": "body", "properties": {"shape": "generic"}},
                            {"type": "forces", "properties": {"show_components": True}},
                            {"type": "moments", "properties": {"show_direction": True}},
                            {"type": "equilibrium_equations", "properties": {"visible": True}}
                        ]
                    }
                }
            },
            Subject.CIRCUIT_ANALYSIS: {
                "kirchhoff_laws": {
                    "circuit_schematic": {
                        "title": "Circuit Schematic with Current and Voltage Labels",
                        "description": "A circuit diagram showing current directions and voltage polarities",
                        "elements": [
                            {"type": "voltage_source", "properties": {"polarity": "marked"}},
                            {"type": "resistors", "properties": {"values": "labeled"}},
                            {"type": "current_arrows", "properties": {"direction": "assumed"}},
                            {"type": "nodes", "properties": {"labeled": True}}
                        ],
                        "hints": [
                            "Mark voltage polarities consistently",
                            "Choose current directions and stick to them",
                            "Label all nodes clearly",
                            "Show the reference direction for each current"
                        ]
                    },
                    "node_analysis_diagram": {
                        "title": "Node Analysis Setup",
                        "description": "Identifying nodes and applying KCL",
                        "elements": [
                            {"type": "nodes", "properties": {"numbered": True}},
                            {"type": "current_flows", "properties": {"into_node": True, "out_of_node": True}},
                            {"type": "kcl_equations", "properties": {"visible": True}}
                        ]
                    }
                }
            }
        }
    
    def _initialize_misconception_visuals(self) -> Dict[str, List[str]]:
        """Initialize visual suggestions for specific misconceptions."""
        return {
            "force_direction_error": [
                "free_body_diagram",
                "force_components_diagram"
            ],
            "missing_reactions": [
                "support_types_diagram",
                "reaction_force_diagram"
            ],
            "sign_convention_error": [
                "coordinate_system_diagram",
                "sign_convention_guide"
            ],
            "current_direction_error": [
                "current_direction_guide",
                "circuit_with_labels"
            ],
            "voltage_polarity_error": [
                "voltage_polarity_guide",
                "circuit_schematic"
            ]
        }
    
    def _initialize_interactive_elements(self) -> Dict[str, List[str]]:
        """Initialize interactive visual elements."""
        return {
            "free_body_diagram": [
                "draggable_forces",
                "adjustable_magnitudes",
                "real_time_equilibrium_check"
            ],
            "circuit_schematic": [
                "clickable_components",
                "adjustable_values",
                "real_time_calculation"
            ],
            "equivalent_point_load": [
                "slider_for_load_magnitude",
                "draggable_centroid",
                "instant_force_calculation"
            ]
        }
    
    def _needs_visual_scaffolding(self, misconceptions: List[Misconception], 
                                current_stage: str) -> bool:
        """Determine if visual scaffolding is needed."""
        
        # Always suggest visuals for critical misconceptions
        critical_misconceptions = [m for m in misconceptions if m.severity.value == "critical"]
        if critical_misconceptions:
            return True
        
        # Suggest visuals in early stages
        if current_stage in ["initial", "setup", "planning"]:
            return True
        
        # Suggest visuals if student seems confused
        if any("visual" in m.description.lower() for m in misconceptions):
            return True
        
        return False
    
    def _determine_visual_type(self, subject: Subject, topic: str, 
                             misconceptions: List[Misconception]) -> str:
        """Determine the most appropriate visual type."""
        
        # Check if misconceptions suggest specific visuals
        for misconception in misconceptions:
            if misconception.description in self.misconception_visuals:
                visual_types = self.misconception_visuals[misconception.description]
                return visual_types[0]  # Return first suggested visual
        
        # Default visuals based on subject and topic
        if subject == Subject.STATICS:
            if topic == "distributed_loads":
                return "free_body_diagram"
            else:
                return "equilibrium_diagram"
        
        elif subject == Subject.CIRCUIT_ANALYSIS:
            if topic == "kirchhoff_laws":
                return "circuit_schematic"
            else:
                return "circuit_schematic"
        
        return "general_diagram"
    
    def _generate_title(self, visual_type: str, topic: str) -> str:
        """Generate a title for the visual suggestion."""
        
        if visual_type == "free_body_diagram":
            return f"Free Body Diagram for {topic.replace('_', ' ').title()}"
        elif visual_type == "circuit_schematic":
            return f"Circuit Schematic for {topic.replace('_', ' ').title()}"
        elif visual_type == "equivalent_point_load":
            return "Equivalent Point Load Representation"
        else:
            return f"Visual Aid for {topic.replace('_', ' ').title()}"
    
    def _generate_description(self, visual_type: str, topic: str, 
                            misconceptions: List[Misconception]) -> str:
        """Generate a description for the visual suggestion."""
        
        if visual_type == "free_body_diagram":
            return "Draw a free body diagram showing all forces acting on the system. Include reaction forces, applied loads, and any distributed loads."
        
        elif visual_type == "circuit_schematic":
            return "Create a circuit diagram with all components labeled. Mark current directions and voltage polarities consistently."
        
        elif visual_type == "equivalent_point_load":
            return "Convert the distributed load to an equivalent point load. Show where this equivalent force should be placed."
        
        else:
            return f"A visual representation to help understand the {topic.replace('_', ' ')} concept."
    
    def _generate_visual_elements(self, visual_type: str, subject: Subject, 
                                topic: str) -> List[Dict[str, Any]]:
        """Generate the visual elements for the suggestion."""
        
        if subject in self.visual_templates and topic in self.visual_templates[subject]:
            topic_templates = self.visual_templates[subject][topic]
            
            if visual_type in topic_templates:
                return topic_templates[visual_type]["elements"]
        
        # Fallback elements
        return [
            {"type": "generic_element", "properties": {"description": "Basic visual element"}}
        ]
    
    def _generate_visual_hints(self, visual_type: str, 
                             misconceptions: List[Misconception]) -> List[str]:
        """Generate hints for creating the visual."""
        
        hints = []
        
        # Add general hints based on visual type
        if visual_type == "free_body_diagram":
            hints.extend([
                "Draw the body as a simple shape",
                "Show all external forces",
                "Use consistent units",
                "Mark force directions clearly"
            ])
        
        elif visual_type == "circuit_schematic":
            hints.extend([
                "Use standard circuit symbols",
                "Label all components",
                "Show current directions with arrows",
                "Mark voltage polarities"
            ])
        
        # Add specific hints for misconceptions
        for misconception in misconceptions:
            if "force direction" in misconception.description.lower():
                hints.append("Pay special attention to force directions")
            elif "missing" in misconception.description.lower():
                hints.append("Make sure you include all relevant elements")
            elif "sign" in misconception.description.lower():
                hints.append("Use consistent sign conventions")
        
        return hints
    
    def _should_be_interactive(self, visual_type: str, current_stage: str) -> bool:
        """Determine if the visual should be interactive."""
        
        # Interactive visuals for complex concepts
        if visual_type in ["free_body_diagram", "circuit_schematic"]:
            return True
        
        # Interactive for early stages
        if current_stage in ["initial", "exploration"]:
            return True
        
        return False
    
    def get_interactive_features(self, visual_type: str) -> List[str]:
        """Get available interactive features for a visual type."""
        
        if visual_type in self.interactive_elements:
            return self.interactive_elements[visual_type]
        
        return []
    
    def suggest_sketch_improvements(self, sketch_description: str, 
                                 subject: Subject, topic: str) -> List[str]:
        """Suggest improvements for a student's sketch."""
        
        improvements = []
        
        if subject == Subject.STATICS:
            if "free body diagram" in sketch_description.lower():
                if "missing forces" in sketch_description.lower():
                    improvements.append("Add all reaction forces at supports")
                    improvements.append("Include any applied loads")
                if "wrong direction" in sketch_description.lower():
                    improvements.append("Check force directions against standard conventions")
                    improvements.append("Use arrows to clearly show force directions")
        
        elif subject == Subject.CIRCUIT_ANALYSIS:
            if "circuit" in sketch_description.lower():
                if "missing labels" in sketch_description.lower():
                    improvements.append("Label all components with their values")
                    improvements.append("Mark current directions with arrows")
                if "wrong connections" in sketch_description.lower():
                    improvements.append("Verify all component connections")
                    improvements.append("Check that nodes are properly connected")
        
        return improvements
    
    def create_visual_summary(self, problem_subject: Subject, 
                            problem_topic: str, 
                            resolved_concepts: List[str]) -> VisualSuggestion:
        """Create a visual summary of the solved problem."""
        
        title = f"Summary Diagram: {problem_topic.replace('_', ' ').title()}"
        description = f"A comprehensive visual summary showing the key concepts and solution approach for {problem_topic}."
        
        elements = [
            {"type": "problem_setup", "properties": {"visible": True}},
            {"type": "solution_steps", "properties": {"numbered": True}},
            {"type": "key_concepts", "properties": {"highlighted": True}},
            {"type": "final_answer", "properties": {"boxed": True}}
        ]
        
        hints = [
            "Review the complete solution process",
            "Identify the key concepts used",
            "Note the relationships between different parts",
            "Understand how the visual elements relate to the math"
        ]
        
        return VisualSuggestion(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            visual_type="summary_diagram",
            elements=elements,
            hints=hints,
            is_interactive=False
        ) 