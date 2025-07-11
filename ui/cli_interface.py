"""
Command Line Interface for the Tutoring Agent

A simple CLI to demonstrate the tutoring system functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tutoring_agent import TutoringAgent
from core.models import ProblemInstance, Subject, Difficulty


def print_banner():
    """Print the application banner."""
    print("=" * 60)
    print("           STEM TUTORING AGENT DEMO")
    print("=" * 60)
    print("A modular AI tutoring system for college-level STEM education")
    print("Focus: Conceptual understanding through Socratic questioning")
    print("=" * 60)
    print()


def print_help():
    """Print help information."""
    print("Available commands:")
    print("  start <subject> <topic>  - Start a new tutoring session")
    print("  subjects                 - List available subjects")
    print("  topics <subject>         - List available topics for a subject")
    print("  example                  - Start with example beam problem")
    print("  help                     - Show this help message")
    print("  quit                     - Exit the application")
    print()


def list_subjects():
    """List available subjects."""
    print("Available subjects:")
    print("  - statics")
    print("  - circuit_analysis")
    print()


def list_topics(subject: str):
    """List available topics for a subject."""
    if subject.lower() == "statics":
        print("Available topics for Statics:")
        print("  - distributed_loads")
        print("  - truss_analysis")
        print("  - beam_analysis")
        print("  - equilibrium")
        print("  - general_statics")
    elif subject.lower() == "circuit_analysis":
        print("Available topics for Circuit Analysis:")
        print("  - kirchhoff_laws")
        print("  - nodal_analysis")
        print("  - mesh_analysis")
        print("  - thevenin_equivalent")
        print("  - general_circuits")
    else:
        print(f"Unknown subject: {subject}")
        list_subjects()


def create_problem_instance(subject: str, topic: str) -> ProblemInstance:
    """Create a problem instance based on subject and topic."""
    
    if subject.lower() == "statics":
        if topic.lower() == "distributed_loads":
            description = """
            A simply supported beam of length 6m carries a uniformly distributed load 
            of 2 kN/m over its entire length. The beam has a rectangular cross-section 
            with width 200mm and depth 300mm. Determine the maximum bending moment 
            and the maximum shear force in the beam.
            """
        elif topic.lower() == "truss_analysis":
            description = """
            Analyze the truss structure shown. Determine the forces in members AB, BC, 
            and CD. The truss is loaded with a 10 kN force at joint B.
            """
        else:
            description = f"General statics problem involving {topic.replace('_', ' ')}"
        
        return ProblemInstance(
            id="demo_problem",
            subject=Subject.STATICS,
            topic=topic.lower(),
            difficulty=Difficulty.INTERMEDIATE,
            description=description.strip()
        )
    
    elif subject.lower() == "circuit_analysis":
        if topic.lower() == "kirchhoff_laws":
            description = """
            Analyze the circuit with a 12V voltage source and three resistors 
            (R1=4Ω, R2=6Ω, R3=8Ω) connected in series. Determine the current 
            through each resistor and the voltage drop across each.
            """
        else:
            description = f"General circuit analysis problem involving {topic.replace('_', ' ')}"
        
        return ProblemInstance(
            id="demo_problem",
            subject=Subject.CIRCUIT_ANALYSIS,
            topic=topic.lower(),
            difficulty=Difficulty.INTERMEDIATE,
            description=description.strip()
        )
    
    else:
        raise ValueError(f"Unknown subject: {subject}")


def run_tutoring_session(agent: TutoringAgent, problem: ProblemInstance):
    """Run an interactive tutoring session."""
    
    print(f"\nStarting tutoring session for: {problem.topic.replace('_', ' ').title()}")
    print(f"Subject: {problem.subject.value}")
    print(f"Difficulty: {problem.difficulty.value}")
    print("\nProblem:")
    print(problem.description)
    print("\n" + "="*60)
    
    # Start session
    session = agent.start_session(problem)
    session_id = session.session_id
    
    print("Tutoring session started! Type 'quit' to end the session.")
    print("Type 'help' for session commands.")
    print()
    
    while True:
        try:
            # Get student input with proper error handling
            try:
                student_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nSession ended by user.")
                break
            
            if student_input.lower() == 'quit':
                break
            elif student_input.lower() == 'help':
                print_session_help()
                continue
            elif student_input.lower() == 'summary':
                summary = agent.get_session_summary(session_id)
                print_session_summary(summary)
                continue
            elif student_input.lower() == 'suggestions':
                suggestions = agent.get_adaptive_suggestions(session_id)
                print_adaptive_suggestions(suggestions)
                continue
            elif not student_input:
                continue
            
            # Process input
            response = agent.process_student_input(session_id, student_input)
            
            # Display response
            print_agent_response(response)
            
        except Exception as e:
            print(f"Error processing input: {e}")
            continue
    
    # End session
    final_summary = agent.end_session(session_id)
    print("\n" + "="*60)
    print("SESSION ENDED")
    print("="*60)
    print_final_summary(final_summary)


def print_session_help():
    """Print help for session commands."""
    print("\nSession commands:")
    print("  help        - Show this help")
    print("  summary     - Show session summary")
    print("  suggestions - Show adaptive suggestions")
    print("  quit        - End the session")
    print()


def print_agent_response(response):
    """Print the agent's response in a formatted way."""
    
    # Handle different response types
    if hasattr(response.content, 'question_text'):
        # Socratic question
        print(f"\nTutor: {response.content.question_text}")
    elif hasattr(response.content, 'title'):
        # Visual suggestion
        print(f"\nTutor: {response.content.description}")
        print(f"[Visual Aid: {response.content.title}]")
        if response.content.hints:
            print("Hints:")
            for hint in response.content.hints:
                print(f"  • {hint}")
    else:
        # Plain text response
        print(f"\nTutor: {response.content}")
    
    if response.detected_misconceptions:
        print("\n[Detected Issues:]")
        for misconception in response.detected_misconceptions:
            severity_icon = "🔴" if misconception.severity.value == "critical" else "🟡"
            print(f"  {severity_icon} {misconception.description}")
    
    if response.suggested_actions:
        print("\n[Suggested Actions:]")
        for action in response.suggested_actions:
            print(f"  • {action}")
    
    print()


