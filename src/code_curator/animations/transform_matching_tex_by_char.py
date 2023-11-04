from __future__ import annotations

from manim import BulletedList
from manim import Mobject
from manim import SingleStringMathTex
from manim import TransformMatchingTex


class TransformMatchingTexByChar(TransformMatchingTex):
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        **kwargs,
    ) -> None:
        self.target_tex_mobjects: list[SingleStringMathTex] = self._get_tex_mobjects(target_mobject)
        self.source_map = {}
        self.target_map = {}

        overall_index: int = 0

        start: int = 0
        end: int = 0

        # TODO: Account for case folding
        # TODO: Account for whitespace

        curr_word: str = ""

        for submobject in self.target_tex_mobjects:
            for target_char in submobject.tex_string:
                if self.mobject.tex_string[overall_index] == target_char:
                    end += 1
                    # NOTE: Assume only single space separating words
                    if target_char.strip() == "":
                        curr_word = ""
                else:
                    self.source_map[self.mobject.tex_string]





        breakpoint()
        # super().

    def _get_tex_mobjects(self, mobject: Mobject) -> list[SingleStringMathTex]:
        if isinstance(mobject, SingleStringMathTex) and not isinstance(mobject, BulletedList):
            return [mobject]

        tex_mobjects = []
        for submobject in mobject.submobjects:
            tex_mobjects.extend(
                self._get_tex_mobjects(submobject)
            )

        return tex_mobjects

