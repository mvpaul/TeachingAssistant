# STEM Tutoring Agent Framework

A modular AI tutoring system designed for college-level STEM education that focuses on **conceptual understanding** rather than providing direct answers.

## Core Philosophy

This agent is designed to:
- **Detect conceptual red flags** in student reasoning
- **Engage in Socratic questioning** to guide self-discovery
- **Provide visual scaffolding** to support understanding
- **Diagnose errors** and guide students toward self-derived solutions

## Architecture Overview

```
TeachingAssistant/
├── core/                    # Core system components
│   ├── problem_injection.py # Problem parsing and structuring
│   ├── misconception_detector.py # Error detection engine
│   ├── socratic_engine.py   # Question generation logic
│   ├── visual_scaffolding.py # Diagram and visual suggestions
│   └── dialog_state.py      # Conversation memory and state
├── subjects/                # Subject-specific implementations
│   ├── statics/            # Statics problems and logic
│   └── circuit_analysis/   # Circuit analysis problems
├── ui/                     # User interface layer
├── data/                   # Problem databases and templates
└── tests/                  # Unit tests and integration tests
```

## Key Components

### 1. Problem Injection Module
- Parses structured problem prompts
- Extracts metadata (topic, difficulty, known misconceptions)
- Creates `ProblemInstance` objects for reasoning

### 2. Misconception Detector
- Analyzes user input (text, math, sketches)
- Flags conceptual errors and "red zone" mistakes
- Maps errors to specific remediation strategies

### 3. Socratic Engine
- Generates progressive questioning sequences
- Follows branching logic trees
- Challenges faulty reasoning without giving answers

### 4. Visual Scaffolding Generator
- Suggests relevant diagrams and visual aids
- Supports free body diagrams, circuit schematics, etc.
- Integrates with sketch-to-text tools

### 5. Dialog State Tracker
- Maintains conversational memory
- Tracks problem-solving progress
- Identifies unresolved conceptual gaps

## Usage Example

```python
from core.tutoring_agent import TutoringAgent
from subjects.statics.problems import BeamProblem

# Initialize the agent
agent = TutoringAgent()

# Start a tutoring session
problem = BeamProblem(
    description="A beam with distributed load...",
    difficulty="intermediate",
    topic="distributed_loads"
)

session = agent.start_session(problem)
response = agent.process_student_input("I think the reaction force is 500N")
```

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the demo script: `python3 demo.py`
3. Run the CLI interface: `python3 ui/cli_interface.py`
4. Or use the Python API directly

### Quick Demo

To see the system in action immediately:

```bash
python3 demo.py
```

This will run a complete tutoring session with a beam problem, showing:
- Problem injection and parsing
- Misconception detection
- Socratic questioning
- Visual scaffolding
- Dialog state tracking

## Development Status

- [x] Core architecture design
- [x] Basic module structure
- [ ] Subject-specific implementations
- [ ] UI layer development
- [ ] Problem database population 