from manim import *

'''
1. PresentProblem
2. ProblemAnalysis
3. IdentifyKeyPoints
4. DelveIntoKeyPoints
'''

from leetcode.problem_setup.present_problem import PresentProblem
from leetcode.problem_analysis import ProblemAnalysis

from singly_linked_list.singly_linked_list import SinglyLinkedList


sll = SinglyLinkedList(0, 1, 2, 3)

class MyScene(PresentProblem, ProblemAnalysis):
    config.background_color = '#000E15'
    # config.disable_caching = True
    def construct(self):
        PresentProblem.construct(self)
        ProblemAnalysis.construct(self)

    def setup(self):
        pass
        # PresentProblem.construct(self)
        # ProblemAnalysis.construct(self)

    def play_animations(self, animations):
        print(animations)
        for anim in animations:
            self.play(anim)
            self.wait(frozen_frame=False)