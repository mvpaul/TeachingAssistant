# STEM Tutoring Agent Architecture

## Overview

This document describes the architecture of the modular STEM tutoring agent system designed for college-level education. The system focuses on **conceptual understanding** rather than providing direct answers, using Socratic questioning and misconception detection to guide students toward self-discovery.

## Core Philosophy

The tutoring agent is built around these key principles:

1. **No Direct Answers**: The agent never provides solutions, only guidance
2. **Misconception Detection**: Identifies "red zone" errors that need immediate attention
3. **Socratic Questioning**: Uses progressive questioning to challenge assumptions
4. **Visual Scaffolding**: Provides diagrams and visual aids when needed
5. **Adaptive Tutoring**: Adjusts strategy based on student progress and responses

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Tutoring Agent                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │   Problem   │ │Misconception│ │  Socratic   │           │
│  │  Injection  │ │  Detector   │ │   Engine    │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
│  ┌─────────────┐ ┌─────────────┐                           │
│  │   Visual    │ │   Dialog    │                           │
│  │Scaffolding  │ │   State     │                           │
│  └─────────────┘ └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    User Interface                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │     CLI     │ │    Web      │ │   Python    │           │
│  │  Interface  │ │  Interface  │ │    API      │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Problem Injection Module (`core/problem_injection.py`)

**Purpose**: Parses and structures problem prompts for the tutoring agent.

**Key Functions**:
- `parse_problem()`: Converts raw problem text into structured `ProblemInstance`
- `_classify_subject()`: Identifies subject (Statics, Circuit Analysis, etc.)
- `_extract_topic()`: Determines specific topic within subject
- `_assess_difficulty()`: Evaluates problem complexity
- `_extract_known_misconceptions()`: Identifies common errors to watch for

**Data Flow**:
```
Raw Problem Text → ProblemInstance {
    subject: Subject,
    topic: str,
    difficulty: Difficulty,
    description: str,
    known_misconceptions: List[str],
    expected_concepts: List[str],
    visual_hints: List[str]
}
```

### 2. Misconception Detector (`core/misconception_detector.py`)

**Purpose**: Analyzes student responses to detect conceptual errors and misconceptions.

**Key Functions**:
- `detect_misconceptions()`: Main detection function
- `_analyze_text_response()`: Pattern matching for text-based errors
- `_analyze_mathematical_expressions()`: Mathematical error detection
- `_analyze_sketches()`: Visual misconception analysis
- `get_critical_misconceptions()`: Filters for "red zone" errors

**Detection Methods**:
- **Pattern Matching**: Regex patterns for common error phrases
- **Mathematical Analysis**: Symbolic math error detection
- **Visual Analysis**: Sketch/diagram error detection
- **Confidence Indicators**: Overconfidence or uncertainty detection

**Data Flow**:
```
StudentResponse → List[Misconception] {
    description: str,
    severity: ErrorSeverity,
    detected_patterns: List[str],
    related_concepts: List[str],
    confidence: float
}
```

### 3. Socratic Engine (`core/socratic_engine.py`)

**Purpose**: Generates progressive questioning sequences to guide student learning.

**Key Functions**:
- `generate_question()`: Creates contextually appropriate questions
- `_determine_question_type()`: Chooses question strategy
- `_generate_question_text()`: Creates actual question text
- `adapt_question_strategy()`: Adjusts based on student response

**Question Types**:
- **Clarification**: "What do you mean by...?"
- **Assumption Challenge**: "Why do you think...?"
- **Conceptual**: "What is the difference between...?"
- **Calculation Check**: "How did you arrive at...?"
- **Visual Aid**: "Can you draw a diagram...?"

**Data Flow**:
```
Context → SocraticQuestion {
    question_text: str,
    question_type: QuestionType,
    target_concept: str,
    follow_up_questions: List[str],
    expected_insights: List[str]
}
```

### 4. Visual Scaffolding (`core/visual_scaffolding.py`)

**Purpose**: Suggests relevant diagrams and visual aids to support understanding.

**Key Functions**:
- `generate_visual_suggestion()`: Creates visual aid recommendations
- `_determine_visual_type()`: Chooses appropriate visual type
- `_generate_visual_elements()`: Defines visual components
- `suggest_sketch_improvements()`: Provides sketch feedback

**Visual Types**:
- **Free Body Diagrams**: For statics problems
- **Circuit Schematics**: For circuit analysis
- **Equivalent Point Loads**: For distributed loads
- **Interactive Elements**: Draggable forces, adjustable values

**Data Flow**:
```
Context → VisualSuggestion {
    title: str,
    description: str,
    visual_type: str,
    elements: List[Dict],
    hints: List[str],
    is_interactive: bool
}
```

### 5. Dialog State Tracker (`core/dialog_state.py`)

**Purpose**: Maintains conversational memory and tracks problem-solving progress.

**Key Functions**:
- `add_student_response()`: Updates conversation state
- `get_current_stage()`: Determines problem-solving stage
- `should_suggest_visual()`: Decides when visual aids are needed
- `get_adaptive_suggestions()`: Provides strategy recommendations

**State Tracking**:
- **Conversation History**: All student-agent interactions
- **Concept Progress**: Resolved vs pending concepts
- **Misconception Evolution**: Detection and resolution tracking
- **Question Effectiveness**: Which questions work best

**Data Flow**:
```
Interaction → DialogState {
    conversation_history: List[Dict],
    detected_misconceptions: List[Misconception],
    resolved_concepts: List[str],
    pending_concepts: List[str],
    session_metadata: Dict
}
```