def print_session_summary(summary):
    """Print session summary."""
    print(f"\nSession Summary:")
    print(f"  Current Stage: {summary['current_stage']}")
    print(f"  Conversation Length: {summary['conversation_length']} exchanges")
    print(f"  Resolved Concepts: {summary['resolved_concepts']}")
    print(f"  Pending Concepts: {summary['pending_concepts']}")
    print(f"  Critical Misconceptions: {summary['critical_misconceptions']}")
    print()


def print_adaptive_suggestions(suggestions):
    """Print adaptive suggestions."""
    if suggestions:
        print("\nAdaptive Suggestions:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    else:
        print("\nNo adaptive suggestions at this time.")
    print()


def print_final_summary(summary):
    """Print final session summary."""
    print(f"Final Session Summary:")
    print(f"  Problem: {summary['problem']['topic'].replace('_', ' ').title()}")
    print(f"  Subject: {summary['problem']['subject']}")
    print(f"  Duration: {summary['session_duration']}")
    print(f"  Concepts Resolved: {len(summary['concept_progress']['resolved'])}")
    print(f"  Concepts Pending: {len(summary['concept_progress']['pending'])}")
    print(f"  Misconceptions Addressed: {summary['misconceptions_addressed']}")
    print()


def main():
    """Main application loop."""
    print_banner()
    
    # Initialize tutoring agent
    agent = TutoringAgent()
    
    print_help()
    
    while True:
        try:
            # Get command with proper error handling
            try:
                command = input("tutor> ").strip().split()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == "quit":
                print("Goodbye!")
                break
            elif cmd == "help":
                print_help()
            elif cmd == "subjects":
                list_subjects()
            elif cmd == "topics":
                if len(command) < 2:
                    print("Usage: topics <subject>")
                else:
                    list_topics(command[1])
            elif cmd == "example":
                problem = agent.create_beam_problem_example()
                run_tutoring_session(agent, problem)
            elif cmd == "start":
                if len(command) < 3:
                    print("Usage: start <subject> <topic>")
                    print("Example: start statics distributed_loads")
                else:
                    try:
                        problem = create_problem_instance(command[1], command[2])
                        run_tutoring_session(agent, problem)
                    except ValueError as e:
                        print(f"Error: {e}")
            else:
                print(f"Unknown command: {cmd}")
                print_help()
                
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == "__main__":
    main() 