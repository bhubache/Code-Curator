from __future__ import annotations

from manim import Scene

from .animations.animation_generator import AnimationGenerator


class GeneratorScene(AnimationGenerator, Scene):
    """Provide connection between custom code and manim scene."""
