from typing import Any

from .base_sll_animation import BaseSLLAnimation
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from data_structures.singly_linked_list import singly_linked_list
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import linear, smooth, VGroup, Animation, Circle, UP, LEFT, RIGHT, Scene

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class _RemoveAt(BaseSLLAnimation):
    def __init__(
        self,
        sll,
        index:     int,
        node:      SLLNode,
        prev_node_pointer_to_next = None,
        trav_first = None,
        trav_second = None,
        sll_group_to_shift = None,
        mob_anims: dict = None,
        run_time:  int = 1,
        rate_func = linear,
        **kwargs
    ):
        run_time = len(mob_anims)
        print(run_time)
        super().__init__(
            sll,
            index=index,
            node=node,
            run_time=run_time,
            mob_groups=mob_anims,
            rate_func=rate_func,
            **kwargs
        )
        self.group_to_shift = VGroup(*[node for i, node in enumerate(self.sll) if i >= self.index], self.sll.tail_pointer)
        self.prev_node_pointer_to_next = prev_node_pointer_to_next
        self.trav_first = trav_first
        self.trav_second = trav_second
        self.sll_group_to_shift = sll_group_to_shift
        self.container = self.node.container
        self.pointer_to_next = self.node.pointer_to_next

        self.new_sll = singly_linked_list.SinglyLinkedList(*[node.data._value for node in self.sll._nodes])
        self.shift_left_value = self.sll.get_left()[0] - self.new_sll.get_left()[0]
        self.original_prev_removed_node_next_pointer_copy = self.sll._nodes[index - 1].pointer_to_next.copy()

    def begin(self):
        import json
        # print(json.dumps(self.mob_groups, indent=4, default=str))
        self.sll.save_state()
        self.node.save_state()
        self.node.pointer_to_next.save_state()
        self.sll.head_pointer.save_state()
        self._save_state_prev_node_pointer_to_next()
        self.sll_group_to_shift.save_state()
        self.trav_first.save_state()
        self.trav_second.save_state()
        self.group_to_shift.save_state()

        self.final_list_copy = singly_linked_list.SinglyLinkedList(*[node.data._value for node in self.sll])
        self.shift_left_value = self.sll.get_left()[0] - self.final_list_copy.get_left()[0]
        self.final_list_copy.save_state()

        self.distance_to_shift = abs(self.sll[0].get_left() - self.sll[1].get_left())

        self.prev_list_shift_alpha = 0
        # self.distance_up = None
        # self.distance_up = abs(self.node.get_container_top() - self.sll[0].get_container_top())

        self.original_sll_location = self.sll.get_center()
        super().begin()

    def interpolate_mobject(self, alpha: float):
        for animation_num, mob_group in self.mob_groups.items():
            for animation_str, mob_info in mob_group.items():
                normalized_alpha = self._get_normalized_alpha(alpha, animation_num)

                if normalized_alpha <= 0 or normalized_alpha > 1:
                    continue

                mobject = mob_info['mobject']

                if animation_str == 'trav_first_fade_in':
                    self.trav_first.set_opacity(normalized_alpha)
                    if round(normalized_alpha, 3) == 1:
                        self.trav_first.save_state()
                elif animation_str == 'trav_second_fade_in':
                    self.trav_second.set_opacity(normalized_alpha)
                    if round(normalized_alpha, 3) == 1:
                        self.trav_second.save_state()
                elif animation_str == 'trav_first_move':
                    self.trav_first.restore()
                    next_node = mob_info['next_node']
                    self.trav_first.move_immediately_alpha(next_node, next_node, smooth(normalized_alpha))
                    if round(normalized_alpha, 3) == 1:
                        self.trav_first.save_state()
                elif animation_str == 'trav_second_move':
                    self.trav_second.restore()
                    next_node = mob_info['next_node']
                    self.trav_second.move_immediately_alpha(next_node, next_node, smooth(normalized_alpha))
                    if round(normalized_alpha, 3) == 1:
                        self.trav_second.save_state()
                elif animation_str == 'pointer_shrink':
                    self.prev_node_pointer_to_next.restore()
                    diff_width = (
                        abs((self.prev_node_pointer_to_next.get_start_and_end()[1] - self.prev_node_pointer_to_next.get_start_and_end()[0])[0] * (1 - smooth(normalized_alpha)))
                    )
                    width = (self.prev_node_pointer_to_next.get_start_and_end()[1] - self.prev_node_pointer_to_next.get_start_and_end()[0])[0]
                    self.prev_node_pointer_to_next.become(
                        SinglyDirectedEdge(
                            start=self.prev_node_pointer_to_next.get_start_and_end()[0],
                            end=(self.prev_node_pointer_to_next.get_start_and_end()[0] + [self.prev_node_pointer_to_next.tip.length * (smooth(normalized_alpha)), 0, 0]) + [diff_width, 0, 0]
                        )
                    )
                    if round(normalized_alpha, 3) == 1:
                        self.trav_first.node.pointer_to_next.save_state()
                elif animation_str == 'pointer_grow':
                    # NOTE: Seems like there might be a little over extension in the animation?
                    self.prev_node_pointer_to_next.restore()
                    self.prev_node_pointer_to_next.become(
                        SinglyDirectedEdge(
                        start=self.trav_first.node.pointer_to_next.get_start_and_end()[0],
                        end=(
                            self.prev_node_pointer_to_next.get_start_and_end()[1]
                            + (
                                (self.trav_first.node.next.get_container_left() - self.prev_node_pointer_to_next.get_start_and_end()[0]) * [smooth(normalized_alpha), 0, 0]
                            )
                            - [(self.prev_node_pointer_to_next.tip.length * smooth(normalized_alpha)), 0, 0]
                            )
                        )
                    )
                    if round(normalized_alpha, 3) == 1:
                        self.trav_first.node.pointer_to_next.save_state()
                elif animation_str == 'pointer_curve':
                    self.prev_node_pointer_to_next.restore()
                    start = self.prev_node_pointer_to_next.get_start_and_end()[0]
                    end = self.prev_node_pointer_to_next.get_start_and_end()[1] + ((self.trav_second.node.get_container_left() - self.prev_node_pointer_to_next.get_start_and_end()[1]) * [smooth(normalized_alpha), 0, 0])

                    self.prev_node_pointer_to_next.become(
                        SinglyDirectedEdge.create_curved_pointer(
                        start=start,
                        end=end,
                        angle=(smooth(normalized_alpha) * (1.25 + self.trav_first.node.radius))
                        )
                    )
                    if round(normalized_alpha, 3) == 1:
                        self.trav_first.node.pointer_to_next.save_state()
                elif animation_str == 'container_fade_out':
                    self.container.set_stroke(opacity=1 - smooth(normalized_alpha))
                    for sub in self.container.submobjects:
                        sub.set_opacity(1 - smooth(normalized_alpha))
                elif animation_str == 'pointer_fade_out':
                    self.pointer_to_next.set_opacity(1 - smooth(normalized_alpha))
                elif animation_str == 'center_list':
                    d_alpha = smooth(normalized_alpha) - smooth(self.prev_list_shift_alpha)
                    self.prev_list_shift_alpha = normalized_alpha
                    self.sll.shift(LEFT * self.shift_left_value * d_alpha)
                elif animation_str == 'shift_sub_list':
                    # d_alpha = smooth(normalized_alpha) - smooth(self.prev_list_shift_alpha)
                    # self.prev_list_shift_alpha = normalized_alpha
                    # self.sll.shift(LEFT * self.shift_left_value * d_alpha)

                    # if self._get_mob_animation_num('shift_sub_list') == self._get_mob_animation_num('center_list'):
                    final_start = self.original_prev_removed_node_next_pointer_copy.get_start_and_end()[0]
                    final_end = self.original_prev_removed_node_next_pointer_copy.get_start_and_end()[1] + (LEFT * self.shift_left_value * smooth(normalized_alpha))

                    if self._get_mob_animation_num('shift_sub_list') != self._get_mob_animation_num('center_list'):
                        self.final_list_copy.restore()
                        self.group_to_shift.restore()
                        point_to_shift_to = self.final_list_copy[self.index - 1].get_container_right()
                        self.group_to_shift.shift(LEFT * (self.group_to_shift[0].get_left() - point_to_shift_to) * smooth(normalized_alpha))
                        # self.group_to_shift.shift(LEFT * (self.node.radius + self.node.pointer_to_next.length) * smooth(normalized_alpha))
                        # self.group_to_shift.shift(LEFT * abs(self.final_list_copy[self.index - 1].pointer_to_next.get_start_and_end()[1] - self.trav_second.node.get_container_left()) * smooth(normalized_alpha))
                        end = self.group_to_shift[0].get_container_left()

                        if round(normalized_alpha, 3) == 1:
                            self.prev_node_pointer_to_next.become(
                                SinglyDirectedEdge(
                                    start=self.sll[self.index - 1].get_container_right(),
                                    end=self.group_to_shift[0].get_container_left()
                                )
                            )
                        # self.final_list_copy.shift(LEFT * self.shift_left_value)
                        # end = self.final_list_copy[self.index - 2].pointer_to_next.get_start_and_end()[1]
                    elif self._get_mob_animation_num('shift_sub_list') == self._get_mob_animation_num('center_list'):

                        self.group_to_shift.restore()
                        self.group_to_shift.shift(LEFT * abs(final_end - self.trav_second.node.get_container_left()) * smooth(normalized_alpha))

                        end = self.group_to_shift[0].get_container_left()

                        if round(normalized_alpha, 3) == 1:
                            self.prev_node_pointer_to_next.become(
                                SinglyDirectedEdge(
                                    start=final_start + (LEFT * self.shift_left_value * 1),
                                    end=final_end
                                )
                            )

                    self.prev_node_pointer_to_next.become(
                        SinglyDirectedEdge.create_curved_pointer(
                            # start=final_start + (LEFT * self.shift_left_value * smooth(normalized_alpha)),
                            start=self.sll[self.index - 1].get_container_right(),
                            end=end,
                            angle=(1 - smooth(normalized_alpha)) * (1.25 + self.trav_second.node.radius)
                        )
                    )


                    self.trav_first.fade(normalized_alpha)
                    self.trav_second.fade(normalized_alpha)

    def clean_up_from_scene(self, scene: Scene = None) -> None:
        scene.add(self.node)
        self.node.remove(self.sll)
        scene.remove(self.trav_first)
        scene.remove(self.trav_second)
        # scene.remove(self.trav)

        super().clean_up_from_scene(scene)

    def _save_state_prev_node_pointer_to_next(self):
        if self.prev_node_pointer_to_next is not None:
            self.prev_node_pointer_to_next.save_state()

    def _restore_prev_node_pointer_to_next(self):
        if self.prev_node_pointer_to_next is not None:
            self.prev_node_pointer_to_next.restore()