## Data Models

### Core Data Structures

1. **ProblemInstance**: Complete problem representation
2. **StudentResponse**: Student input (text, math, sketches)
3. **Misconception**: Detected conceptual error
4. **SocraticQuestion**: Generated question with metadata
5. **VisualSuggestion**: Visual aid recommendation
6. **DialogState**: Conversation state and progress
7. **AgentResponse**: Structured tutor response

### Enums and Constants

- **Subject**: STATICS, CIRCUIT_ANALYSIS
- **Difficulty**: BEGINNER, INTERMEDIATE, ADVANCED
- **ErrorSeverity**: MINOR, MODERATE, CRITICAL
- **QuestionType**: CLARIFICATION, ASSUMPTION_CHALLENGE, etc.

## Data Flow Example: Beam Problem

Here's how data flows through the system for a typical beam problem:

```
1. Problem Injection
   Raw Text → ProblemInstance {
       subject: STATICS,
       topic: "distributed_loads",
       difficulty: INTERMEDIATE,
       known_misconceptions: ["force direction errors", "missing reactions"]
   }

2. Student Response Processing
   "I think the reaction force is 500N" → StudentResponse

3. Misconception Detection
   StudentResponse → List[Misconception] {
       description: "Incorrect force direction assumption",
       severity: CRITICAL,
       confidence: 0.8
   }

4. Socratic Question Generation
   Context + Misconceptions → SocraticQuestion {
       question_text: "What forces are acting on the beam?",
       question_type: CLARIFICATION,
       target_concept: "force_equilibrium"
   }

5. Visual Scaffolding (if needed)
   Context → VisualSuggestion {
       title: "Free Body Diagram for Distributed Loads",
       visual_type: "free_body_diagram",
       hints: ["Draw the beam as a horizontal line", "Show all forces"]
   }

6. Dialog State Update
   Interaction → Updated DialogState {
       conversation_history: [...],
       detected_misconceptions: [...],
       resolved_concepts: [...]
   }
```

## Subject-Specific Implementations

### Statics (`subjects/statics/`)

**Topics Covered**:
- Distributed loads
- Truss analysis
- Equilibrium problems
- Free body diagrams

**Common Misconceptions**:
- Force direction errors
- Missing reaction forces
- Sign convention mistakes
- Integration errors

### Circuit Analysis (`subjects/circuit_analysis/`)

**Topics Covered**:
- Kirchhoff's laws
- Nodal analysis
- Mesh analysis
- Thevenin equivalents

**Common Misconceptions**:
- Current direction errors
- Voltage polarity mistakes
- Node conservation errors

## Extensibility

The system is designed to be easily extensible:

### Adding New Subjects

1. Create new subject directory: `subjects/new_subject/`
2. Implement subject-specific logic
3. Add to `Subject` enum
4. Update problem injection patterns
5. Add misconception detection rules

### Adding New Question Types

1. Extend `QuestionType` enum
2. Add question templates to Socratic engine
3. Implement question generation logic
4. Add follow-up strategies

### Adding New Visual Types

1. Define visual template in visual scaffolding
2. Add visual elements and hints
3. Implement interactive features
4. Update misconception-visual mappings

## Testing and Validation

### Test Structure

- **Unit Tests**: Individual module testing
- **Integration Tests**: End-to-end flow testing
- **Demo Scripts**: Complete system demonstrations

### Key Test Scenarios

1. **Misconception Detection**: Verify error pattern matching
2. **Question Generation**: Test Socratic questioning logic
3. **Visual Scaffolding**: Validate visual aid suggestions
4. **Dialog State**: Confirm conversation tracking
5. **Subject-Specific**: Test statics and circuit analysis

## Performance Considerations

### Scalability

- **Modular Design**: Easy to add new subjects/topics
- **Pattern Matching**: Efficient misconception detection
- **State Management**: Lightweight conversation tracking
- **Memory Usage**: Minimal session data storage

### Optimization Opportunities

- **Caching**: Question templates and patterns
- **Parallel Processing**: Multiple misconception detection
- **Lazy Loading**: Subject-specific modules
- **Session Persistence**: Database storage for long sessions

## Future Enhancements

### Planned Features

1. **Machine Learning Integration**: Improved misconception detection
2. **Natural Language Processing**: Better text analysis
3. **Interactive Visualizations**: Real-time diagram generation
4. **Multi-modal Input**: Voice, handwriting, gestures
5. **Collaborative Learning**: Multi-student sessions

### Research Directions

1. **Adaptive Learning**: Personalized question sequences
2. **Cognitive Modeling**: Student mental model tracking
3. **Emotional Intelligence**: Frustration and confidence detection
4. **Learning Analytics**: Detailed progress tracking
5. **A/B Testing**: Question effectiveness optimization

## Conclusion

This architecture provides a solid foundation for a sophisticated STEM tutoring system that prioritizes conceptual understanding over rote memorization. The modular design ensures extensibility while maintaining the core Socratic tutoring philosophy.

The system successfully demonstrates:
- **Modular Architecture**: Clean separation of concerns
- **Extensible Design**: Easy to add new subjects and features
- **Robust Error Detection**: Comprehensive misconception identification
- **Adaptive Tutoring**: Context-aware question generation
- **Visual Support**: Integrated scaffolding system
- **Progress Tracking**: Detailed learning analytics

This framework can serve as the foundation for advanced AI tutoring systems in STEM education. 