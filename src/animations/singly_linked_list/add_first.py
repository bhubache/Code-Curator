from typing import Any

# from data_structures.singly_linked_list.singly_linked_list import SinglyLinkedList
from animations.singly_linked_list.base_sll_animation import BaseSLLAnimation
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import LEFT, Animation, linear, smooth, Scene

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# TODO: Allow specifying the time that each animation should take within this class animation
#       alpha should be scaled accordingly
# TODO: Create unaligned addfirst
# TODO: Create generic adding node animation (not just to front)


class _AddToFront(Animation):
    '''
    Private class for animating adding to the front of a linked list.

    This class is intended to be able to handle various ways of animating
    the addition of a node to the front of a singly linked list. It can
    vary by:
        - Number of subanimations
        - Grouping of subanimations
        - Order of subanimations
        - Runtime
        - Rate function
        - How certain mobjects are made to appear on the screen
            * Fading in
            * Creation
            * etc...

    Attributes:
        sll: SinglyLinkedList
            The linked list to which the node will be added.
        node: SLLNode
            The node that will be added.
        mob_groups: dict
            A dictionary that contains the mobjects ordered
            and grouped in the way that they will be animated.

            Example:
            {
                "1": {
                    "container": "Circle"
                },
                "2": {
                    "pointer_to_next": "SinglyDirectedEdge",
                    "head_pointer": "Pointer",
                    "sll": "SinglyLinkedList"
                }
            }

            This dictionary states that there will be two animations
            where the first animation fades in the node container and
            the second animation fades in the nodes' next pointer, moves
            the head trav, and centers the linked list.
        run_time: int
            How long the animation will run for.
        rate_func: function
            Maps the animation progression [0, 1] to some function.

            Example:
                linear simply maps the animation progression 1:1.
                So, if the animation were 37% complete, the linear
                function outputs 0.37.
        num_animations: int
            The number of subanimations that make up this animation.
        alpha_thresholds: dict
            A mapping of a animation number to the animation progression
            (alpha) at which point the subanimation will be complete.

            Example:
            {
                "1": 0.25,
                "2": 0.5,
                "3": 0.75,
                "4": 1.0
            }
            This dictionary states that subanimation 1 will be finished
            at the animation progression (alpha) value of 0.25, and
            subanimation 2 will be finished at alpha 0.5 etc...
        alpha_step_size: float
            The amount of animation progress that each subanimation gets.

    Methods:
        begin:
            Performs setup for the animation.
        interpolate_mobject:
            Logic for the progression of the animation.
        clean_up_from_scene:
            Adding and removing of mobjects from scene.
    '''
    def __init__(
        self,
        sll,
        node:      SLLNode,
        mob_anims: dict,
        run_time:  int = 1,
        rate_func = linear,
        **kwargs
    ):
        run_time = len(mob_anims)
        super().__init__(
            sll,
            run_time=run_time,
            rate_func=rate_func,
            **kwargs
        )
        self.sll = sll
        self.node = node
        self.mob_groups = mob_anims
        self.num_animations = len(self.mob_groups)
        self.alpha_thresholds = {num: num / self.num_animations for num in self.mob_groups}
        self.alpha_step_size = 1 / self.num_animations
        
    def begin(self) -> None:
        self.sll.save_state()
        self.node._pointer_to_next.save_state()
        self.sll.head_pointer.save_state()

        self.original_sll_location = self.sll.get_center()

        self.node.container.set_opacity(0)
        self.node.pointer_to_next.set_opacity(0)
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        for animation_num, mob_group in self.mob_groups.items():
            for mob_name, mob in mob_group.items():
                normalized_alpha = self._get_normalized_alpha(alpha, animation_num)

                if normalized_alpha <= 0 or normalized_alpha >= 1:
                    continue

                if mob_name == 'container':
                    mob.set_stroke(opacity=normalized_alpha)
                    for container_sub in mob.submobjects:
                        container_sub.set_opacity(normalized_alpha)
                elif mob_name == 'pointer_to_next':
                    if self._get_mob_animation_num('pointer_to_next') == self._get_mob_animation_num('sll'):
                        curr_start, curr_end = mob.get_start_and_end()
                        mob.become(SinglyDirectedEdge(start=curr_start, end=curr_end))
                    else:
                        mob.restore()
                        original_start, original_end = mob.get_start_and_end()
                        new_end = [mob.tip.length, 0, 0] + original_start + ((original_end - original_start - [mob.tip.length, 0, 0]) * [smooth(normalized_alpha), 1, 1])
                        mob.become(SinglyDirectedEdge(start=original_start, end=new_end))
                    mob.set_opacity(normalized_alpha)
                elif mob_name == 'head_pointer':
                    mob.restore()
                    mob.move_immediately_alpha(self.node, self.node, smooth(normalized_alpha))
                elif mob_name == 'sll':
                    mob.move_to([self.original_sll_location[0] - (self.original_sll_location[0] * smooth(normalized_alpha)), 0, 0])

    def clean_up_from_scene(self, scene: Scene = None) -> None:
        scene.add(self.node)
        self.node.remove(self.sll)
        super().clean_up_from_scene(scene)

    def _get_normalized_alpha(self, alpha: float, animation_num: int) -> float:
        start_alpha = self.alpha_thresholds[animation_num] - self.alpha_step_size
        end_alpha = start_alpha + self.alpha_step_size

        if alpha < start_alpha:
            return 0
        elif start_alpha <= alpha <= end_alpha:
            alpha = (alpha - (self.alpha_step_size * (animation_num - 1))) / self.alpha_step_size
            if alpha > 1:
                alpha = 1
            return alpha
        elif alpha > end_alpha:
            return 1
        else:
            raise Exception(f'Animation number {animation_num} has alpha {alpha}')
        
    def _get_mob_animation_num(self, mob_name: str) -> int:
        for animation_num, mob_group in self.mob_groups.items():
            if mob_name in mob_group:
                return animation_num
        raise


