from __future__ import annotations

import inspect
from collections.abc import Generator
from collections.abc import Sequence
from typing import TYPE_CHECKING

from manim import Animation
from manim import AnimationGroup

from code_curator.animations.curator_animation import CuratorAnimation
from code_curator.animations.fixed_succession import FixedSuccession
from code_curator.auto_animation_timer import AutoAnimationTimer


if TYPE_CHECKING:
    from types import TracebackType
    from code_curator.base_scene import BaseScene
    from ..script_handling.components.animation_script.animation_script import (
        AnimationScript,
    )


class AnimationGenerator(Generator):
    def __init__(self, *args, owner: BaseScene | None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.sub_generators: Sequence[Generator] = []

    def __getattr__(self, item: str):
        owner = self.owner
        while True:
            try:
                return getattr(owner, item)
            except AttributeError:
                try:
                    owner = owner.owner
                except AttributeError:
                    print(f"Unable to find item {item}!")
                    raise

    @property
    def namespace_path(self) -> list[str]:
        namespace_parts: list[str] = []
        owner = self
        while isinstance(owner, AnimationGenerator):
            namespace_parts.insert(0, owner.__class__.__name__)
            owner = owner.owner

        return namespace_parts

    @property
    def aligned_animation_script_owner(self) -> AnimationScript:
        child = self.owner.aligned_animation_scene

        for child_id in self.namespace_path:
            child = child.get_child(child_id)

        return child

    def prep_rendering(self):
        self.sub_generators = self._get_organized_sub_generators()

    def send(self, value=None):
        return self._get_sub_generators()

    def throw(
        self,
        type_: type[BaseException],
        val: BaseException | object = ...,
        tb: TracebackType | None = ...,
    ):
        pass

    @staticmethod
    def _is_generator_function(obj) -> bool:
        return inspect.isgeneratorfunction(obj)

    def _get_organized_sub_generators(self):
        sub_generators = []
        for attr_name in dir(self):
            try:
                attr_value = getattr(self, attr_name)
            except AttributeError:
                continue

            if self._is_specified_in_animation_scene(attr_value) and self._is_generator(
                attr_value,
            ):
                sub_generators.append(attr_value)

        return sub_generators

    def _is_specified_in_animation_scene(self, obj) -> bool:
        try:
            obj_namespace_path = self.namespace_path + [self._get_gen_name(obj)]
        except AttributeError:
            return False
        else:
            try:
                return self.owner.namespace_path_exists(obj_namespace_path)
            except AttributeError:
                return self.namespace_path_exists(obj_namespace_path[1:])

    def _is_generator(self, obj) -> bool:
        return self._is_generator_function(obj) or issubclass(obj, Generator)

    # TODO: Ensure generator methods are ordered according to animation script
    def _get_sub_generators(self):
        for gen_method in self.sub_generators:
            if self._is_generator_function(gen_method):
                gen_method = AutoAnimationTimer.time(
                    gen_method,
                    owner=self,
                )
                self._insert_timing_logic(gen_method)
                yield gen_method(self)
            else:
                yield from gen_method(owner=self).send(None)

    def _insert_timing_logic(self, gen_method):
        for attr_value in gen_method.__globals__.values():
            if (
                isinstance(attr_value, type)
                and issubclass(attr_value, Animation)
                and attr_value is not Animation
                and attr_value is not AnimationGroup
                and attr_value is not FixedSuccession
            ):
                CuratorAnimation._owner = self
                if CuratorAnimation not in attr_value.__bases__:
                    try:
                        attr_value.__bases__ = (
                            CuratorAnimation,
                        ) + attr_value.__bases__
                    except TypeError:
                        breakpoint()

    def _get_gen_name(self, obj) -> str:
        return obj.__name__
