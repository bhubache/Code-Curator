from manim import *

# from problem_setup.problem_text import ProblemText
# from problem_text import ProblemText

from base_scene import BaseScene
from leetcode.problem_text import ProblemText
# from .animation_timer import AnimationTimer
import os

from typing import Iterable

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
                 problem_dir = None):
        BaseScene.__init__(self, problem_dir=problem_dir)
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

        self._title_key, self._statement_header_key, self._statement_key, self._constraints_header_key, self._consraints_key = self._animation_timings.keys()

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
        self._animation_spec = {
            self._title_key: {
                'pre': None,
                'during': self.present_problem_title(self._animation_timings[self._title_key]),
                'post': None
            },
            self._statement_header_key: {
                'pre': None,
                'during': self.present_problem_statement_header(self._animation_timings[self._statement_header_key]),
                'post': None
            },
            self._statement_key: {
                'pre': None,
                'during': self.present_problem_statement(self._animation_timings[self._statement_key]),
                'post': None
            },
            self._constraints_header_key: {
                'pre': None,
                'during': self.present_problem_constraints_header(self._animation_timings[self._constraints_header_key]),
                'post': None
            },
            self._constraints_key: {
                'pre': None,
                'during': self._init_constraints_animations(),
                'post': None
            },
        }

    def setup(self):
        pass

    def construct(self):
        self.run_animations()

    def tear_down(self):
        self.play(FadeOut(*self.mobjects))

    def _init_constraints_animations(self):
        constraints_dict = {}
        for index in range(len(self._constraints)):
            constraints_dict[index + 1] = {
                'pre': None,
                'during': self.present_single_problem_constraint(index=index),
                'post': None
            }
        return constraints_dict

    def present_problem_title(self, animation_timings):
        def inner():
            # Fade in title         - 50%
            # Wait                  - 25%
            # Move title to edge up - 25
            fade_in_percentage = 0.25
            wait_percentage = 0.25
            move_up_percentage = 1.0 - fade_in_percentage - wait_percentage
            duration = float(animation_timings['duration'])
            return self._make_successive_animations(
                FadeIn(self._title, run_time=duration * fade_in_percentage),
                Wait(duration * wait_percentage),
                self._title.animate(run_time=duration * move_up_percentage).to_edge(UP)
            )
        return inner

    def present_problem_statement_header(self, animation_timings):
        def inner():
            self._position_element_below_other(self._statement_header, self._title)
            return self._make_successive_animations(
                FadeIn(self._statement_header)
            )
        return inner

    def present_problem_statement(self, animation_timings):
        def inner():
            self._position_element_below_other(self._statement, self._statement_header)
            return self._make_successive_animations(
                FadeIn(self._statement)
            )
        return inner

    def present_problem_constraints_header(self, animation_timings):
        def inner():
            self._position_element_below_other(self._constraints_header, self._statement)
            return self._make_successive_animations(
                FadeIn(self._constraints_header)
            )
        return inner

    def present_single_problem_constraint(self, index):
        def inner():
            self._position_element_below_other(self._constraints, self._constraints_header)
            return self._make_successive_animations(
                FadeIn(self._constraints[index])
            )
        return inner

    def _position_element_below_other(self, element, other):
        element.next_to(other, DOWN)
        element.to_edge(LEFT)