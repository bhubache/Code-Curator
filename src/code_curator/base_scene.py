from __future__ import annotations

from manim import config
from manim import Mobject
from manim import Scene

from code_curator.animations.curator_animation_new import CuratorAnimation
from code_curator.custom_logging.custom_logger import CustomLogger


logger = CustomLogger.getLogger(__name__)


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
    # config["background_color"] = constants.DEFAULT_BACKGROUND_COLOR
    config["background_color"] = "#282C34"
    # config["background_color"] = "#2D3139"
    # config["background_color"] = "#414855"
    # config["background_color"] = "#3D424B"
    # config["background_color"] = "#33373D"
    config["disable_caching"] = True

    mobjects = _OneElementMobjectListDescriptor()

    def __init__(self, animation_script=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.animation_script = animation_script

    @property
    def submobjects(self) -> list[Mobject]:
        return self.mobjects[0].submobjects

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

    def construct(self) -> None:
        self.play(
            CuratorAnimation(
                self.mobjects[0],
                animation_script=self.animation_script,
                scene=self,
                run_time=self.animation_script.run_time,
            ),
        )
