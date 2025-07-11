"""
Statics Problem Templates and Logic

This module contains specialized problem templates and logic for statics problems.
"""

from typing import Dict, List, Any
from core.models import ProblemInstance, Subject, Difficulty


class StaticsProblem:
    """Specialized problem handling for statics."""
    
    @staticmethod
    def create_distributed_load_problem() -> ProblemInstance:
        """Create a distributed load problem."""
        return ProblemInstance(
            id="distributed_load_001",
            subject=Subject.STATICS,
            topic="distributed_loads",
            difficulty=Difficulty.INTERMEDIATE,
            description="""
            A simply supported beam of length 8m carries a uniformly distributed load 
            of 3 kN/m over its entire length. The beam has a rectangular cross-section 
            with width 250mm and depth 400mm. Determine:
            1. The reaction forces at the supports
            2. The maximum bending moment
            3. The maximum shear force
            """,
            known_misconceptions=[
                "confusing distributed load with point load",
                "incorrect force direction in free body diagram",
                "missing reaction forces",
                "wrong sign conventions"
            ],
            expected_concepts=[
                "force_equilibrium",
                "moment_equilibrium", 
                "free_body_diagrams",
                "distributed_load_integration",
                "equivalent_point_load",
                "centroid_calculation"
            ],
            visual_hints=[
                "Draw a free body diagram",
                "Show the distributed load as a rectangle",
                "Mark the centroid of the distributed load",
                "Include all reaction forces"
            ]
        )
    
    @staticmethod
    def create_truss_problem() -> ProblemInstance:
        """Create a truss analysis problem."""
        return ProblemInstance(
            id="truss_001",
            subject=Subject.STATICS,
            topic="truss_analysis",
            difficulty=Difficulty.INTERMEDIATE,
            description="""
            Analyze the simple truss structure. The truss has three members: AB, BC, and AC.
            A 15 kN force is applied at joint B. Determine the forces in all three members
            and identify which members are in tension and which are in compression.
            """,
            known_misconceptions=[
                "assuming all members are in tension",
                "incorrect joint equilibrium",
                "missing zero-force members"
            ],
            expected_concepts=[
                "force_equilibrium",
                "joint_analysis",
                "method_of_joints",
                "tension_compression_identification"
            ],
            visual_hints=[
                "Draw the truss structure",
                "Identify all joints",
                "Show force directions",
                "Apply equilibrium at each joint"
            ]
        )
    
    @staticmethod
    def create_equilibrium_problem() -> ProblemInstance:
        """Create a general equilibrium problem."""
        return ProblemInstance(
            id="equilibrium_001",
            subject=Subject.STATICS,
            topic="equilibrium",
            difficulty=Difficulty.BEGINNER,
            description="""
            A 50 kg block is placed on an inclined plane at 30 degrees to the horizontal.
            The coefficient of static friction is 0.3. Determine if the block will slide
            down the plane or remain in equilibrium.
            """,
            known_misconceptions=[
                "ignoring friction forces",
                "incorrect force decomposition",
                "wrong coordinate system"
            ],
            expected_concepts=[
                "force_equilibrium",
                "force_decomposition",
                "friction_forces",
                "coordinate_systems"
            ],
            visual_hints=[
                "Draw a free body diagram",
                "Show all forces acting on the block",
                "Use appropriate coordinate system",
                "Include friction force"
            ]
        )
    
    @staticmethod
    def get_problem_templates() -> Dict[str, Dict[str, Any]]:
        """Get all available problem templates."""
        return {
            "distributed_loads": {
                "description": "Problems involving distributed loads on beams",
                "difficulty_range": [Difficulty.INTERMEDIATE, Difficulty.ADVANCED],
                "key_concepts": ["integration", "centroid", "equivalent forces"],
                "common_misconceptions": [
                    "confusing distributed load with point load",
                    "incorrect centroid location",
                    "wrong integration limits"
                ]
            },
            "truss_analysis": {
                "description": "Analysis of truss structures using method of joints",
                "difficulty_range": [Difficulty.INTERMEDIATE, Difficulty.ADVANCED],
                "key_concepts": ["joint equilibrium", "method of joints", "zero-force members"],
                "common_misconceptions": [
                    "assuming all members are in tension",
                    "incorrect joint equilibrium",
                    "missing zero-force members"
                ]
            },
            "equilibrium": {
                "description": "Basic static equilibrium problems",
                "difficulty_range": [Difficulty.BEGINNER, Difficulty.INTERMEDIATE],
                "key_concepts": ["force equilibrium", "moment equilibrium", "free body diagrams"],
                "common_misconceptions": [
                    "missing forces in free body diagram",
                    "incorrect force directions",
                    "wrong moment calculations"
                ]
            }
        } 