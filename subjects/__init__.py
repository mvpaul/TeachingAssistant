"""
Subject-specific implementations for the tutoring agent.

This package contains specialized logic and problem templates for different
STEM subjects like Statics and Circuit Analysis.
"""

from .statics import StaticsProblem
from .circuit_analysis import CircuitProblem

__all__ = ["StaticsProblem", "CircuitProblem"] 