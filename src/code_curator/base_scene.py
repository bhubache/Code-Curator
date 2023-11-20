from __future__ import annotations

from typing import TYPE_CHECKING

from manim import config
from manim import Group
from manim import Mobject
from manim import Scene

from code_curator import constants
from code_curator.animations.curator_animation_new import CuratorAnimation
from code_curator.animations.curator_animation_new import ExcludeDuplicationSubmobjectsMobject
from code_curator.custom_logging.custom_logger import CustomLogger


if TYPE_CHECKING:
    from .script_handling.components.animation_script.composite_animation_script import (  # noqa: E501
        CompositeAnimationScript,
    )

logger = CustomLogger.getLogger(__name__)


class MyClass:
    """Meant to simply hold attributes so one instance can be shared across streams."""


class _AllowOneMobjectList(list):
    def __setitem__(self, key, mobjects) -> None:
        raise NotImplementedError()
        # if len(mobjects) == 0 and isinstance(mobjects[0], ExcludeDuplicationSubmobjectsMobject):
        #     super().__setitem__(key, mobjects)

        # if len(mobjects) > 1:
        #     raise RuntimeError(f"{self.__class__.__name__}.mobjects should never exceed 1, it is currently {len(self.mobjects)}")

        # if len(mobjects) == 1 and not isinstance(mobjects[0], ExcludeDuplicationSubmobjectsMobject):
        #     raise RuntimeError(f"Only {ExcludeDuplicationSubmobjectsMobject.__name__} should be in {self.__class__.__name__}.mobjects, found {self.mobjects}")


class _AllowOneMobjectDescriptor:
    def __set_name__(self, owner, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance, owner=None):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value) -> None:
        if not hasattr(instance, self.private_name):
            if len(value) != 1:
                return

            if not isinstance(value[0], ExcludeDuplicationSubmobjectsMobject):
                return

            setattr(instance, self.private_name, _AllowOneMobjectList(value[0]))


class BaseScene(Scene):
    config["background_color"] = constants.DEFAULT_BACKGROUND_COLOR
    config["disable_caching"] = True

    mobjects = _AllowOneMobjectDescriptor()

    def __init__(self, animation_script, stream_clses: list[type]) -> None:
        super().__init__()
        self.animation_script = animation_script
        self.stream_instances = []
        self._setup_attrs(stream_clses)

    # @property
    # def mobjects(self) -> Sequence[Mobject]:
    #     if ExcludeDuplicationSubmobjectsMobject() in self._mobjects:
    #         raise BaseException()

    #     return self._mobjects

    # @mobjects.setter
    # def mobjects(self, value: Sequence[Mobject]) -> None:
    #     self._mobjects = value

    # def __instantiate_streams(self, stream_clses: list[type]) -> None:
    #     attrs_before_scene_init

    def _setup_attrs(self, stream_clses: list[type]) -> None:
        attrs_before_attr_setup = set(self.__dict__.keys())
        self.initialize_scene()
        newly_added_attrs = set(self.__dict__.keys()) - attrs_before_attr_setup

        # for stream_inst in self.stream_instances:
        #     for attr_name in newly_added_attrs:
        #         setattr(stream_inst, attr_name, getattr(self, attr_name))

        dict_to_pass = {attr_name: getattr(self, attr_name) for attr_name in newly_added_attrs}

        shared_instance = MyClass()

        for stream_cls in stream_clses:
            self.stream_instances.append(stream_cls(**dict_to_pass, scene=self, shared=shared_instance))

    def setup_attrs(self) -> None:
        pass

    def construct(self) -> None:
        self.play(
            CuratorAnimation(
                self.animation_script._animation_script,
                stream_instances=self.stream_instances,
                run_time=self.animation_script.run_time,
                scene=self,
            ),
        )

    @property
    def scene_mobjects(self) -> list[Mobject]:
        return self.mobjects[0].submobjects

    def replace(self, old_mobject: Mobject, new_mobject: Mobject) -> None:
        # There might be a group with submobjects of a SLL that's also in the scene's mobjects. Remove the duplication
        non_groups = [mob for mob in self.mobjects[0].submobjects if not isinstance(mob, Group)]
        duplicating_mobs = []
        for non_group in non_groups:
            for mob in self.mobjects[0].submobjects:
                if non_group is mob:
                    continue

                # FIXME: Only search groups
                is_duplicating_mob = any(
                    [sub_mob in mob for sub_mob in non_group],
                )
                if is_duplicating_mob:
                    duplicating_mobs.append(non_group)
                    break

        for mob in duplicating_mobs:
            self.mobjects[0].submobjects.remove(mob)

        insertion_index = self.mobjects[0].submobjects.index(old_mobject)
        self.mobjects[0].submobjects.insert(insertion_index, new_mobject)
        self.mobjects[0].submobjects.remove(old_mobject)
