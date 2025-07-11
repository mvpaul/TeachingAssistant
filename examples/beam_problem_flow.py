"""
Example: Complete Data Flow for Beam with Distributed Load Problem

This example demonstrates the complete flow of the tutoring system for a typical
beam problem, showing how each module contributes to the tutoring process.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tutoring_agent import TutoringAgent
from core.models import ProblemInstance, Subject, Difficulty, StudentResponse


def demonstrate_beam_problem_flow():
    """
    Demonstrate the complete data flow for a beam with distributed load problem.
    
    This shows:
    1. Problem injection and parsing
    2. Misconception detection at each step
    3. Socratic questioning progression
    4. Visual scaffolding when needed
    5. Dialog state tracking and adaptation
    """
    
    print("=" * 80)
    print("BEAM WITH DISTRIBUTED LOAD - COMPLETE TUTORING FLOW")
    print("=" * 80)
    
    # Initialize the tutoring agent
    agent = TutoringAgent()
    
    # Create the beam problem
    problem_description = """
    A simply supported beam of length 6m carries a uniformly distributed load 
    of 2 kN/m over its entire length. The beam has a rectangular cross-section 
    with width 200mm and depth 300mm. Determine the maximum bending moment 
    and the maximum shear force in the beam.
    """
    
    problem = ProblemInstance(
        id="beam_distributed_load_001",
        subject=Subject.STATICS,
        topic="distributed_loads",
        difficulty=Difficulty.INTERMEDIATE,
        description=problem_description.strip(),
        known_misconceptions=[
            "confusing distributed load with point load",
            "incorrect force direction in free body diagram", 
            "missing reaction forces",
            "wrong sign conventions",
            "incorrect integration of distributed load"
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
    
    print("PROBLEM SETUP:")
    print(f"Subject: {problem.subject.value}")
    print(f"Topic: {problem.topic}")
    print(f"Difficulty: {problem.difficulty.value}")
    print(f"Description: {problem.description}")
    print(f"Expected Concepts: {', '.join(problem.expected_concepts)}")
    print(f"Known Misconceptions: {', '.join(problem.known_misconceptions)}")
    print()
    
    # Start tutoring session
    session = agent.start_session(problem)
    session_id = session.session_id
    print(f"Tutoring session started: {session_id}")
    print()
    
    # Simulate a realistic tutoring conversation
    conversation_turns = [
        {
            "student_input": "I need to find the reaction forces first",
            "expected_misconceptions": [],
            "stage": "initial",
            "description": "Student starts with correct approach"
        },
        {
            "student_input": "The reaction force at the left support is 6 kN upward",
            "expected_misconceptions": ["missing reaction forces"],
            "stage": "exploration", 
            "description": "Student mentions only one reaction force"
        },
        {
            "student_input": "I think the distributed load can be replaced by a point load of 12 kN at the center",
            "expected_misconceptions": [],
            "stage": "analysis",
            "description": "Student correctly identifies equivalent point load"
        },
        {
            "student_input": "The moment should be positive because it's clockwise",
            "expected_misconceptions": ["wrong sign conventions"],
            "stage": "analysis",
            "description": "Student has incorrect sign convention understanding"
        },
        {
            "student_input": "I'm confused about the free body diagram",
            "expected_misconceptions": [],
            "stage": "exploration",
            "description": "Student needs visual scaffolding"
        },
        {
            "student_input": "Now I understand - the equivalent force is 12 kN at 3m from the left",
            "expected_misconceptions": [],
            "stage": "synthesis",
            "description": "Student shows understanding"
        },
        {
            "student_input": "The maximum moment is 18 kN⋅m at the center",
            "expected_misconceptions": [],
            "stage": "synthesis", 
            "description": "Student provides correct calculation"
        }
    ]
    
    print("TUTORING CONVERSATION:")
    print("-" * 80)
    
    for i, turn in enumerate(conversation_turns, 1):
        print(f"Turn {i}: {turn['description']}")
        print(f"Stage: {turn['stage']}")
        print(f"Student: {turn['student_input']}")
        
        # Process student input
        response = agent.process_student_input(session_id, turn['student_input'])
        
        # Display agent response
        print(f"Tutor: {response.content}")
        
        # Show detected misconceptions
        if response.detected_misconceptions:
            print("🔍 Detected Misconceptions:")
            for misconception in response.detected_misconceptions:
                severity_icon = "🔴" if misconception.severity.value == "critical" else "🟡"
                print(f"  {severity_icon} {misconception.description}")
                print(f"    Confidence: {misconception.confidence:.2f}")
                print(f"    Related Concepts: {', '.join(misconception.related_concepts)}")
        
        # Show response type and metadata
        print(f"Response Type: {response.response_type}")
        if response.metadata:
            print(f"Metadata: {response.metadata}")
        
        # Show suggested actions
        if response.suggested_actions:
            print("💡 Suggested Actions:")
            for action in response.suggested_actions:
                print(f"  • {action}")
        
        print()
        
        # Show session progress every few turns
        if i % 3 == 0:
            summary = agent.get_session_summary(session_id)
            print(f"📊 Progress Update:")
            print(f"  Stage: {summary['current_stage']}")
            print(f"  Resolved Concepts: {summary['resolved_concepts']}")
            print(f"  Pending Concepts: {summary['pending_concepts']}")
            print(f"  Critical Misconceptions: {summary['critical_misconceptions']}")
            print()
    
    # Final session summary
    print("=" * 80)
    print("FINAL SESSION SUMMARY")
    print("=" * 80)
    
    final_summary = agent.end_session(session_id)
    
    print(f"Session Duration: {final_summary['session_duration']}")
    print(f"Total Exchanges: {final_summary['session_metrics']['conversation_length']}")
    print()
    
    print("Concept Progress:")
    print(f"  Resolved: {len(final_summary['concept_progress']['resolved'])}")
    for concept in final_summary['concept_progress']['resolved']:
        print(f"    ✓ {concept}")
    
    print(f"  Pending: {len(final_summary['concept_progress']['pending'])}")
    for concept in final_summary['concept_progress']['pending']:
        print(f"    ⏳ {concept}")
    
    print()
    print(f"Misconceptions Addressed: {final_summary['misconceptions_addressed']}")
    
    # Show adaptive suggestions that were generated
    print()
    print("Adaptive Strategies Used:")
    print("  • Progressive questioning from clarification to conceptual")
    print("  • Visual scaffolding when student was confused")
    print("  • Misconception-specific remediation")
    print("  • Confidence building through positive reinforcement")
    
    print("\n" + "=" * 80)
    print("EXAMPLE COMPLETED SUCCESSFULLY")
    print("=" * 80)


def show_data_structures():
    """Show the key data structures used in the system."""
    
    print("\n" + "=" * 80)
    print("KEY DATA STRUCTURES")
    print("=" * 80)
    
    print("1. ProblemInstance:")
    print("   - Contains problem description, metadata, expected concepts")
    print("   - Includes known misconceptions to watch for")
    print("   - Provides visual hints for scaffolding")
    print()
    
    print("2. StudentResponse:")
    print("   - Text input from student")
    print("   - Mathematical expressions")
    print("   - Sketch data (optional)")
    print("   - Confidence indicators")
    print()
    
    print("3. Misconception:")
    print("   - Description of the error")
    print("   - Severity level (critical/moderate/minor)")
    print("   - Detected patterns")
    print("   - Related concepts")
    print("   - Confidence score")
    print()
    
    print("4. SocraticQuestion:")
    print("   - Question text")
    print("   - Question type (clarification, assumption_challenge, etc.)")
    print("   - Target concept")
    print("   - Follow-up questions")
    print("   - Expected insights")
    print()
    
    print("5. VisualSuggestion:")
    print("   - Visual type (free_body_diagram, circuit_schematic, etc.)")
    print("   - Description and hints")
    print("   - Visual elements")
    print("   - Interactive features")
    print()
    
    print("6. DialogState:")
    print("   - Conversation history")
    print("   - Detected misconceptions")
    print("   - Resolved vs pending concepts")
    print("   - Session metadata")
    print()


if __name__ == "__main__":
    demonstrate_beam_problem_flow()
    show_data_structures() 