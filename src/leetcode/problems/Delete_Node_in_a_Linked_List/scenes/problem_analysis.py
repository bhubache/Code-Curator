from manim import *
from leetcode.scenes.problem_analysis.base_problem_analysis import BaseProblemAnalysis
from leetcode.problem_text import ProblemText
from data_structures.singly_linked_list.singly_linked_list import SinglyLinkedList
from script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript

from typing import Iterable

from .present_problem import CONSTRAINTS

EXPLANATIONS = []
EXPLANATIONS.append('Node is in the list and is not the tail node')
EXPLANATIONS.append('Not pertinent')
EXPLANATIONS.append('Not pertinent')
EXPLANATIONS.append('It\'s impossible to delete the tail')

class ProblemAnalysis(BaseProblemAnalysis):
    def __init__(self, problem_dir: str, aligned_animation_scene: CompositeAnimationScript):
        super().__init__(
            constraints=CONSTRAINTS,
            explanations=EXPLANATIONS,
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene
        )
        self.add_overriding_animation(self.explanation_1)
        # self.add_overriding_animation(self.made_up_name)

    def explanation_1(self) -> Iterable[Animation]:
        sll = SinglyLinkedList(0, 1)

        return [Wait(), FadeIn(sll), Wait()]

    def third_constraint_animation(self):
        title = ProblemText.create_title('Remove the value 2 from the linked list')
        title.to_edge(UP)
        sll = SinglyLinkedList(9, 2, 5, 2, 2)

        question_mark = ProblemText.create_statement('?')
        question_mark.next_to(sll, UP)

        return Succession(AnimationGroup(FadeIn(title), FadeIn(sll)), FadeIn(question_mark))
