from __future__ import annotations

from typing import TYPE_CHECKING

from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut
from manim import Mobject
from manim import Scene
from manim import Transform

from code_curator.custom_logging.custom_logger import CustomLogger

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList

logger = CustomLogger.getLogger(__name__)


class TransformSinglyLinkedList(AnimationGroup):
    def __init__(self, mobject: SinglyLinkedList, methods, **kwargs) -> None:
        self.mobject = mobject
        self.ungroupified_mobject = mobject
        self.methods = methods
        self.target_mobject = self.mobject.target

        mobject_family_members = set(self.mobject.family_members_with_points())
        target_mobject_family_members = set(self.target_mobject.family_members_with_points())

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
                if get_original_id(mobject) == submobject_id:
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

        # Exclude animations that animate submobjects of other FadeIn animations
        for outer_mob_animtion in self.fading_in_animations.copy():
            outer_mob = outer_mob_animtion.mobject
            for inner_mob_animation in self.fading_in_animations.copy():
                inner_mob = inner_mob_animation.mobject
                # Exclude self by excluding first element from slice
                if inner_mob in outer_mob.family_members_with_points()[1:]:
                    self.fading_in_animations.remove(inner_mob_animation)

        super().__init__(*(self.transform_animations + self.fading_out_animations + self.fading_in_animations))

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)

        for fade_in_animation in self.fading_in_animations:
            # TODO CUR-3: Change to ``Scene.remove``
            scene.mobjects[0].remove(fade_in_animation.mobject)

        # TODO CUR-3: Figure out what mobjects stay and go and what need to stay and go
        scene.remove(self.mobject, self.target_mobject)
        scene.add(self.ungroupified_mobject)

        # Apply all methods to self.mobject so it catches up to target in appearance
        for method, method_args, method_kwargs in self.methods:
            method.__func__(self.ungroupified_mobject, *method_args, **method_kwargs)
