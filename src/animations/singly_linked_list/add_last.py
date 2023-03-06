from typing import Any

# from data_structures.singly_linked_list.singly_linked_list import SinglyLinkedList
from animations.singly_linked_list.base_sll_animation import BaseSLLAnimation
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import RIGHT, Animation, linear, smooth, Scene

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class _AddToBack(Animation):
    def __init__(
        self,
        sll,
        node:      SLLNode,
        prev_node_pointer_to_next,
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
        self.prev_node_pointer_to_next = prev_node_pointer_to_next
        print(self.prev_node_pointer_to_next)
        self.mob_groups = mob_anims
        self.num_animations = len(self.mob_groups)
        self.alpha_thresholds = {num: num / self.num_animations for num in self.mob_groups}
        self.alpha_step_size = 1 / self.num_animations
        
    def begin(self) -> None:
        self.sll.save_state()
        self.prev_node_pointer_to_next.save_state()
        self.sll.tail_pointer.save_state()

        self.original_sll_location = self.sll.get_center()

        self.node.container.set_opacity(0)
        self.prev_node_pointer_to_next.set_opacity(0)
        # self.node.pointer_to_next.set_opacity(0)
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
                elif mob_name == 'prev_node_pointer_to_next':
                    if self._get_mob_animation_num('prev_node_pointer_to_next') == self._get_mob_animation_num('sll'):
                        curr_start, curr_end = mob.get_start_and_end()
                        mob.become(SinglyDirectedEdge(start=curr_start, end=curr_end))
                    else:
                        mob.restore()
                        original_start, original_end = mob.get_start_and_end()
                        new_end = [mob.tip.length, 0, 0] + original_start + ((original_end - original_start - [mob.tip.length, 0, 0]) * [smooth(normalized_alpha), 1, 1])
                        mob.become(SinglyDirectedEdge(start=original_start, end=new_end))
                    mob.set_opacity(normalized_alpha)
                elif mob_name == 'tail_pointer':
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


class AddLast:
    def __init__(self, sll):
        self._sll = sll
        self._node = None
        self._prev_node_pointer_to_next = None
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
                'container': self._node.container,
                'prev_node_pointer_to_next': self._sll._nodes[-2].pointer_to_next,
                'tail_pointer': self._sll.tail_pointer,
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
                'container': self._node._container
            },
            2: {
                'prev_node_pointer_to_next': self._sll._nodes[-2].pointer_to_next,
                'tail_pointer': self._sll.tail_pointer,
                'sll': self._sll
            }
        }

    @_add_node_and_animate
    def node_and_pointer_then_everything_else(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container,
                'prev_node_pointer_to_next': self._sll._nodes[-2].pointer_to_next,
            },
            2: {
                'tail_pointer': self._sll.tail_pointer,
                'sll': self._sll
            }
        }

    @_add_node_and_animate
    def node_and_pointer_and_trav_then_center(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container,
                'prev_node_pointer_to_next': self._sll._nodes[-2].pointer_to_next,
                'tail_pointer': self._sll.tail_pointer
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
                'prev_node_pointer_to_next': self._sll._nodes[-2].pointer_to_next,
            },
            3: {
                'tail_pointer': self._sll.tail_pointer,
                'sll': self._sll
            }
        }

    @_add_node_and_animate
    def node_and_pointer_then_trav_then_center(self, data: Any):
        self._mob_anims = {
            1: {
                'container': self._node._container,
                'prev_node_pointer_to_next': self._sll._nodes[-2].pointer_to_next,
            },
            2: {
                'tail_pointer': self._sll.tail_pointer,
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
                'prev_node_pointer_to_next': self._sll._nodes[-2].pointer_to_next,
                'tail_pointer': self._sll.tail_pointer,
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
                'prev_node_pointer_to_next': self._sll._nodes[-2].pointer_to_next,
            },
            3: {
                'tail_pointer': self._sll.tail_pointer,
            },
            4: {
                'sll': self._sll
            }
        }

    def _add_node(self, data: Any) -> None:
        node = SLLNode(data)
        node.next_to(self._sll._tail, RIGHT, buff=1)
        self._sll._tail.set_next(node)

        # node.add(self._sll._tail._pointer_to_next)
        self._prev_node_pointer_to_next = self._sll._tail.pointer_to_next
        self._sll._tail.add(self._prev_node_pointer_to_next)
        node.add(node._container)

        self._sll._nodes.append(node)
        self._sll.add(node)

        self._sll._tail = node
        return node
    
    def _create_animation(self):
        if self._node is None or self._mob_anims is None:
            raise RuntimeError('Make node or mob_anims has not been set yet!')
        
        return _AddToBack(
            sll=self._sll,
            node=self._node,
            prev_node_pointer_to_next=self._prev_node_pointer_to_next,
            mob_anims=self._mob_anims
        )