class RemoveAt:
    def __init__(self, sll):
        self._sll = sll
        self._index = None
        self._prev_node_pointer_to_next = None
        self._removed_node = None
        self._sll_group_to_shift = None
        self._trav_first = None
        self._trav_second = None
        self._anim_pre_reqs = self._get_mob_anim_template()
        self._mob_anims = {}

    def _add_node_and_animate(fn):
        def inner(self, *args, **kwargs):
            self._index, self._removed_node = self._remove_node(*args, **kwargs)
            self._prev_node_pointer_to_next = self._sll[self._index - 1].pointer_to_next
            self._sll_group_to_shift = VGroup(*[node for i, node in enumerate(self._sll) if i > self._index], self._sll.tail_pointer)
            fn(self, *args, **kwargs)
            self._set_trav_conditions(**kwargs)
            return self._account_for_dependencies()
        return inner
    
    def _get_mob_anim_template(self):
        return {
                'trav_names': [],
                'trav_placement': {
                    'start': True,
                    'end': False
                }
            }
    
    def _account_for_dependencies(self) -> Animation:
        TRAV_NAMES = self._anim_pre_reqs['trav_names']
        DISPLAY_TRAV = len(TRAV_NAMES) > 0

        if not DISPLAY_TRAV:
            self._trav_first = Circle().fade(1)
            self._trav_second = Circle().fade(1)
            return self._create_animation()
        
        trav_start_list = [position_str for position_str, is_placed in self._anim_pre_reqs['trav_placement'].items() if is_placed]
        if len(trav_start_list) > 1:
            raise RuntimeError('When animating singly linked list insertion, trav may only have one start position.')
        TRAV_PLACEMENT = trav_start_list[0]

        trav_first_node = self._sll[0] if TRAV_PLACEMENT == 'start' else self._sll[self._index - 1]
        trav_second_node = self._sll[1] if TRAV_PLACEMENT == 'start' else self._sll[self._index + 1]
        self._trav_first = Pointer(
            node=trav_first_node,
            sll=self._sll,
            label=TRAV_NAMES[0],
            direction=UP
        )
        self._trav_second = Pointer(
            node=trav_second_node,
            sll=self._sll,
            label=TRAV_NAMES[1],
            direction=UP
        )

        self._trav_first.set_opacity(0)
        self._sll.add(self._trav_first)
        self._trav_second.set_opacity(0)
        self._sll.add(self._trav_second)

        animation_num = 1
        beginning_trav_animations = {
            animation_num: {
                'trav_first_fade_in': {'mobject': self._trav_first},
                'trav_second_fade_in': {'mobject': self._trav_second}
            }
        }

        animation_num += 1

        # If trav will be starting at its last position, we just need to fade it in
        if TRAV_PLACEMENT == 'start':
            for node_index in range(self._index - 2):
                beginning_trav_animations[animation_num] = {
                    'trav_first_move': {
                        'mobject': self._trav_first,
                        'curr_node': self._sll[node_index],
                        'next_node': self._sll[node_index + 1]
                    }
                }
                beginning_trav_animations[animation_num]['trav_second_move'] = {
                    'mobject': self._trav_first,
                    'curr_node': self._sll[node_index + 1],
                    'next_node': self._sll[node_index + 2]
                }
                animation_num += 1

            beginning_trav_animations[animation_num] = {
                    'trav_first_move': {
                        'mobject': self._trav_first,
                        'curr_node': self._sll[self._index - 2],
                        'next_node': self._sll[self._index - 1]
                    }
                }
            beginning_trav_animations[animation_num]['trav_second_move'] = {
                'mobject': self._trav_first,
                'curr_node': self._sll[self._index - 1],
                'next_node': self._removed_node
            }
            animation_num += 1

        if len(TRAV_NAMES) == 2:
            beginning_trav_animations[animation_num] = {
                'trav_second_move': {
                    'mobject': self._trav_second,
                    'curr_node': self._removed_node,
                    'next_node': self._sll[self._index]
                }
            }
            animation_num += 1

        updated_mob_anims = beginning_trav_animations

        for mob_group in self._mob_anims.values():
            updated_mob_anims[animation_num] = mob_group
            animation_num += 1

        self._mob_anims = updated_mob_anims

        return self._create_animation()
    
    def _remove_node(self, index: int, *args, **kwargs) -> None:
        removed_node = self._sll._nodes[index]
        self._prev_node_pointer_to_next = self._sll._nodes[-2].pointer_to_next
        del self._sll._nodes[index]

        return index, removed_node
    
    def _create_animation(self):
        if self._removed_node is None or self._mob_anims is None:
            raise RuntimeError('Make node or mob_anims has not been set yet!')
        
        animation = _RemoveAt(
            sll=self._sll,
            index=self._index,
            node=self._removed_node,
            prev_node_pointer_to_next=self._prev_node_pointer_to_next,
            trav_first=self._trav_first,
            trav_second=self._trav_second,
            sll_group_to_shift=self._sll_group_to_shift,
            mob_anims=self._mob_anims
        )

        # self._mob_anims = self._get_mob_anim_template()
        self._mob_anims = {}

        return animation

    def _set_trav_names(self, names: list[str]) -> None:
        self._anim_pre_reqs['trav_names'] = names
    
    # def _set_trav_display(self, is_displayed: bool) -> None:
    #     self._anim_pre_reqs['display_trav'] = is_displayed

    def _set_trav_position(self, position: str) -> None:
        other_position = 'end' if position == 'start' else 'start'
        self._anim_pre_reqs['trav_placement'][position] = True
        self._anim_pre_reqs['trav_placement'][other_position] = False

    # def _set_aligned(self, aligned: bool) -> None:
    #     self._anim_pre_reqs['aligned'] = aligned

    def _remove_mob_anim(self, anim_name: str) -> None:
        animation_num_removed_from = None
        for animation_num, info in self._mob_anims.items():
            if anim_name in info:
                del self._mob_anims[animation_num][anim_name]
                animation_num_removed_from = animation_num

        if len(self._mob_anims[animation_num_removed_from]) == 0:
            del self._mob_anims[animation_num_removed_from]

            for new_animation_num in range(animation_num_removed_from, len(self._mob_anims) + 1):
                self._mob_anims[new_animation_num] = self._mob_anims.pop(new_animation_num + 1)

    def _remove_container_fade_in(self) -> None:
        self._remove_mob_anim('container_fade_in')

    def _remove_pointer_to_next_fade_in(self) -> None:
        self._remove_mob_anim('pointer_to_next_fade_in')

    def _remove_prev_node_pointer_to_next_move(self) -> None:
        self._remove_mob_anim('prev_node_pointer_to_next_move')

    def _remove_flatten(self) -> None:
        self._remove_mob_anim('flatten')

    def _remove_shift_sub_list(self) -> None:
        self._remove_mob_anim('shift_sub_list')

    def _add_to_mob_anims(self, group_num: int, key: str, value: dict) -> None:
        if group_num is None:
            group_num = len(self._mob_anims) + 1
        elif group_num == -1:
            group_num = len(self._mob_anims)
        
        if group_num not in self._mob_anims:
            self._mob_anims[group_num] = {key: value}
        else:
            self._mob_anims[group_num][key] = value

    def _clear_mob_anims(self):
        self._mob_anims = {}

    def _add_pointer_shrink(self, group_num: int = None) -> None:
        key = 'pointer_shrink'
        value = {'mobject': self._prev_node_pointer_to_next}
        self._add_to_mob_anims(group_num, key, value)

    def _add_pointer_grow(self, group_num: int = None) -> None:
        key = 'pointer_grow'
        value = {'mobject': self._prev_node_pointer_to_next}
        self._add_to_mob_anims(group_num, key, value)

    def _add_pointer_curve(self, group_num: int = None) -> None:
        key = 'pointer_curve'
        value = {'mobject': self._prev_node_pointer_to_next}
        self._add_to_mob_anims(group_num, key, value)

    def _add_pointer_move(self, group_num: int = None) -> None:
        key = 'pointer_move'
        value = {'mobject': self._prev_node_pointer_to_next}
        self._add_to_mob_anims(group_num, key, value)
    
    def _add_container_fade_out(self, group_num: int = None) -> None:
        key = 'container_fade_out'
        value = {'mobject': self._removed_node.container}
        self._add_to_mob_anims(group_num, key, value)

    def _add_pointer_fade_out(self, group_num: int = None) -> None:
        key = 'pointer_fade_out'
        value = {'mobject': self._removed_node.pointer_to_next}
        self._add_to_mob_anims(group_num, key, value)

    # def _add_prev_node_pointer_to_next_move(self, group_num: int = None) -> None:
    #     key = 'prev_node_pointer_to_next_move'
    #     value = {'mobject': self._prev_node_pointer_to_next}
    #     self._add_to_mob_anims(group_num, key, value)

    # def _add_flatten(self, group_num: int = None) -> None:
    #     key = 'flatten'
    #     value = {'mobject': self._sll_group_to_shift}
    #     self._add_to_mob_anims(group_num, key, value)

    def _add_shift_sub_list(self, group_num: int = None) -> None:
        key = 'shift_sub_list'
        value = {'mobject': self._sll_group_to_shift}
        self._add_to_mob_anims(group_num, key, value)

    def _add_center_list(self, group_num: int = None) -> None:
        key = 'center_list'
        value = {'mobject': self._sll}
        self._add_to_mob_anims(group_num, key, value)

    # def _set_add_to_front(self, add_to_front: bool) -> None:
    #     self._anim_pre_reqs['add_to_front'] = add_to_front
    #     self._anim_pre_reqs['add_to_back'] = not add_to_front

    # def _set_add_to_back(self, add_to_back: bool) -> None:
    #     self._anim_pre_reqs['add_to_back'] = add_to_back
    #     self._anim_pre_reqs['add_to_front'] = not add_to_back

    def _set_trav_conditions(self, *, index: int, trav_names: list[str], trav_position: str, **kwargs) -> None:
        self._set_trav_names(trav_names)
        self._set_trav_position(trav_position)
        # self._set_aligned(aligned)
        # if index == 0:
        #     self._set_add_to_front(True)
        # if (aligned and (index == 0 or index == len(self._sll))) \
        # or not aligned:
        #     self._set_trav_display(trav_displayed)
        #     self._set_trav_position(trav_position)

        #     if index == 0:
        #         self._remove_prev_node_pointer_to_next_move()
        # else:
        #     self._set_trav_display(False)

        #     # TODO: Temporary fix for aligned insertion not at front or end
        #     ###############################################################
        #     self._inserted_node.remove(self._inserted_node.pointer_to_next)
        #     self._inserted_node.set_next(self._sll[self._index + 2])
        #     self._inserted_node.next = self._sll[self._index]
        #     for submobject in self._inserted_node.submobjects:
        #         submobject.set_opacity(0)
        #     ###############################################################

        #     self._clear_mob_anims()
        #     self._add_container_fade_in()
        #     self._add_pointer_to_next_fade_in(-1)
        #     self._add_shift_sub_list(-1)

    @_add_node_and_animate
    def one_by_one(
        self,
        *,
        index: int,
        end_index: int,
        trav_names: list = None,
        pointer_fade_is_first: bool = False,
        trav_position: str = 'start',
        pointer_movement: str = 'specific'
    ) -> Animation:
        self._add_pointer_shrink()
        self._add_pointer_grow()
        self._add_pointer_curve()
        # self._add_pointer_move()
        self._add_container_fade_out()
        self._add_pointer_fade_out()
        self._add_shift_sub_list()
        self._add_center_list(-1)

    @_add_node_and_animate
    def show_node_and_pointer_together(
        self,
        *,
        index: int,
        data: Any,
        aligned: bool,
        trav_displayed: bool,
        trav_position: str = 'start',
    ) -> Animation:
        self._add_container_fade_in()
        self._add_pointer_to_next_fade_in(-1)

        self._add_prev_node_pointer_to_next_move()
        self._add_flatten()

    @_add_node_and_animate
    def show_node_and_pointer_prev_pointer_together(
        self,
        *,
        index: int,
        data: Any,
        aligned: bool,
        trav_displayed: bool,
        trav_position: str = 'start',
    ):
        self._add_container_fade_in()
        self._add_pointer_to_next_fade_in(-1)
        self._add_prev_node_pointer_to_next_move(-1)

        self._add_flatten()

    @_add_node_and_animate
    def show_node_and_pointer_prev_pointer_and_flatten_together(
        self,
        *,
        index: int,
        data: Any,
        aligned: bool,
        trav_displayed: bool,
        trav_position: str = 'start',
    ):
        self._add_container_fade_in()
        self._add_pointer_to_next_fade_in(-1)
        self._add_prev_node_pointer_to_next_move(-1)
        self._add_flatten(-1)

    @_add_node_and_animate
    def all_together(
        self,
        *,
        index: int,
        end_index: int,
        aligned: bool = True,
        trav_displayed: bool = False,
        trav_position: str = 'start'
    ):
        self._add_container_fade_in()
        self._add_pointer_to_next_fade_in(-1)
        self._add_shift_sub_list(-1)