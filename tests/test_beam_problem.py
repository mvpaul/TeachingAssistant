"""
Test script demonstrating the tutoring system with a beam problem.

This script shows the complete flow of:
1. Problem injection
2. Misconception detection
3. Socratic questioning
4. Visual scaffolding
5. Dialog state tracking
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tutoring_agent import TutoringAgent
from core.models import StudentResponse


def test_beam_problem_flow():
    """Test the complete flow with a beam problem."""
    
    print("=" * 60)
    print("TESTING TUTORING SYSTEM - BEAM PROBLEM")
    print("=" * 60)
    
    # Initialize the tutoring agent
    agent = TutoringAgent()
    
    # Create a beam problem
    problem = agent.create_beam_problem_example()
    print(f"Problem: {problem.topic}")
    print(f"Subject: {problem.subject.value}")
    print(f"Difficulty: {problem.difficulty.value}")
    print(f"Description: {problem.description.strip()}")
    print()
    
    # Start a tutoring session
    session = agent.start_session(problem)
    session_id = session.session_id
    print(f"Session started with ID: {session_id}")
    print()
    
    # Simulate student responses and track the conversation
    student_responses = [
        "I think the reaction force is 500N",
        "The distributed load should be treated as a point load at the center",
        "I'm not sure about the sign conventions for moments",
        "I understand now - the equivalent force equals the area under the distributed load"
    ]
    
    for i, response in enumerate(student_responses, 1):
        print(f"Turn {i}:")
        print(f"Student: {response}")
        
        # Process the response
        agent_response = agent.process_student_input(session_id, response)
        
        # Display the response
        print(f"Tutor: {agent_response.content}")
        
        if agent_response.detected_misconceptions:
            print("Detected misconceptions:")
            for misconception in agent_response.detected_misconceptions:
                severity = "🔴 CRITICAL" if misconception.severity.value == "critical" else "🟡 MODERATE"
                print(f"  {severity}: {misconception.description}")
        
        if agent_response.suggested_actions:
            print("Suggested actions:")
            for action in agent_response.suggested_actions:
                print(f"  • {action}")
        
        print()
    
    # Get session summary
    summary = agent.get_session_summary(session_id)
    print("Session Summary:")
    print(f"  Current Stage: {summary['current_stage']}")
    print(f"  Conversation Length: {summary['conversation_length']}")
    print(f"  Resolved Concepts: {summary['resolved_concepts']}")
    print(f"  Pending Concepts: {summary['pending_concepts']}")
    print(f"  Critical Misconceptions: {summary['critical_misconceptions']}")
    print()
    
    # Get adaptive suggestions
    suggestions = agent.get_adaptive_suggestions(session_id)
    if suggestions:
        print("Adaptive Suggestions:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
        print()
    
    # End the session
    final_summary = agent.end_session(session_id)
    print("Final Summary:")
    print(f"  Problem: {final_summary['problem']['topic']}")
    print(f"  Duration: {final_summary['session_duration']}")
    print(f"  Concepts Resolved: {len(final_summary['concept_progress']['resolved'])}")
    print(f"  Concepts Pending: {len(final_summary['concept_progress']['pending'])}")
    print(f"  Misconceptions Addressed: {final_summary['misconceptions_addressed']}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)


def test_misconception_detection():
    """Test specific misconception detection scenarios."""
    
    print("\n" + "=" * 60)
    print("TESTING MISCONCEPTION DETECTION")
    print("=" * 60)
    
    agent = TutoringAgent()
    problem = agent.create_beam_problem_example()
    session = agent.start_session(problem)
    session_id = session.session_id
    
    # Test different types of misconceptions
    misconception_tests = [
        {
            "response": "The reaction force is downward",
            "expected": "force direction error"
        },
        {
            "response": "I only need one reaction force",
            "expected": "missing reactions"
        },
        {
            "response": "The moment should be positive",
            "expected": "sign convention error"
        },
        {
            "response": "I'm not sure about this",
            "expected": "confidence issue"
        }
    ]
    
    for test in misconception_tests:
        print(f"Testing: '{test['response']}'")
        response = agent.process_student_input(session_id, test['response'])
        
        if response.detected_misconceptions:
            print("  Detected misconceptions:")
            for misconception in response.detected_misconceptions:
                print(f"    - {misconception.description}")
        else:
            print("  No misconceptions detected")
        print()
    
    agent.end_session(session_id)


def test_visual_scaffolding():
    """Test visual scaffolding generation."""
    
    print("\n" + "=" * 60)
    print("TESTING VISUAL SCAFFOLDING")
    print("=" * 60)
    
    agent = TutoringAgent()
    problem = agent.create_beam_problem_example()
    session = agent.start_session(problem)
    session_id = session.session_id
    
    # Test responses that should trigger visual suggestions
    visual_test_responses = [
        "I can't visualize this",
        "I don't know how to draw the diagram",
        "The forces are confusing me"
    ]
    
    for response in visual_test_responses:
        print(f"Student: {response}")
        agent_response = agent.process_student_input(session_id, response)
        
        if agent_response.response_type == "visual_scaffolding":
            print("  Visual suggestion generated!")
            visual = agent_response.content
            print(f"  Title: {visual.title}")
            print(f"  Description: {visual.description}")
            print(f"  Visual Type: {visual.visual_type}")
            if visual.hints:
                print("  Hints:")
                for hint in visual.hints:
                    print(f"    • {hint}")
        else:
            print("  No visual suggestion generated")
        print()
    
    agent.end_session(session_id)


if __name__ == "__main__":
    # Run all tests
    test_beam_problem_flow()
    test_misconception_detection()
    test_visual_scaffolding()
    
    print("\nAll tests completed!") 