from .base_sll_animation import BaseSLLAnimation
from data_structures.nodes.singly_linked_list_node import SLLNode
from manim import linear, smooth, VGroup

class _Insert(BaseSLLAnimation):
    def __init__(
        self,
        sll,
        index:     int,
        node:      SLLNode,
        prev_node_pointer_to_next = None,
        trav = None,
        sll_group_to_shift = None,
        mob_anims: dict = None,
        run_time:  int = 1,
        rate_func = linear,
        **kwargs
    ):
        run_time = len(mob_anims)
        super().__init__(
            sll,
            index=index,
            node=node,
            run_time=run_time,
            mob_groups=mob_anims,
            rate_func=rate_func,
            **kwargs
        )
        self.prev_node_pointer_to_next = prev_node_pointer_to_next
        self.trav = trav
        self.sll_group_to_shift = sll_group_to_shift
        self.container = self.node.container
        self.pointer_to_next = self.node.pointer_to_next

    def begin(self):
        self.sll.save_state()
        self.node.save_state()
        self.node.pointer_to_next.save_state()
        self.sll.head_pointer.save_state()
        self._save_state_prev_node_pointer_to_next()
        self.sll_group_to_shift.save_state()
        self.trav.save_state()

        self.final_list_copy = singly_linked_list.SinglyLinkedList(*[node.data._value for node in self.sll])
        self.shift_left_value = self.sll.get_left()[0] - self.final_list_copy.get_left()[0]

        self.distance_to_shift = abs(self.sll[0].get_left() - self.sll[1].get_left())
        self.distance_up = None
        if self.index == 0:
            self.distance_up = abs(self.node.get_container_top() - self.sll[1].get_container_top())
        else:
            self.distance_up = abs(self.node.get_container_top() - self.sll[0].get_container_top())

        self.original_sll_location = self.sll.get_center()

        self.node.container.set_opacity(0)
        self.node.pointer_to_next.set_opacity(0)
        super().begin()

    def interpolate_mobject(self, alpha: float):
        for animation_num, mob_group in self.mob_groups.items():
            for animation_str, mob_info in mob_group.items():
                normalized_alpha = self._get_normalized_alpha(alpha, animation_num)

                if normalized_alpha <= 0 or normalized_alpha > 1:
                    continue

                mobject = mob_info['mobject']

                if animation_str == 'trav_fade_in':
                    self.trav.set_opacity(normalized_alpha)
                    if round(normalized_alpha, 3) == 1:
                        self.trav.save_state()
                    # self.trav.save_state()
                elif animation_str == 'trave_fade_out':
                    self.trav.set_opacity(1 - normalized_alpha)
                elif animation_str == 'trav_move':
                    self.trav.restore()
                    next_node = mob_info['next_node']
                    self.trav.move_immediately_alpha(next_node, next_node, smooth(normalized_alpha))
                    if round(normalized_alpha, 3) == 1:
                        self.trav.save_state()
                elif animation_str == 'container_fade_in':
                    self.container.set_stroke(opacity=normalized_alpha)
                    for container_sub in self.container.submobjects:
                        container_sub.set_opacity(normalized_alpha)
                elif animation_str == 'pointer_to_next_fade_in':
                    self.pointer_to_next.set_opacity(normalized_alpha)
                elif animation_str == 'prev_node_pointer_to_next_move':
                    self.prev_node_pointer_to_next.restore()
                    original_start, original_end = self.prev_node_pointer_to_next.get_start_and_end()
                    final_end = original_end + ((self.node.get_container_left() - original_end) * smooth(normalized_alpha))
                    self.prev_node_pointer_to_next.become(
                        SinglyDirectedEdge(
                            start=original_start,
                            end=final_end
                        )
                    )
                elif animation_str == 'shift_sub_list':
                    self.sll.restore()
                    self.node.restore()
                    self.sll_group_to_shift.restore()
                    self.sll.shift(LEFT * self.shift_left_value * smooth(alpha))
                    self.sll_group_to_shift.shift(RIGHT * self.distance_to_shift * smooth(alpha))
                elif animation_str == 'flatten':
                    self.sll.restore()
                    self.node.restore()
                    self.sll_group_to_shift.restore()
                    self.trav.restore()
                    
                    def flatten_list(self, alpha):
                        # self.sll.restore()
                        if self.index == 0:
                            self.sll.shift(RIGHT * self.shift_left_value * smooth(alpha))
                        else:
                            self.sll.shift(LEFT * self.shift_left_value * smooth(alpha))

                        # self.node.restore()
                        if self.index == 0:
                            self.node.shift(LEFT * self.shift_left_value * smooth(alpha) * 2)
                        self.node.shift(UP * self.distance_up * smooth(alpha))

                        # self.sll_group_to_shift.restore()
                        # self.sll_group_to_shift.shift(LEFT * self.shift_left_value * smooth(alpha))
                        self.sll_group_to_shift.shift(RIGHT * self.distance_to_shift * smooth(alpha))

                        if self.prev_node_pointer_to_next is not None:
                            self.prev_node_pointer_to_next.become(SinglyDirectedEdge(start=self.sll[self.index - 1].get_container_right(), end=self.sll[self.index].get_container_left()))

                        self.trav.set_opacity(1 - alpha)

                        def rotate_start():
                            start, _ = self.node.pointer_to_next.get_start_and_end()
                            curr_x = start[0]
                            curr_y = start[1]

                            origin_x, origin_y, _ = self.node.get_container_center()
                            angle = -(math.pi / 2 * smooth(alpha))
                            sine = math.sin(angle)
                            cosine = math.cos(angle)

                            new_x = origin_x + cosine * (curr_x - origin_x) - sine * (curr_y - origin_y)
                            new_y = origin_y - sine * (curr_x - origin_x) + cosine * (curr_y - origin_y)
                            return [new_x, new_y, 0]

                        def rotate_end():
                            # FIXME: Hardcoded bottom of container
                            curr_x, curr_y, _ = self.sll[self.index + 1].get_container_bottom()

                            angle = -(math.pi / 2 * smooth(alpha))
                            sine = math.sin(angle)
                            cosine = math.cos(angle)

                            origin_x, origin_y, _ = self.sll[self.index + 1].get_container_center()
                            curr_x = curr_x - origin_x
                            curr_y = curr_y - origin_y

                            new_x = curr_x * cosine - curr_y * sine
                            new_y = curr_x * sine + curr_y * cosine

                            new_x += origin_x
                            new_y += origin_y
                            return [new_x, new_y, 0]

                        # Move next pointer on node being inserted
                        # new_node_start, new_node_end = new_node._pointer_to_next.get_start_and_end()
                        self.node.pointer_to_next.become(
                            SinglyDirectedEdge(
                                start=rotate_start(),
                                end=rotate_end()
                            )
                        )
                    flatten_list(self, normalized_alpha)

    def clean_up_from_scene(self, scene: Scene = None) -> None:
        scene.add(self.node)
        self.node.remove(self.sll)
        scene.remove(self.trav)
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
        self._inserted_node = None
        self._sll_group_to_shift = None
        self._trav = None
        self._anim_pre_reqs = self._get_mob_anim_template()
        self._mob_anims = {}

    def _add_node_and_animate(fn):
        def inner(self, *args, **kwargs):
            print(kwargs)
            if kwargs.get('index') != 0:
                self._index, self._inserted_node = self._add_node(*args, **kwargs)
                self._prev_node_pointer_to_next = self._sll[self._index - 1].pointer_to_next
                # NOTE: Won't work with add_last
                self._sll_group_to_shift = VGroup(*[node for i, node in enumerate(self._sll) if i > self._index], self._sll.tail_pointer)
            fn(self, *args, **kwargs)
            if kwargs.get('index') == 0:
                return self._add_first_equivalent(kwargs.get('data'))
            self._set_trav_conditions(**kwargs)
            return self._account_for_dependencies()
        return inner
    
    def _get_mob_anim_template(self):
        return {
                'aligned': False,
                'add_to_front': False,
                'add_to_back': False,
                'display_trav': False,
                'trav_name': 'trav',
                'trav_placement': {
                    'start': True,
                    'end': False
                }
            }
    
    def _account_for_dependencies(self) -> Animation:
        ALIGNED = self._anim_pre_reqs['aligned']
        ADD_TO_FRONT = self._anim_pre_reqs['add_to_front']
        ADD_TO_BACK = self._anim_pre_reqs['add_to_back']
        DISPLAY_TRAV = self._anim_pre_reqs['display_trav']
        TRAV_NAME = self._anim_pre_reqs['trav_name']

        if ALIGNED and DISPLAY_TRAV and ADD_TO_FRONT:
            raise RuntimeError('You cannot have an aligned animation with display trav when adding to front of linked list')
        
        # if ADD_TO_FRONT:
        #     return self._add_first_equivalent()
        
        if not ALIGNED:
            self._inserted_node.container.next_to(self._sll[self._index + 1].container, DOWN)
            self._inserted_node.pointer_to_next.become(SinglyDirectedEdge(start=self._inserted_node.get_container_top(), end=self._sll[self._index + 1].get_container_bottom()))


        if not DISPLAY_TRAV:
            self._trav = Circle().fade(1)
            return self._create_animation()
        
        trav_start_list = [position_str for position_str, is_placed in self._anim_pre_reqs['trav_placement'].items() if is_placed]
        if len(trav_start_list) > 1:
            raise RuntimeError('When animating singly linked list insertion, trav may only have one start position.')
        TRAV_PLACEMENT = trav_start_list[0]

        trav_starting_node = self._sll[0] if TRAV_PLACEMENT == 'start' else self._sll[self._index - 1]
        self._trav = Pointer(
            node=trav_starting_node,
            sll=self._sll,
            label=TRAV_NAME,
            direction=UP
        )

        self._trav.set_opacity(0)
        self._sll.add(self._trav)
        

        animation_num = 1
        beginning_trav_animations = {
            animation_num: {
                'trav_fade_in': {'mobject': self._trav}
            }
        }

        animation_num += 1

        # If trav will be starting at its last position, we just need to fade it in
        if TRAV_PLACEMENT == 'start':
            for node_index in range(self._index - 1):
                beginning_trav_animations[animation_num] = {
                    'trav_move': {
                        'mobject': self._trav,
                        'curr_node': self._sll[node_index],
                        'next_node': self._sll[node_index + 1]
                    }
                }
                animation_num += 1

        updated_mob_anims = beginning_trav_animations


        for mob_group in self._mob_anims.values():
            updated_mob_anims[animation_num] = mob_group
            animation_num += 1

        self._mob_anims = updated_mob_anims

        return self._create_animation()
    
    def _add_node(self, index: int, data: Any, **kwargs) -> None:
        node = SLLNode(data)
        node.next_to(self._sll[index + 1], LEFT, buff=1)
        node.set_next(self._sll._nodes[index])

        node.add(node._pointer_to_next)
        node.add(node._container)

        self._sll._nodes.insert(index, node)
        self._sll.add(node)

        self._sll._head = node
        return index, node
    
    def _create_animation(self):
        if self._inserted_node is None or self._mob_anims is None:
            raise RuntimeError('Make node or mob_anims has not been set yet!')
        
        animation = _Insert(
            sll=self._sll,
            index=self._index,
            node=self._inserted_node,
            prev_node_pointer_to_next=self._prev_node_pointer_to_next,
            trav=self._trav,
            sll_group_to_shift=self._sll_group_to_shift,
            mob_anims=self._mob_anims
        )

        # self._mob_anims = self._get_mob_anim_template()
        self._mob_anims = {}

        return animation
    
    def _set_trav_display(self, is_displayed: bool) -> None:
        self._anim_pre_reqs['display_trav'] = is_displayed

    def _set_trav_position(self, position: str) -> None:
        other_position = 'end' if position == 'start' else 'start'
        self._anim_pre_reqs['trav_placement'][position] = True
        self._anim_pre_reqs['trav_placement'][other_position] = False

    def _set_aligned(self, aligned: bool) -> None:
        self._anim_pre_reqs['aligned'] = aligned

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
    
    def _add_container_fade_in(self, group_num: int = None) -> None:
        key = 'container_fade_in'
        # value = {'mobject': self._inserted_node.container}
        value = {'mobject': self._inserted_node}
        self._add_to_mob_anims(group_num, key, value)

    def _add_pointer_to_next_fade_in(self, group_num: int = None) -> None:
        key = 'pointer_to_next_fade_in'
        # value = {'mobject': self._inserted_node.pointer_to_next}
        value = {'mobject': self._inserted_node}
        self._add_to_mob_anims(group_num, key, value)

    def _add_prev_node_pointer_to_next_move(self, group_num: int = None) -> None:
        key = 'prev_node_pointer_to_next_move'
        value = {'mobject': self._prev_node_pointer_to_next}
        self._add_to_mob_anims(group_num, key, value)

    def _add_flatten(self, group_num: int = None) -> None:
        key = 'flatten'
        value = {'mobject': self._sll_group_to_shift}
        self._add_to_mob_anims(group_num, key, value)

    def _add_shift_sub_list(self, group_num: int = None) -> None:
        key = 'shift_sub_list'
        value = {'mobject': self._sll_group_to_shift}
        self._add_to_mob_anims(group_num, key, value)

    def _set_add_to_front(self, add_to_front: bool) -> None:
        self._anim_pre_reqs['add_to_front'] = add_to_front
        self._anim_pre_reqs['add_to_back'] = not add_to_front

    def _set_add_to_back(self, add_to_back: bool) -> None:
        self._anim_pre_reqs['add_to_back'] = add_to_back
        self._anim_pre_reqs['add_to_front'] = not add_to_back

    def _set_trav_conditions(self, *, index: int, aligned: bool, trav_displayed: bool, trav_position: str, **kwargs) -> None:
        self._set_aligned(aligned)
        if index == 0:
            self._set_add_to_front(True)
        if (aligned and (index == 0 or index == len(self._sll))) \
        or not aligned:
            self._set_trav_display(trav_displayed)
            self._set_trav_position(trav_position)

            if index == 0:
                self._remove_prev_node_pointer_to_next_move()
        else:
            self._set_trav_display(False)

            # TODO: Temporary fix for aligned insertion not at front or end
            ###############################################################
            self._inserted_node.remove(self._inserted_node.pointer_to_next)
            self._inserted_node.set_next(self._sll[self._index + 2])
            self._inserted_node.next = self._sll[self._index]
            for submobject in self._inserted_node.submobjects:
                submobject.set_opacity(0)
            ###############################################################

            self._clear_mob_anims()
            self._add_container_fade_in()
            self._add_pointer_to_next_fade_in(-1)
            self._add_shift_sub_list(-1)

    def _add_first_equivalent(self, data: Any) -> Animation:
        add_first_obj = AddFirst(self._sll)
        # data = self._inserted_node.data._value
        # self._inserted_node.remove(self._inserted_node.pointer_to_next)

        # self._inserted_node._pointer_to_next = None
        # return add_first_obj.node_then_pointer_then_trav_then_center(data)
        print(self._mob_anims)
        if len(self._mob_anims) == 1:
            return add_first_obj.all_together(data)
        elif len(self._mob_anims) == 2:
            if self._mob_anims[1] == 'container_fade_in':
                return add_first_obj.node_then_everything_else(data)
            elif 'container_fade_in' in self._mob_anims[1] and 'pointer_to_next_fade_in':
                return add_first_obj.node_and_pointer_then_everything_else(data)
            elif len(self._mob_anims[2]) and 'shift_sub_list' in self._mob_anims[2]:
                return add_first_obj.node_and_pointer_and_trav_then_center(data)
        elif len(self._mob_anims) == 3:
            if len(self._mob_anims[1]) == 1 and len(self._mob_anims[2]) == 1:
                return add_first_obj.node_then_pointer_then_trav_and_center(data)
            elif len(self._mob_anims[1]) == 2:
                return add_first_obj.node_and_pointer_then_trav_then_center(data)
            else:
                return add_first_obj.node_then_pointer_and_trav_then_center(data)
        elif len(self._mob_anims) == 4:
            return add_first_obj.node_then_pointer_then_trav_then_center(data)
        
            

    @_add_node_and_animate
    def one_by_one(
        self,
        *,
        index: int,
        data: Any,
        aligned: bool,
        trav_displayed: bool,
        prev_node_pointer_is_first: bool = False,
        trav_position: str = 'start',
    ) -> Animation:
        self._add_container_fade_in()
        if prev_node_pointer_is_first:
            self._add_prev_node_pointer_to_next_move()
            self._add_pointer_to_next_fade_in()
        else:
            self._add_pointer_to_next_fade_in()
            self._add_prev_node_pointer_to_next_move()
        self._add_flatten()

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
        data: Any,
        aligned: bool = True,
        trav_displayed: bool = False,
        trav_position: str = 'start'
    ):
        self._add_container_fade_in()
        self._add_pointer_to_next_fade_in(-1)
        self._add_shift_sub_list(-1)