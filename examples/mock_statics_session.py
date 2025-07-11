#!/usr/bin/env python3
"""
Mock Session: Student Solving Statics Problem Incorrectly

This example demonstrates how the tutoring system guides a student through
a statics problem step by step, showing the interaction between all modules
as they detect misconceptions and provide appropriate guidance.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tutoring_agent import TutoringAgent
from core.models import ProblemInstance, Subject, Difficulty, StudentResponse


def run_mock_statics_session():
    """
    Run a detailed mock session showing how the system guides a student
    through a statics problem with multiple misconceptions.
    """
    
    print("=" * 80)
    print("MOCK SESSION: STUDENT SOLVING STATICS PROBLEM INCORRECTLY")
    print("=" * 80)
    print("This session demonstrates how the tutoring system detects misconceptions")
    print("and guides the student toward correct reasoning through Socratic questioning.")
    print("=" * 80)
    print()
    
    # Initialize the tutoring agent
    agent = TutoringAgent()
    
    # Create a statics problem (beam with distributed load)
    problem = ProblemInstance(
        id="mock_statics_001",
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
    print()
    print("Problem Description:")
    print(problem.description.strip())
    print()
    print("Expected Concepts:", ", ".join(problem.expected_concepts))
    print("Known Misconceptions:", ", ".join(problem.known_misconceptions))
    print()
    
    # Start tutoring session
    session = agent.start_session(problem)
    session_id = session.session_id
    
    print("=" * 80)
    print("TUTORING SESSION BEGINS")
    print("=" * 80)
    
    # Simulate a realistic conversation with multiple misconceptions
    conversation = [
        {
            "turn": 1,
            "student_input": "I need to find the reaction forces first",
            "description": "Student starts with correct approach",
            "expected_behavior": "System should encourage this good start",
            "modules_involved": ["Dialog State", "Socratic Engine"]
        },
        {
            "turn": 2,
            "student_input": "The reaction force at the left support is 12 kN upward",
            "description": "Student mentions only one reaction force - CRITICAL MISCONCEPTION",
            "expected_behavior": "System should detect missing reaction forces and challenge assumption",
            "modules_involved": ["Misconception Detector", "Socratic Engine", "Visual Scaffolding"]
        },
        {
            "turn": 3,
            "student_input": "I think the distributed load can be treated as a point load of 24 kN at the center",
            "description": "Student correctly identifies equivalent point load concept",
            "expected_behavior": "System should acknowledge good understanding",
            "modules_involved": ["Dialog State", "Socratic Engine"]
        },
        {
            "turn": 4,
            "student_input": "The moment should be positive because it's clockwise",
            "description": "Student has incorrect sign convention understanding",
            "expected_behavior": "System should detect sign convention error and provide guidance",
            "modules_involved": ["Misconception Detector", "Socratic Engine"]
        },
        {
            "turn": 5,
            "student_input": "I'm confused about the free body diagram",
            "description": "Student needs visual scaffolding",
            "expected_behavior": "System should provide visual aid suggestion",
            "modules_involved": ["Dialog State", "Visual Scaffolding"]
        },
        {
            "turn": 6,
            "student_input": "Now I see - I need both reaction forces R1 and R2",
            "description": "Student corrects the missing reaction force misconception",
            "expected_behavior": "System should acknowledge progress and move to next concept",
            "modules_involved": ["Dialog State", "Socratic Engine"]
        },
        {
            "turn": 7,
            "student_input": "The equivalent force is 24 kN at 4m from the left support",
            "description": "Student shows understanding of equivalent point load",
            "expected_behavior": "System should acknowledge concept mastery",
            "modules_involved": ["Dialog State", "Socratic Engine"]
        },
        {
            "turn": 8,
            "student_input": "I understand now - clockwise moments are negative in standard convention",
            "description": "Student corrects sign convention misconception",
            "expected_behavior": "System should acknowledge correction and guide to final calculation",
            "modules_involved": ["Dialog State", "Socratic Engine"]
        },
        {
            "turn": 9,
            "student_input": "The maximum moment is 24 kN⋅m at the center of the beam",
            "description": "Student provides final calculation",
            "expected_behavior": "System should acknowledge completion and provide summary",
            "modules_involved": ["Dialog State", "Socratic Engine"]
        }
    ]
    
    for turn_data in conversation:
        print(f"\n{'='*60}")
        print(f"TURN {turn_data['turn']}: {turn_data['description']}")
        print(f"{'='*60}")
        print(f"Expected Behavior: {turn_data['expected_behavior']}")
        print(f"Modules Involved: {', '.join(turn_data['modules_involved'])}")
        print()
        
        print(f"Student: {turn_data['student_input']}")
        
        # Process the student input
        response = agent.process_student_input(session_id, turn_data['student_input'])
        
        # Display detailed response analysis
        print(f"\nTutor Response:")
        
        # Show the actual response content
        if hasattr(response.content, 'question_text'):
            print(f"  Question: {response.content.question_text}")
            print(f"  Type: {response.content.question_type.value}")
            print(f"  Target Concept: {response.content.target_concept}")
        elif hasattr(response.content, 'title') and hasattr(response.content, 'description'):
            print(f"  Visual Aid: {response.content.title}")
            print(f"  Description: {response.content.description}")
            print(f"  Type: {response.content.visual_type}")
        elif isinstance(response.content, str):
            print(f"  Response: {response.content}")
        else:
            print(f"  Response: {str(response.content)}")
        
        # Show detected misconceptions
        if response.detected_misconceptions:
            print(f"\n🔍 Misconception Detector Results:")
            for misconception in response.detected_misconceptions:
                severity_icon = "🔴 CRITICAL" if misconception.severity.value == "critical" else "🟡 MODERATE"
                print(f"  {severity_icon}: {misconception.description}")
                print(f"    Confidence: {misconception.confidence:.2f}")
                print(f"    Related Concepts: {', '.join(misconception.related_concepts)}")
                print(f"    Detected Patterns: {', '.join(misconception.detected_patterns)}")
        else:
            print(f"\n✅ No misconceptions detected")
        
        # Show response type and strategy
        print(f"\n📊 Response Analysis:")
        print(f"  Response Type: {response.response_type}")
        print(f"  Confidence: {response.confidence:.2f}")
        if response.metadata:
            print(f"  Current Stage: {response.metadata.get('current_stage', 'unknown')}")
            print(f"  Question Type: {response.metadata.get('question_type', 'none')}")
        
        # Show suggested actions
        if response.suggested_actions:
            print(f"\n💡 Suggested Actions:")
            for action in response.suggested_actions:
                print(f"  • {action}")
        
        # Show session progress every few turns
        if turn_data['turn'] % 3 == 0:
            summary = agent.get_session_summary(session_id)
            print(f"\n📈 Progress Update:")
            print(f"  Stage: {summary['current_stage']}")
            print(f"  Resolved Concepts: {summary['resolved_concepts']}")
            print(f"  Pending Concepts: {summary['pending_concepts']}")
            print(f"  Critical Misconceptions: {summary['critical_misconceptions']}")
    
    # Final session analysis
    print("\n" + "="*80)
    print("SESSION ANALYSIS")
    print("="*80)
    
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
    
    # Show learning progression
    print("\n" + "="*80)
    print("LEARNING PROGRESSION ANALYSIS")
    print("="*80)
    
    print("Key Misconceptions Corrected:")
    print("  1. Missing reaction forces → Student learned to include both supports")
    print("  2. Incorrect sign conventions → Student learned standard moment conventions")
    print("  3. Visual confusion → Student used free body diagram effectively")
    
    print("\nConcept Mastery Progression:")
    print("  ✓ Force equilibrium - Student understood need for force balance")
    print("  ✓ Equivalent point load - Student correctly calculated 24 kN at centroid")
    print("  ✓ Free body diagrams - Student used visual aids effectively")
    print("  ✓ Sign conventions - Student learned standard conventions")
    print("  ✓ Moment calculations - Student completed final calculation")
    
    print("\nTutoring Strategy Effectiveness:")
    print("  • Socratic questioning guided student to self-discovery")
    print("  • Visual scaffolding provided when student was confused")
    print("  • Misconception detection caught critical errors early")
    print("  • Progressive difficulty increased as student improved")
    print("  • Positive reinforcement maintained student engagement")
    
    print("\n" + "="*80)
    print("MOCK SESSION COMPLETED SUCCESSFULLY!")
    print("="*80)
    print()
    print("This session demonstrates how the tutoring system:")
    print("✓ Detects misconceptions in real-time")
    print("✓ Provides appropriate Socratic questions")
    print("✓ Offers visual scaffolding when needed")
    print("✓ Tracks student progress and adapts strategy")
    print("✓ Guides students toward correct reasoning without giving answers")


def show_module_interactions():
    """Show how each module interacts during the session."""
    
    print("\n" + "="*80)
    print("MODULE INTERACTION ANALYSIS")
    print("="*80)
    
    print("1. PROBLEM INJECTION MODULE")
    print("   Input: Raw problem text")
    print("   Output: Structured ProblemInstance")
    print("   Key Functions:")
    print("     • Subject classification (Statics)")
    print("     • Topic extraction (distributed_loads)")
    print("     • Difficulty assessment (Intermediate)")
    print("     • Misconception identification")
    print("     • Expected concept mapping")
    print()
    
    print("2. MISCONCEPTION DETECTOR")
    print("   Input: StudentResponse")
    print("   Output: List[Misconception]")
    print("   Detection Methods:")
    print("     • Pattern matching: 'only one reaction' → missing reactions")
    print("     • Mathematical analysis: sign convention errors")
    print("     • Confidence indicators: uncertainty detection")
    print("     • Context analysis: force direction errors")
    print()
    
    print("3. SOCRATIC ENGINE")
    print("   Input: Context + Misconceptions")
    print("   Output: SocraticQuestion")
    print("   Question Strategies:")
    print("     • Clarification: 'What forces are acting on the beam?'")
    print("     • Assumption Challenge: 'Why do you think...?'")
    print("     • Conceptual: 'What is the difference between...?'")
    print("     • Visual Aid: 'Can you draw a diagram...?'")
    print()
    
    print("4. VISUAL SCAFFOLDING")
    print("   Input: Context + Misconceptions")
    print("   Output: VisualSuggestion")
    print("   Visual Types:")
    print("     • Free body diagrams for force analysis")
    print("     • Equivalent point load representations")
    print("     • Interactive force diagrams")
    print("     • Step-by-step solution guides")
    print()
    
    print("5. DIALOG STATE TRACKER")
    print("   Input: All interactions")
    print("   Output: Updated DialogState")
    print("   Tracking Elements:")
    print("     • Conversation history")
    print("     • Concept progress (resolved vs pending)")
    print("     • Misconception evolution")
    print("     • Question effectiveness")
    print("     • Session metadata")
    print()
    
    print("DATA FLOW SUMMARY:")
    print("Student Input → Misconception Detector → Socratic Engine → Visual Scaffolding")
    print("                ↓")
    print("            Dialog State Tracker")
    print("                ↓")
    print("            Adaptive Strategy Selection")


if __name__ == "__main__":
    run_mock_statics_session()
    show_module_interactions() 