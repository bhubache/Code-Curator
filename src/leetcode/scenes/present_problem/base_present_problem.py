import os
from typing import Iterable, final

from manim import *
from base_scene import BaseScene
from leetcode.problem_text import ProblemText
from script_handling.components.animation_script.animation_leaf import AnimationLeaf

'''
TODO
- Allow person to put in basic text and have parser convert it to something that's readable by Tex
'''

TITLE = 'Delete Node in a Linked List'
STATEMENT = 'Write a function to delete a node in a singly linked list. You will not be given access to the head of the list, instead you will be given access to the node to be deleted directly.'
CONSTRAINTS = []
CONSTRAINTS.append('The number of nodes in the given list is in the range [2, 1000]')
CONSTRAINTS.append('-1000 $\leq$ Node.val $\leq$ 1000')
CONSTRAINTS.append('The value of each node in the list is unique')
CONSTRAINTS.append('The node to be deleted is in the list and is not a tail node')

class BasePresentProblem(BaseScene):
    def __init__(self,
                 title = TITLE,
                 statement_header = 'Statement',
                 statement = STATEMENT,
                 constraints_header = 'Constraints',
                 constraints = CONSTRAINTS,
                 problem_dir = None,
                 aligned_animation_scene = None):
        BaseScene.__init__(self, problem_dir=problem_dir, aligned_animation_scene=aligned_animation_scene)
        self._title = ProblemText.create_title(title)
        self._statement_header = ProblemText.create_header(statement_header)
        self._statement = ProblemText.create_statement(statement)
        self._constraints_header = ProblemText.create_header(constraints_header)
        self._constraints = ProblemText.create_constraints_list(constraints)
        self._problem_dir = problem_dir
        # self._animation_timer = AnimationTimer(
        #     script_path=os.path.join(problem_dir, 'script.txt'),
        #     alignment_path=os.path.join(problem_dir, 'aligned_script.txt')
        # )

        # self._animation_timings = self._animation_timer.get_timings()

        # self._title_key, self._statement_header_key, self._statement_key, self._constraints_header_key, self._consraints_key = self._animation_timings.keys()

        # self._title_key = self._animation_timer._script_keys[0]
        # self._statement_header_key = self._animation_timer._script_keys[1]
        # self._statement_key = self._animation_timer._script_keys[2]
        # self._constraints_header_key = self._animation_timer._script_keys[3]
        # self._constraints_key = '<constraints>'

        # animation_spec breaks the PresentProblem Scene down into its major components:
        # - title
        # - statement header
        # - statement
        # - constraint header
        # - constraints
        #
        # To allow flexibility in creating a scene, every section is made up of three portions: pre, during, and post
        # The value of these three keys must be either an Animation of some kind, or a dictionary that follows the same
        # structure (this enables recursion)
        # self._animation_spec = {
        #     self._title_key: {
        #         'pre': None,
        #         'during': self.present_problem_title(self._animation_timings[self._title_key]),
        #         'post': None
        #     },
        #     self._statement_header_key: {
        #         'pre': None,
        #         'during': self.present_problem_statement_header(self._animation_timings[self._statement_header_key]),
        #         'post': None
        #     },
        #     self._statement_key: {
        #         'pre': None,
        #         'during': self.present_problem_statement(self._animation_timings[self._statement_key]),
        #         'post': None
        #     },
        #     self._constraints_header_key: {
        #         'pre': None,
        #         'during': self.present_problem_constraints_header(self._animation_timings[self._constraints_header_key]),
        #         'post': None
        #     },
        #     self._constraints_key: {
        #         'pre': None,
        #         'during': self._init_constraints_animations(),
        #         'post': None
        #     },
        # }

        self._animation_spec = self.create_animation_spec()

    def create_animation_spec(self):
        spec = {
            'title': self.present_problem_title(self.aligned_animation_scene.get_child('title')),
            'statement_header': self.present_problem_statement_header(),
            'statement': self.present_problem_statement(),
            'constraints_header': self.present_problem_constraints_header(),
            # **self._init_constraints_animations()
            }
        return spec

    def setup(self):
        super().setup()

    def construct(self):
        super().construct()
        # self.run_animations()

    def tear_down(self):
        super().tear_down()
        # self.play(FadeOut(*self.mobjects))

    def _init_constraints_animations(self):
        constraints_dict = {}
        for index in range(1, len(self._constraints) + 1):
            if index == 0: continue
            constraints_dict[index] = self.present_single_problem_constraint(index=index)
        return constraints_dict

    def present_problem_title(self, aligned_animation_section: AnimationLeaf):
        def inner():
            return [
                FadeIn(self._title, run_time)
            ]
            return [FadeIn(self._title), Wait(), self._title.animate.to_edge(UP)]
        return inner

    def present_problem_statement_header(self):
        # def inner():
        self._position_element_below_other(self._statement_header, self._title)
        return [FadeIn(self._statement_header)]
        # return inner

    def present_problem_statement(self):
        # def inner():
        self._position_element_below_other(self._statement, self._statement_header)
        return [FadeIn(self._statement)]
        # return inner

    def present_problem_constraints_header(self):
        # def inner():
        self._position_element_below_other(self._constraints_header, self._statement)
        return [FadeIn(self._constraints_header)]
        # return inner

    def present_single_problem_constraint(self, index):
        # def inner():
        self._position_element_below_other(self._constraints, self._constraints_header)
        return [FadeIn(self._constraints[index])]
        # return inner

    def _position_element_below_other(self, element, other):
        element.next_to(other, DOWN)
        element.to_edge(LEFT)