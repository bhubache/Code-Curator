from __future__ import annotations

from typing import TYPE_CHECKING

from manim import config
from manim import Mobject
from manim import Scene

from code_curator.animations.curator_animation import CuratorAnimation
from code_curator.custom_logging.custom_logger import CustomLogger

if TYPE_CHECKING:
    import types

logger = CustomLogger.getLogger(__name__)

config["background_color"] = "#282C34"
config["disable_caching"] = True


class TopLevelBaseSceneMobject(Mobject):
    """"""


class _OneElementMobjectListDescriptor:
    def __set_name__(self, owner, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance, owner=None):
        if not hasattr(instance, self.private_name):
            setattr(instance, self.private_name, [TopLevelBaseSceneMobject()])

        return getattr(instance, self.private_name)

    def __set__(self, instance, value) -> None:
        return


class BaseScene(Scene):
    mobjects = _OneElementMobjectListDescriptor()

    def __init__(self, animation_script=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.animation_script = animation_script

    @property
    def submobjects(self) -> list[Mobject]:
        return self.mobjects[0].submobjects

    @property
    def moving_mobjects(self):
        return self.get_mobject_family_members()

    @moving_mobjects.setter
    def moving_mobjects(self, new_value) -> None:
        pass

    def add(self, *mobjects) -> None:
        for mob in mobjects:
            self.mobjects[0].add(mob)

    def remove(self, *mobjects) -> None:
        for mob in mobjects:
            self.mobjects[0].remove(mob)

    def clear(self):
        self.mobjects[0].submobjects = []
        self.foreground_mobjects = []
        return self

    def add_foreground_mobject(self, mobject: Mobject):
        mobject.z_index = 1
        self.add(mobject)

    def remove_foreground_mobject(self, mobject: Mobject):
        mobject.z_index = 0

    def get_start_time(self, method: types.MethodType) -> float:
        for entry in self.animation_script.entries:
            if entry["name"] == method.__name__:
                return entry["start_time"]

        raise RuntimeError("Unable to get start time")

    def construct(self) -> None:
        self.play(
            CuratorAnimation(
                self.mobjects[0],
                animation_script=self.animation_script,
                scene=self,
                run_time=self.animation_script.run_time,
            ),
        )
