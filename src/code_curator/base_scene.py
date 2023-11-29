from __future__ import annotations


from manim import config
from manim import Mobject
from manim import Scene

from code_curator import constants
from code_curator.animations.curator_animation_new import CuratorAnimation
from code_curator.animations.curator_animation_new import ExcludeDuplicationSubmobjectsMobject
from code_curator.custom_logging.custom_logger import CustomLogger


logger = CustomLogger.getLogger(__name__)


class MyClass:
    """Meant to simply hold attributes so one instance can be shared across streams."""


class _AllowOneMobjectList(list):
    def __setitem__(self, key, mobjects) -> None:
        raise NotImplementedError()


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
    # config["background_color"] = constants.DEFAULT_BACKGROUND_COLOR
    config["background_color"] = "#282C34"
    # config["background_color"] = "#2D3139"
    # config["background_color"] = "#414855"
    # config["background_color"] = "#3D424B"
    # config["background_color"] = "#33373D"
    config["disable_caching"] = True

    mobjects = _AllowOneMobjectDescriptor()

    def __init__(self, animation_script, **kwargs) -> None:
        super().__init__(**kwargs)
        self.animation_script = animation_script

    def construct(self) -> None:
        self.play(
            CuratorAnimation(
                animation_script=self.animation_script._animation_script["Video"],
                scene=self,
                run_time=self.animation_script.run_time,
            ),
        )

    @property
    def scene_mobjects(self) -> list[Mobject]:
        return self.mobjects[0].submobjects

    def replace(self, old_mobject: Mobject, new_mobject: Mobject) -> None:
        self.mobjects[0].submobjects.remove(old_mobject)
        # TODO: May have to insert new_mobject at the same index old_mobject was at
        self.mobjects[0].submobjects.append(new_mobject)

        # Keep only the copies of data structures
        copy_to_original = {}
        for i, submobject_outer in enumerate(self.mobjects[0].submobjects):
            for submobject_inner in self.mobjects[0].submobjects[i + 1 :]:
                try:
                    if submobject_inner.original_id == str(id(submobject_outer)):
                        copy_to_original[submobject_inner] = submobject_outer
                        break
                except AttributeError:
                    continue

        for submobject in copy_to_original:
            if submobject not in self.mobjects[0].submobjects:
                self.mobjects[0].submobjects.append(submobject)

        for submobject in copy_to_original.values():
            self.mobjects[0].submobjects.remove(submobject)
