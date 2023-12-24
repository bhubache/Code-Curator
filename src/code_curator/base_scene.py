from __future__ import annotations

from manim import config
from manim import Group
from manim import Mobject
from manim import Scene

from code_curator.animations.curator_animation_new import CuratorAnimation
from code_curator.custom_logging.custom_logger import CustomLogger


logger = CustomLogger.getLogger(__name__)


class _MobjectSentinel(Mobject):
    def __new__(cls):
        if not hasattr(cls, "_singleton_instance"):
            cls._singleton_instance = super().__new__(cls)

        return cls._singleton_instance


class ExcludeDuplicationSubmobjectsMobject(Mobject):
    def __new__(cls):
        if not hasattr(cls, "_singleton_instance"):
            cls._singleton_instance = super().__new__(cls)
            cls._singleton_instance.__initialized = False

        return cls._singleton_instance

    def __init__(self, *args, **kwargs) -> None:
        if self.__initialized:
            return

        self.__initialized = True
        super().__init__(*args, **kwargs)

    def remove(self, *mobjects: Mobject) -> Mobject:
        # If more than one mobject has been passed to a single FadeOut animation,
        # all the mobjects will be wrapped in a Group. So, we need to iterate over
        # the group to remove each mobject.
        for mobject_to_remove in mobjects:
            if isinstance(mobject_to_remove, Group):
                for submobject_to_remove in mobject_to_remove:
                    self.remove(submobject_to_remove)

            self._remove(
                mobject_to_remove=mobject_to_remove,
                mobject_to_search=self,
                mobject_container=None,
            )

        self._remove_all_sentinels()

        return self

    def _remove(
        self,
        *,
        mobject_to_remove: Mobject,
        mobject_to_search: Mobject,
        mobject_container: Mobject | None,
    ) -> None:
        try:
            problem_tex_parent = mobject_to_search.problem_tex_parent
        except AttributeError:
            pass
        else:
            if mobject_to_remove is problem_tex_parent:
                self._place_sentinel(
                    mobject_container=mobject_container,
                    mobject_to_remove=mobject_to_search,
                )

        if mobject_to_remove in mobject_to_search.submobjects:
            self._place_sentinel(
                mobject_container=mobject_to_search,
                mobject_to_remove=mobject_to_remove,
            )

        # FIXME: I think some mobjects aren't being removed because we're modifying
        #   the length of mobject_to_search.submobjects while iterating?

        for mobject in mobject_to_search.submobjects:
            self._remove(
                mobject_to_remove=mobject_to_remove,
                mobject_to_search=mobject,
                mobject_container=mobject_to_search,
            )

    def _place_sentinel(
        self,
        *,
        mobject_container: Mobject,
        mobject_to_remove: Mobject,
    ) -> None:
        index: int = mobject_container.submobjects.index(mobject_to_remove)
        mobject_container.submobjects[index] = _MobjectSentinel()

    def _remove_all_sentinels(self) -> None:
        # TODO: Remove empty Groups?
        new_submobjects = []
        for submobject in self.submobjects:
            if isinstance(submobject, _MobjectSentinel):
                continue

            try:
                submobject.submobjects = self._remove_all_sentinels_helper(submobject)
            except AttributeError:
                pass
            finally:
                new_submobjects.append(submobject)

        self.submobjects = new_submobjects

    def _remove_all_sentinels_helper(self, mobject: Mobject):
        new_submobjects: list[Mobject] = []
        for submobject in mobject.submobjects:
            if isinstance(submobject, _MobjectSentinel):
                continue

            try:
                submobject.submobjects = self._remove_all_sentinels_helper(submobject)
            except AttributeError:
                pass
            finally:
                new_submobjects.append(submobject)

        return new_submobjects


class _AllowOneMobjectDescriptor:
    def __set_name__(self, owner, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance, owner=None):
        # NOTE: Added try/except block to make testing with BaseScene work
        return [ExcludeDuplicationSubmobjectsMobject()]

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

    mobjects = _AllowOneMobjectDescriptor()

    def __init__(self, animation_script=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.animation_script = animation_script

    @property
    def scene_mobjects(self) -> list[Mobject]:
        return self.mobjects[0].submobjects

    def add(self, *mobjects) -> None:
        for mob in mobjects:
            self.mobjects[0].add(mob)

    # # FIXME: remove method
    # def remove(self, *mobjects) -> None:
    #     for mob in mobjects:
    #         self.mobjects[0].remove(mob)

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
