from manim import *
from code_curator.leetcode.problem_text import ProblemText
# import main
from code_curator.leetcode.scenes.present_problem.base_present_problem import BasePresentProblem

from code_curator.data_structures.singly_linked_list import SinglyLinkedList

TITLE = 'Delete Node in a Linked List'
STATEMENT = 'Write a function to delete a node in a singly linked list. You will not be given access to the head of the list, instead you will be given access to the node to be deleted directly.'
CONSTRAINTS = []
CONSTRAINTS.append('The number of nodes in the given list is in the range [2, 1000]')
CONSTRAINTS.append('-1000 $\leq$ Node.val $\leq$ 1000')
CONSTRAINTS.append('The value of each node in the list is unique')
CONSTRAINTS.append('The node to be deleted is in the list and is not a tail node')

class PresentProblem(BasePresentProblem):
    def __init__(self, problem_dir: str, aligned_animation_scene):
        super().__init__(
            title=TITLE,
            statement_header='Statement',
            statement=STATEMENT,
            constraints_header='Constraints',
            constraints=CONSTRAINTS,
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene
        )
