from manim import *
from leetcode.problem_analysis.base_problem_analysis import BaseProblemAnalysis
from leetcode.problem_text import ProblemText
from singly_linked_list.singly_linked_list import SinglyLinkedList

from typing import Iterable

from .present_problem import CONSTRAINTS

EXPLANATIONS = []
EXPLANATIONS.append('Node is in the list and is not the tail node')
EXPLANATIONS.append('Not pertinent')
EXPLANATIONS.append('Not pertinent')
EXPLANATIONS.append('It\'s impossible to delete the tail')

class ProblemAnalysis(BaseProblemAnalysis):
    def __init__(self, problem_dir: str, aligned_animation_script):
        super().__init__(
            constraints=CONSTRAINTS,
            explanations=EXPLANATIONS,
            problem_dir=problem_dir,
            aligned_animation_script=aligned_animation_script
        )
        self.add_overriding_animation(self.explanation_1_pre)

    def explanation_1_pre(self) -> Iterable[Animation]:
        sll = SinglyLinkedList(0, 1)
        add_node_animation = AnimationGroup(*sll.add_last(2))

        square = Square()

        return [Wait(), FadeIn(square), square.animate.rotate(45)]

    def third_constraint_animation(self):
        title = ProblemText.create_title('Remove the value 2 from the linked list')
        title.to_edge(UP)
        sll = SinglyLinkedList(9, 2, 5, 2, 2)

        question_mark = ProblemText.create_statement('?')
        question_mark.next_to(sll, UP)

        return Succession(AnimationGroup(FadeIn(title), FadeIn(sll)), FadeIn(question_mark))