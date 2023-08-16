from __future__ import annotations

import inspect
from collections.abc import Generator
from types import MethodType
from types import TracebackType
from typing import Type
from types import FunctionType

from manim import Animation
from manim import AnimationGroup

from code_curator.animations.fixed_succession import FixedSuccession
from code_curator.auto_animation_timer import AutoAnimationTimer
from code_curator.animations.curator_animation import CuratorAnimation
from code_curator.base_scene import BaseScene
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript


class AnimationGenerator(Generator):
    def __init__(self, owner: BaseScene) -> None:
        super().__init__()
        self.owner = owner
        self.sub_generators = self._get_organized_sub_generators()
        # self._insert_timing_logic()

    def __getattr__(self, item: str):
        owner = self.owner
        while True:
            try:
                return getattr(owner, item)
            except AttributeError:
                try:
                    owner = owner.owner
                except AttributeError:
                    print(f'Unable to find item {item}!')
                    breakpoint()

    def _get_organized_sub_generators(self):
        sub_generators = []
        for attr_value in self.__class__.__dict__.values():
            if self._is_specified_in_animation_scene(attr_value) and self._is_generator(attr_value):
                sub_generators.append(attr_value)

        return sub_generators

    def _is_specified_in_animation_scene(self, obj) -> bool:
        try:
            obj_namespace_path = self.namespace_path + [self._get_gen_name(obj)]
        except AttributeError:
            return False
        else:
            return self.owner.namespace_path_exists(obj_namespace_path)

    def _is_generator(self, obj) -> bool:
        return self._is_generator_function(obj) or issubclass(obj, Generator)

    @staticmethod
    def _is_generator_function(obj) -> bool:
        return inspect.isgeneratorfunction(obj)

    def _insert_timing_logic(self, gen_method):
        for attr_name, attr_value in gen_method.__globals__.items():
            # from code_curator.animations.change_color import ChangeColor
            # if attr_name == 'ChangeColor':
            #     if attr_value.__name__ == 'inner':
            #         continue
            #     gen_method.__globals__[attr_name] = test_deco(attr_value, self)
            if (isinstance(attr_value, type)
            and issubclass(attr_value, Animation)
            # and not issubclass(attr_value, CuratorAnimation)
            and attr_value is not Animation
            and attr_value is not AnimationGroup
            and attr_value is not FixedSuccession):
                # if attr_value.__name__ == 'inner':
                #     continue
                # gen_method.__globals__[attr_name] = test_deco(attr_value, self)
                CuratorAnimation._owner = self
                if CuratorAnimation not in attr_value.__bases__:
                    try:
                        attr_value.__bases__ = (CuratorAnimation, ) + attr_value.__bases__
                    except TypeError:
                        breakpoint()

# TODO: Ensure generator methods are ordered according to animation script
    def _get_sub_generators(self):
        for gen_method in self.sub_generators:
            if self._is_generator_function(gen_method):
                gen_method = AutoAnimationTimer.time(gen_method, owner=self, aligned_animation_script_owner=self.aligned_animation_script_owner)
                self._insert_timing_logic(gen_method)
                yield gen_method(self)
            else:
                yield from gen_method(owner=self).send(None)

    def _get_gen_name(self, obj) -> str:
        return obj.__name__

    def send(self, value=None):
        return self._get_sub_generators()
        # yield from self.sub_generators

    def throw(
        self,
        type_: Type[BaseException],
        val: BaseException | object = ...,
        tb: TracebackType | None = ...,
    ):
        pass

    @property
    def namespace_path(self) -> list[str]:
        namespace_parts: list[str] = []
        owner = self
        while isinstance(owner, AnimationGenerator):
            namespace_parts.insert(0, owner.__class__.__name__)
            owner = owner.owner

        return namespace_parts

    @property
    def aligned_animation_script_owner(self) -> CompositeAnimationScript:
        child = self.owner.aligned_animation_scene
        for child_id in self.namespace_path:
            child = child.get_child(child_id)

        return child