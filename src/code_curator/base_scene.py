from __future__ import annotations

import inspect
import itertools
from abc import ABC
from abc import abstractmethod
from collections.abc import Callable
from collections.abc import Generator
from collections.abc import Iterable

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.scene_scheduler import SceneScheduler
from code_curator.script_handling.components.animation_script.animation_leaf import AnimationLeaf
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript
from manim import config
from manim import FadeIn
from manim import FadeOut
from manim import Scene
from manim import Wait
logger = CustomLogger.getLogger(__name__)


class BaseScene(ABC, Scene):
    """Test docstring

    :param ABC: _description_
    :type ABC: _type_
    :param Scene: _description_
    :type Scene: _type_
    :raises RuntimeError: _description_
    :return: _description_
    :rtype: _type_
    """
    config.background_color = '#000E15'

    def __init__(self, problem_dir: str, aligned_animation_scene: CompositeAnimationScript) -> None:
        Scene.__init__(self)
        # CuratorAnimation.animation_scene_script = aligned_animation_scene
        self._aligned_animation_scene: CompositeAnimationScript = aligned_animation_scene
        self._problem_dir: str = problem_dir
        self._animation_spec: dict = {}
        self._scene_scheduler: SceneScheduler = SceneScheduler()
        self._mobjects_pickle: str = 'mobjects_pickle.pkl'

    def __getattr__(self, attr_name):
        section_name = inspect.stack()[1].function
        subsection_name = '_'.join(attr_name.split('_')[:-1])
        subsection_number = attr_name.split('_')[-1]
        if subsection_number.isnumeric():
            animation_leaf = self.aligned_animation_scene.get_component(f'{section_name}_{subsection_number}')
            timing_info = getattr(animation_leaf, animation_leaf.SUBANIMATION_TIMINGS_NAME)
            return timing_info[subsection_name].copy()
        else:
            animation_leaf = self.aligned_animation_scene.get_component(section_name)
            timing_info = getattr(animation_leaf, animation_leaf.SUBANIMATION_TIMINGS_NAME)
            return timing_info[section_name].copy()

    @property
    def aligned_animation_scene(self) -> CompositeAnimationScript:
        return self._aligned_animation_scene

    @property
    def problem_dir(self) -> str:
        return self._problem_dir

    @property
    def animation_spec(self) -> dict:
        return self._animation_spec

    @property
    def scene_scheduler(self) -> SceneScheduler:
        return self._scene_scheduler

    # NOTE: This may not work with multiple scenes!!!
    def setup(self) -> None:
        rolled_up_animations = self.scene_scheduler.schedule(
            self.aligned_animation_scene,
        )

        for i, composite in enumerate(rolled_up_animations):
            try:
                if composite.is_overriding_animation:
                    rolled_up_animations[i] = self.super_add_overriding_animation(
                        composite,
                    )
            except AttributeError:
                pass

        rolled_up_animations.insert(-1, self.aligned_animation_scene.get_child('remove_duplication').animation)

        self._animations = rolled_up_animations

    def construct(self) -> None:
        # anim = self._animations[0]
        # anim.func()
        # self.play(anim.animation)

        for obj in self._animations:
            if isinstance(obj, AnimationLeaf):
                obj.func()
                self.play(obj.animation)
            elif callable(obj):
                obj()
            elif isinstance(obj, Generator):
                # TODO: Handle wait animations elsewhere
                for elem in itertools.chain.from_iterable(obj):
                    self.play(elem)
                    wait_animation = self.__create_filling_wait_animation(elem)
                    if wait_animation is not None:
                        self.play(wait_animation)
            else:
                raise RuntimeError(
                    f'Unexpected type {type(obj)} when running animations: {obj}',
                )

    def __create_filling_wait_animation(self, animation) -> Wait:
        try:
            if animation.remaining_time > 0:
                return Wait(animation.remaining_time)
        except AttributeError:
            return Wait(min(sub_anim.remaining_time for sub_anim in animation.animations))

    def _from_iterable(self, iterables):
        for it in iterables:
            yield from it

    def tear_down(self) -> None:
        self.play(FadeOut(*self.mobjects))

    @abstractmethod
    def create_animation_spec(self) -> dict:
        pass

    def super_add_overriding_animation(self, composite: CompositeAnimationScript) -> Callable:
        def inner() -> None:
            mobjects_on_screen_before_animation = self.mobjects.copy()

            self.play(
                FadeOut(*self.mobjects),
                run_time=composite.override_start_time,
            )

            for child in composite.children:
                self.play(child.animation)

            try:
                self.play(
                    FadeOut(*self.mobjects),
                    run_time=composite.override_end_time,
                )
            except AttributeError:
                # FIXME: THIS IS A WORKAROUND!
                self.play(
                    FadeOut(*self.mobjects),
                    run_time=0.5,
                )
            try:
                self.play(
                    FadeIn(*mobjects_on_screen_before_animation),
                    run_time=composite.override_end_time,
                )
            except AttributeError:
                # FIXME: THIS IS A WORKAROUND!
                self.play(
                    FadeIn(*mobjects_on_screen_before_animation),
                    run_time=0.5,
                )

        return inner

    def add_base_animations(self) -> None:
        for section_name, func in self.animation_spec.items():
            if self.aligned_animation_scene.component_uses_code_timing(section_name):
                self.aligned_animation_scene.apply_code_timing(
                    section_name, func,
                )
            else:
                if self._func_outputs_list_of_funcs(func):
                    # FIXME: index as name will only work for constraints children and similar situations
                    list_of_funcs = func()
                    for i, anim_func in enumerate(list_of_funcs):
                        parent_of_animations = self.aligned_animation_scene.get_child(section_name)
                        parent_of_animations.add_animation(
                            # unique_id=f'{section_name}_{i}',
                            unique_id=i,
                            func=anim_func, animation=anim_func(),
                            is_overriding_animation=False,
                        )
                else:
                    self.aligned_animation_scene.add_animation(
                        unique_id=section_name,
                        func=func, animation=func(),
                        is_overriding_animation=False,
                    )

    def _func_outputs_list_of_funcs(self, func: Callable) -> bool:
        poorly_named_var = func()
        if isinstance(poorly_named_var, Iterable):
            for elem in poorly_named_var:
                if isinstance(elem, type(func)):
                    return True

        return False
