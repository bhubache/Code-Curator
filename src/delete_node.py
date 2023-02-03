from manim import *
from leetcode.problem_setup.present_problem import PresentProblem
from leetcode.problem_analysis import ProblemAnalysis
from singly_linked_list.singly_linked_list import SinglyLinkedList

class MyScene(PresentProblem, ProblemAnalysis):
    config.background_color = '#000E15'
    # config.disable_caching = True
    def construct(self):
        sll = SinglyLinkedList(0, 1, 2, 3)
        PresentProblem.construct(self)
        ProblemAnalysis.construct(self)
        # self.play(FadeIn(sll))
        self.wait()