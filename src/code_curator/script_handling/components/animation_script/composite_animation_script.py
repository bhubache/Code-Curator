from __future__ import annotations

import inspect
from collections.abc import Callable
from collections.abc import Sequence
from types import GeneratorType

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.script_handling.components.alignment_script.alignments.aligned_script import AlignedScript
from manim import Animation

from .animation_leaf import AnimationLeaf
from .animation_script import AnimationScript
logger = CustomLogger.getLogger(__name__)


# TODO: ORGANIZE

class CompositeAnimationScript(AnimationScript):
    def __init__(self, unique_id: str, children: list[AnimationLeaf]):
        self._unique_id = unique_id
        self._children = children
        self._parent = None
        self._animations: list[Animation] = []
        self._is_overriding_animation = False

    def __str__(self) -> str:
        new_line = '\n'
        tab = '\t'
        new_line_and_tab = new_line + tab
        return f'{self._unique_id}{new_line}{new_line_and_tab.join([tab+str(child) for child in self._children])}'

    def get_flattened_iterable(self) -> list:
        try:
            return [self.animation]
            # return self.animation
        except AttributeError:
            flattened = []
            for child in self.children:
                flattened += child.get_flattened_iterable()

            return flattened

    @property
    def is_overriding_animation(self) -> bool:
        return self._is_overriding_animation

    @is_overriding_animation.setter
    def is_overriding_animation(self, value: bool) -> None:
        self._is_overriding_animation = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent: CompositeAnimationScript):
        self._parent = new_parent
        for child in self.children:
            child.parent = self

    @property
    def text(self):
        raise NotImplementedError()

    @property
    def num_words(self):
        total_words = 0
        for child in self.children:
            total_words += child.num_words
        return total_words

    @property
    def children(self):
        return self._children

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def audio_duration(self):
        total_duration = 0.0
        for child in self.children:
            total_duration += child.audio_duration
        return total_duration

    @property
    def animation_run_time(self):
        total_run_time = 0.0
        for child in self.children:
            total_run_time += child.animation_run_time
        return total_run_time

    def get_child(self, unique_id: str) -> AnimationScript:
        for child in self.children:
            if child.unique_id == unique_id:
                return child

        raise LookupError(f'Unable to find child ``{unique_id}`` of parent ``{self.unique_id}``')

    def set_child(self, unique_id: str, new_child: AnimationScript) -> None:
        for i, child in enumerate(self._children):
            if child.unique_id == unique_id:
                self._children[i] = new_child

        raise LookupError(f'Unable to find child ``{unique_id}`` of parent ``{self.unique_id}``')

    # TODO: Raise LookupError if comment can't be found
    def get_component(self, unique_id: str) -> AnimationScript:
        if self.unique_id == unique_id:
            return self

        for child in self.children:
            comp = child.get_component(unique_id)
            if comp is not None:
                return comp

        if self.parent is None:
            raise LookupError(f'Unable to find component of {self.unique_id} matching {unique_id}.')

    # TODO: I believe there's some wasted time recalculating this recursively every time
    def apply_alignments(self, start, end, aligned_script: AlignedScript):
        for child in self.children:
            child.apply_alignments(
                start, start + child.num_words - 1, aligned_script,
            )

            start += child.num_words

    def component_uses_code_timing(self, leaf_unique_id: str) -> bool:
        comp = self.get_component(leaf_unique_id)
        if comp is None:
            logger.error(
                f'Component by the name {leaf_unique_id} does not exist',
            )
            # raise ValueError(f'Component by the name {leaf_unique_id} does not exist')
            return False

        return comp.use_code_timing

    @property
    def use_code_timing(self):
        return False

    def apply_code_timing(self, section_name: str, func: Callable):
        comp = self.get_component(section_name)
        comp_animations = func()

        new_leaves = []
        for i, animation in enumerate(comp_animations):
            new_leaf_id = f'{section_name}_{i}'
            new_leaf = AnimationLeaf(
                unique_id=new_leaf_id, text=comp.text, is_wait_animation=False,
            )
            new_leaf.add_animation(new_leaf_id, func, animation)
            new_leaf.audio_duration = animation.run_time
            new_leaves.append(new_leaf)
        new_composite = CompositeAnimationScript(
            unique_id=section_name, children=new_leaves,
        )
        self.set_child(unique_id=section_name, new_child=new_composite)

    def _check_that_unique_id_exists(fn):
        def inner(*args, **kwargs):
            call_args: dict = inspect.getcallargs(fn, *args, **kwargs)
            self: CompositeAnimationScript = call_args.get('self')
            unique_id: str = call_args.get('unique_id')
            if not self._unique_id_exists(unique_id):
                raise Exception(
                    f'The name {unique_id} is not present in {self._unique_id}',
                )
            output = fn(*args, **kwargs)
            return output
        return inner

    def _unique_id_exists(self, unique_id: str) -> bool:
        if self._unique_id == unique_id:
            return True

        for child in self._children:
            if child._unique_id_exists(unique_id):
                return True
        return False

    def add_animation(
        self,
        unique_id: str,
        func: Callable,
        animation: Sequence[Animation],
        is_overriding_animation: bool,
    ) -> None:
        if isinstance(animation, GeneratorType):
            child = self.get_child(unique_id)
            child.is_overriding_animation = is_overriding_animation
            child.animation = animation

            # val = next(animation)
            # breakpoint()
            # val = val()
            # val = next(val)
            # val = val()
            # val = next(val)
            # val = val()
            # val = next(val)
            # for generator_func in animation:
            #     child.add_animation(
            #         unique_id=generator_func.__name__,
            #         func=(generator := generator_func()),
            #         animation=generator,
            #         is_overriding_animation=False,
            #     )

            return

        component = self.get_component(unique_id)
        if isinstance(component, AnimationLeaf):
            if len(animation) > 1:
                raise ValueError('Should only be adding one animation to AnimationLeaf.')

            anim = animation[0]
            component.add_animation(
                unique_id=unique_id,
                func=func,
                animation=anim,
            )
        elif isinstance(component, CompositeAnimationScript):
            if len(animation) == 1:
                raise Exception('Is this supposed to happen?')
            else:
                for i, (child, anim) in enumerate(zip(self.children, animation)):
                    is_overriding_start = i == 0
                    is_overriding_end = i == len(self.children) - 1

                    if i > 0:
                        # We only want the real function to be called once so we let the first leaf have it
                        def func():
                            return 0

                    child.add_animation(
                        unique_id=f'{unique_id}_{i}', func=func, animation=anim,
                        is_overriding_start=is_overriding_start, is_overriding_end=is_overriding_end,
                    )

    def add_animation_v2(
        self,
        unique_id: str,
        func: Callable,
        animation: Sequence[Animation],
        is_overriding_animation: bool,
    ) -> bool:
        if self.unique_id == unique_id:
            if not isinstance(animation, Sequence):
                raise TypeError(f'animation should be of type Sequence, not {type(animation)}')

            self.is_overriding_animation = is_overriding_animation
            if len(animation) == 1:
                raise Exception('Is this supposed to happen?')
            elif len(animation) > 1:
                # Create new leaves
                for i, (child, anim) in enumerate(zip(self.children, animation)):
                    is_overriding_start = i == 0
                    is_overriding_end = i == len(self.children) - 1

                    if i > 0:
                        # We only want the real function to be called once so we let the first leaf have it
                        def func(): return 0

                    child.add_animation(
                        unique_id=f'{unique_id}_{i}', func=func, animation=anim,
                        is_overriding_start=is_overriding_start, is_overriding_end=is_overriding_end,
                    )
            else:
                raise ValueError(f'Length of animations must be greater than zero: given {len(animation)}')
        else:
            if not isinstance(animation, Sequence):
                return

            if len(animation) == 1:
                anim = animation[0]
            elif len(animation) > 1:
                anim = animation
            else:
                ValueError(f'There must be at least one animation: given {len(animation)}')

            for child in self.children:
                if isinstance(child, AnimationLeaf):
                    child.add_animation(
                        unique_id=unique_id,
                        func=func,
                        animation=anim,
                    )
                else:
                    child.add_animation(
                        unique_id=unique_id,
                        func=func,
                        animation=anim,
                        is_overriding_animation=is_overriding_animation,
                    )

    def add_animation_v1(self, unique_id: str, func: Callable, animation, is_overriding_animation: bool) -> bool:
        # If we're not at the correct component, search children
        if self.unique_id != unique_id:
            for child in self.children:
                try:
                    child.add_animation(
                        unique_id, func, func()[
                            0
                        ], is_overriding_animation,
                    )
                except TypeError:
                    child.add_animation(
                        unique_id,
                        func,
                        func()[0],
                        is_overriding_animation,
                    )
        else:
            animations = animation
            try:
                len(animations)
            except TypeError:
                animations = func()

            assert len(self.children) == len(animations)

            self.is_overriding_animation = True

            for i, (child, animation) in enumerate(zip(self.children, animations)):
                # if isinstance(animation, Callable):
                #     func = animation
                #     animation = animation()
                is_overriding_start = i == 0
                is_overriding_end = i == len(self.children) - 1

                if i > 0:
                    # We only want the real function to be called once so we let the first leaf have it
                    def func(): return 0

                child.add_animation(
                    unique_id=f'{unique_id}_{i}', func=func, animation=animation,
                    is_overriding_start=is_overriding_start, is_overriding_end=is_overriding_end,
                )
                # if i == 0:
                #     child.add_animation(unique_id=f'{unique_id}_{i}', func=func, animation=animation)
                # else:
                #     child.add_animation(unique_id=f'{unique_id}_{i}', func=lambda : 0, animation=animation)

    # # TODO: Get rid of the try except statement
    # def add_animations(self, unique_id: str, animations: list[Animation], is_overriding_animation: bool) -> bool:
    #     found_composite = False
    #     # FIXME: Check for using closures to pass animation information to
    #       capture dependencies like position elements on screen
    #     if callable(animations) and self.get_child(unique_id).use_code_timing:
    #         found_composite = False
    #         section_leaf = self.get_child(unique_id)
    #         actual_animations = animations()
    #         if section_leaf.use_code_timing:
    #             new_leaves = []
    #             for i, animation in enumerate(actual_animations):
    #                 new_leaf = AnimationLeaf(
    # unique_id=f'{section_leaf.unique_id}_{i}', text=section_leaf.text, is_wait_animation=False
    # )
    #                 new_leaf.add_animation(animation)
    #                 new_leaf.audio_duration = animation.run_time
    #                 new_leaves.append(new_leaf)
    #             new_tree_part = None
    #             if len(actual_animations) > 1:
    #                 new_tree_part = CompositeAnimationScript(unique_id=section_leaf.unique_id, children=new_leaves)
    #             else:
    #                 new_tree_part = new_leaves[0]
    #             self.set_child(unique_id=unique_id, new_child=new_tree_part)
    #     elif self.unique_id != unique_id:
    #         for child in self.children:
    #             if isinstance(child, AnimationLeaf):
    #                 if child.unique_id != unique_id: continue
    #                 else:
    #                     try:
    #                         child.add_animation(animations[0])
    #                     except Exception:
    #                         logger.error('ISSUE FOUND')
    #                         logger.error(animations)
    #                         raise
    #             elif child.add_animations(unique_id, animations, is_overriding_animation): return True
    #     else:
    #         assert len(self.children) == len(animations), 'number of children don\'t match number of animations!'
    #         found_composite = True
    #         self.is_overriding_animation = is_overriding_animation
    #         for i, (child, anim) in enumerate(zip(self.children, animations)):
    #             is_overriding_start = False
    #             is_overriding_end = False
    #             if i == 0:
    #                 is_overriding_start = True
    #             elif i == len(self.children) - 1:
    #                 is_overriding_end = True
    #             child.add_animation(
    #                 anim, is_overriding_start=is_overriding_start, is_overriding_end=is_overriding_end
    #             )
    #     return found_composite
