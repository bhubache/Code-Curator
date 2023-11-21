from __future__ import annotations

from typing import TYPE_CHECKING

from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut
from manim import Mobject
from manim import Scene
from manim import Transform

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.graph import Graph

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList

logger = CustomLogger.getLogger(__name__)


class TransformSinglyLinkedList(AnimationGroup):
    def __init__(self, mobject: SinglyLinkedList, target_mobject: SinglyLinkedList, **kwargs) -> None:
        self.mobject = mobject
        self.target_mobject = target_mobject

        # TODO: Figure out what these methods do exactly
        mobject_family_members = set(mobject.family_members_with_points())
        target_mobject_family_members = set(target_mobject.family_members_with_points())

        def get_original_id(mobject: Mobject) -> str:
            try:
                return mobject.original_id
            except AttributeError:
                return str(id(mobject))

        mobject_family_ids = {str(id(mob)) for mob in mobject_family_members}
        target_mobject_family_original_ids = {get_original_id(mob) for mob in target_mobject_family_members}

        transforming_submobject_ids = mobject_family_ids.intersection(target_mobject_family_original_ids)
        fading_out_submobject_ids = mobject_family_ids - target_mobject_family_original_ids
        fading_in_submobject_ids = target_mobject_family_original_ids - mobject_family_ids

        self.transform_animations = []

        for submobject_id in transforming_submobject_ids:
            original_to_target = []

            for mobject in mobject_family_members:
                if str(id(mobject)) == submobject_id:
                    original_to_target.append(mobject)
                    break

            for mobject in target_mobject_family_members:
                if mobject.original_id == submobject_id:
                    original_to_target.append(mobject)
                    break

            self.transform_animations.append(Transform(*original_to_target))

        self.fading_out_animations = []

        for submobject_id in fading_out_submobject_ids:
            for mobject in mobject_family_members:
                if str(id(mobject)) == submobject_id:
                    self.fading_out_animations.append(FadeOut(mobject))

        self.fading_in_animations = []

        for submobject_id in fading_in_submobject_ids:
            for mobject in target_mobject_family_members:
                if get_original_id(mobject) == submobject_id:
                    self.fading_in_animations.append(FadeIn(mobject))

        super().__init__(*(self.transform_animations + self.fading_out_animations + self.fading_in_animations))

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        try:
            scene.replace(self.mobject, self.target_mobject)
        except ValueError:
            logger.warning(
                "When a submobject is removed from a parent mobject, manim extracts all submobjects from parent and"
                " places them in scene.mobjects",
            )
            mobjects = []
            for mob in scene.mobjects:
                if mob in self.mobject:
                    if self.target_mobject not in mobjects:
                        mobjects.append(self.target_mobject)

                    continue

                mobjects.append(mob)

            scene.mobjects = mobjects

        logger.warning(
            "It seems an extra ``Graph`` is being added to the screen. Removing it. This may interfere with animations"
            " that actually intend to have a graph as well",
        )
        mobjects_without_graph = []
        for mobject in scene.mobjects:
            if not isinstance(mobject, Graph):
                mobjects_without_graph.append(mobject)

        scene.mobjects = mobjects_without_graph