class AddFirst:
    '''
    Handles the internal manipulation and animation of adding a node to the front of a linked list.

    Attributes:
        sll: SinglyLinkedList
            The linked list to which the node will be added.
        node: SLLNode
            The node that will be added.
        mob_anims: dict
            See `mob_groups` in _AddToFront.

    Methods:
        all_together:
            1. Perform all subanimations at once.
        node_then_everything_else:
            1. Animate the node.
            2. Animate everything else.
        node_and_pointer_then_everything_else:
            1. Animate the node and pointer.
            2. Animate everything else.
        node_and_pointer_and_trav_then_center
            1. Animate the node, pointer, and trav.
            2. Animate everything else.
        node_then_pointer_then_trav_and_center
            1. Animate the node.
            2. Animate the pointer.
            3. Animate everything else.
        node_and_pointer_then_trav_then_center:
            1. Animate the node and pointer.
            2. Animate the head trav.
            3. Animate the linked list centering.
        node_then_pointer_and_trav_then_center:
            1. Animate the node.
            2. Animate the pointer and trav.
            3. Animate the linked list centering.
        node_then_pointer_then_trav_then_center
            1. Animate the node.
            2. Animate the pointer.
            3. Animate the trav.
            4. Animate the linked list centering.
    '''
    def __init__(self, sll):
        self._sll = sll
        self._node = None
        self._mob_anims = None

    def _add_node_and_animate(fn):
        def inner(self, *args, **kwargs):
            self._node = self._add_node(*args, **kwargs)
            fn(self, *args, **kwargs)
            return self._create_animation()
        return inner

    #################
    # One animation #
    #################
    @_add_node_and_animate
    def all_together(self, data: Any) -> Animation:
        self._mob_anims = {
            1: {
                'container': self._node._container,
                'pointer_to_next': self._node._pointer_to_next,
                'head_pointer': self._sll.head_pointer,
                'sll': self._sll
            }
        }
    
    ##################
    # Two animations #
    ##################
    @_add_node_and_animate
    def node_then_everything_else(self, data: Any) -> Animation:
        self._mob_anims = {
            1: {
                'container': self._node._container,
            },
            2: {
                'pointer_to_next': self._node._pointer_to_next,
                'head_pointer': self._sll.head_pointer,
                'sll': self._sll
            }
        }

    @_add_node_and_animate
    def node_and_pointer_then_everything_else(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container,
                'pointer_to_next': self._node._pointer_to_next,
            },
            2: {
                'head_pointer': self._sll.head_pointer,
                'sll': self._sll
            }
        }

    @_add_node_and_animate
    def node_and_pointer_and_trav_then_center(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container,
                'pointer_to_next': self._node._pointer_to_next,
                'head_pointer': self._sll.head_pointer
            },
            2: {
                'sll': self._sll
            }
        }

    ####################
    # Three animations #
    ####################
    @_add_node_and_animate
    def node_then_pointer_then_trav_and_center(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container,
            },
            2: {
                'pointer_to_next': self._node._pointer_to_next
            },
            3: {
                'head_pointer': self._sll.head_pointer,
                'sll': self._sll
            }
        }

    @_add_node_and_animate
    def node_and_pointer_then_trav_then_center(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container,
                'pointer_to_next': self._node._pointer_to_next
            },
            2: {
                'head_pointer': self._sll.head_pointer
            },
            3: {
                'sll': self._sll
            }
        }

    @_add_node_and_animate
    def node_then_pointer_and_trav_then_center(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container
            },
            2: {
                'pointer_to_next': self._node._pointer_to_next,
                'head_pointer': self._sll.head_pointer
            },
            3: {
                'sll': self._sll
            }
        }

    ###################
    # Four animations #
    ###################
    @_add_node_and_animate
    def node_then_pointer_then_trav_then_center(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container
            },
            2: {
                'pointer_to_next': self._node._pointer_to_next
            },
            3: {
                'head_pointer': self._sll.head_pointer
            },
            4: {
                'sll': self._sll
            }
        }
    
    def _add_node(self, data: Any) -> None:
        node = SLLNode(data)
        node.next_to(self._sll._head, LEFT, buff=1)
        node.set_next(self._sll._nodes[0])

        node.add(node._pointer_to_next)
        node.add(node._container)

        self._sll._nodes.insert(0, node)
        self._sll.add(node)

        self._sll._head = node
        return node
    
    def _create_animation(self):
        if self._node is None or self._mob_anims is None:
            raise RuntimeError('Make node or mob_anims has not been set yet!')
        
        return _AddToFront(
            sll=self._sll,
            node=self._node,
            mob_anims=self._mob_anims
        )
