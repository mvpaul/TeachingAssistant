#!/usr/bin/env python3
"""
Simple Demo Script for the Tutoring Agent

This script demonstrates the tutoring system with a predefined conversation
flow, showing how the system detects misconceptions and provides guidance.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.tutoring_agent import TutoringAgent


def run_demo():
    """Run a demonstration of the tutoring system."""
    
    print("=" * 60)
    print("           STEM TUTORING AGENT DEMO")
    print("=" * 60)
    print("Demonstrating the complete tutoring flow with a beam problem")
    print("=" * 60)
    print()
    
    # Initialize the tutoring agent
    agent = TutoringAgent()
    
    # Create a beam problem
    problem = agent.create_beam_problem_example()
    
    print("PROBLEM:")
    print(f"Topic: {problem.topic.replace('_', ' ').title()}")
    print(f"Subject: {problem.subject.value}")
    print(f"Difficulty: {problem.difficulty.value}")
    print()
    print("Description:")
    print(problem.description)
    print()
    
    # Start a tutoring session
    session = agent.start_session(problem)
    session_id = session.session_id
    
    print("=" * 60)
    print("TUTORING SESSION")
    print("=" * 60)
    
    # Simulate a realistic tutoring conversation
    conversation = [
        {
            "input": "I think the reaction force is 500N",
            "description": "Student provides incorrect reaction force"
        },
        {
            "input": "I need to draw a free body diagram first",
            "description": "Student shows good problem-solving approach"
        },
        {
            "input": "The distributed load should be replaced by a point load at the center",
            "description": "Student correctly identifies equivalent point load concept"
        },
        {
            "input": "I'm not sure about the sign conventions for moments",
            "description": "Student expresses uncertainty about sign conventions"
        },
        {
            "input": "I understand now - the equivalent force equals the area under the distributed load",
            "description": "Student shows understanding of key concept"
        }
    ]
    
    for i, turn in enumerate(conversation, 1):
        print(f"\nTurn {i}: {turn['description']}")
        print(f"Student: {turn['input']}")
        
        # Process the student input
        response = agent.process_student_input(session_id, turn['input'])
        
        # Display the tutor's response
        if hasattr(response.content, 'question_text'):
            print(f"Tutor: {response.content.question_text}")
        elif hasattr(response.content, 'title'):
            print(f"Tutor: {response.content.description}")
            print(f"[Visual Aid: {response.content.title}]")
        else:
            print(f"Tutor: {response.content}")
        
        # Show detected misconceptions
        if response.detected_misconceptions:
            print("🔍 Detected Issues:")
            for misconception in response.detected_misconceptions:
                severity = "🔴 CRITICAL" if misconception.severity.value == "critical" else "🟡 MODERATE"
                print(f"  {severity}: {misconception.description}")
        
        # Show suggested actions
        if response.suggested_actions:
            print("💡 Suggested Actions:")
            for action in response.suggested_actions:
                print(f"  • {action}")
    
    # Get session summary
    print("\n" + "=" * 60)
    print("SESSION SUMMARY")
    print("=" * 60)
    
    summary = agent.get_session_summary(session_id)
    print(f"Current Stage: {summary['current_stage']}")
    print(f"Conversation Length: {summary['conversation_length']} exchanges")
    print(f"Resolved Concepts: {summary['resolved_concepts']}")
    print(f"Pending Concepts: {summary['pending_concepts']}")
    print(f"Critical Misconceptions: {summary['critical_misconceptions']}")
    
    # End the session
    final_summary = agent.end_session(session_id)
    
    print("\nFINAL RESULTS:")
    print(f"Session Duration: {final_summary['session_duration']}")
    print(f"Concepts Resolved: {len(final_summary['concept_progress']['resolved'])}")
    print(f"Concepts Pending: {len(final_summary['concept_progress']['pending'])}")
    print(f"Misconceptions Addressed: {final_summary['misconceptions_addressed']}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Key Features Demonstrated:")
    print("✓ Problem injection and parsing")
    print("✓ Misconception detection")
    print("✓ Socratic questioning")
    print("✓ Visual scaffolding")
    print("✓ Dialog state tracking")
    print("✓ Adaptive tutoring strategies")


if __name__ == "__main__":
    run_demo() 