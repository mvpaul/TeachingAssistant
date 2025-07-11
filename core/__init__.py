"""
Core tutoring agent modules.

This package contains the fundamental components of the STEM tutoring system:
- Problem injection and parsing
- Misconception detection
- Socratic questioning engine
- Visual scaffolding generation
- Dialog state management
"""

from .problem_injection import ProblemInjection
from .misconception_detector import MisconceptionDetector
from .socratic_engine import SocraticEngine
from .visual_scaffolding import VisualScaffolding
from .dialog_state import DialogState
from .tutoring_agent import TutoringAgent

__all__ = [
    "ProblemInjection",
    "MisconceptionDetector", 
    "SocraticEngine",
    "VisualScaffolding",
    "DialogState",
    "TutoringAgent"
] 