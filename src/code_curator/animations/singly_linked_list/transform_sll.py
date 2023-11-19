from __future__ import annotations

from typing import TYPE_CHECKING

from manim import Animation
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
        self.num_node_difference: int = len(target_mobject) - len(mobject)
        self.submobjects_to_fade_out = []
        self.submobjects_to_fade_in = []
        self.matching_submobject_pairs: list[tuple[Mobject, Mobject]] = []
        self.mobject = mobject
        self.target_mobject = target_mobject

        # If the lengths are the same, we cannot rely on output of min/max because they will choose arbitrarily
        if self.num_node_difference == 0:
            self.shorter_list = mobject
            self.longer_list = target_mobject
        else:
            self.shorter_list = min(mobject, target_mobject, key=len)
            self.longer_list = max(mobject, target_mobject, key=len)

        short_node = next(iter(self.shorter_list))
        for long_node in self.longer_list:
            if short_node.value == long_node.value:
                if self.num_node_difference < 0:
                    self.matching_submobject_pairs.append((long_node, short_node))
                else:
                    self.matching_submobject_pairs.append((short_node, long_node))

                try:
                    short_node = next(self.shorter_list)
                except StopIteration:
                    break
            else:
                if self.num_node_difference < 0:
                    self.submobjects_to_fade_out.append(long_node)
                elif self.num_node_difference > 0:
                    self.submobjects_to_fade_in.append(long_node)
                else:
                    raise NotImplementedError("The node's value has changed")

        self.num_pointer_difference = len(target_mobject.pointers) - len(mobject.pointers)

        if self.num_pointer_difference == 0:
            self.shorter_pointer_list = mobject.pointers
            self.longer_pointer_list = target_mobject.pointers
        else:
            self.shorter_pointer_list = min(mobject.pointers, target_mobject.pointers, key=len)
            self.longer_pointer_list = max(mobject.pointers, target_mobject.pointers, key=len)

        short_pointer_index: int = 0
        for long_pointer in self.longer_pointer_list:
            # TODO: Account for vertex being None
            short_pointer = self.shorter_pointer_list[short_pointer_index]
            pointers_match = any(
                (
                    short_pointer.vertex_one is None
                    and long_pointer.vertex_one is None
                    and short_pointer.vertex_two.value == long_pointer.vertex_two.value,
                    short_pointer.vertex_two is None
                    and long_pointer.vertex_two is None
                    and short_pointer.vertex_one.value == long_pointer.vertex_one.value,
                    short_pointer.vertex_one.value == long_pointer.vertex_one.value
                    and short_pointer.vertex_two.value == long_pointer.vertex_two.value,
                ),
            )
            if pointers_match:
                if self.num_pointer_difference < 0:
                    self.matching_submobject_pairs.append((long_pointer, short_pointer))
                else:
                    self.matching_submobject_pairs.append((short_pointer, long_pointer))

                short_pointer_index += 1
            else:
                if self.num_pointer_difference < 0:
                    self.submobjects_to_fade_out.append(long_pointer)
                elif self.num_pointer_difference > 0:
                    self.submobjects_to_fade_in.append(long_pointer)
                else:
                    self.matching_submobject_pairs.append((short_pointer, long_pointer))
                    short_pointer_index += 1

        original_labeled_line_labels = set(mobject.labeled_pointers.keys())
        target_labeled_line_labels = set(target_mobject.labeled_pointers.keys())
        self.submobjects_to_fade_out.extend(
            [
                self.mobject.labeled_pointers[label]
                for label in list(original_labeled_line_labels - target_labeled_line_labels)
            ],
        )
        self.submobjects_to_fade_in.extend(
            [
                self.target_mobject.labeled_pointers[label]
                for label in list(target_labeled_line_labels - original_labeled_line_labels)
            ],
        )

        for label in original_labeled_line_labels.intersection(target_labeled_line_labels):
            mobject.labeled_pointers[label].suspend_updating()
            target_mobject.labeled_pointers[label].suspend_updating()
            self.matching_submobject_pairs.append(
                (mobject.labeled_pointers[label], target_mobject.labeled_pointers[label]),
            )

        animations: list[Animation] = []
        for submobject in self.submobjects_to_fade_out:
            animations.append(FadeOut(submobject))

        for submobject in self.submobjects_to_fade_in:
            animations.append(FadeIn(submobject))

        # FIXME: There's a pair of None??? Perhaps one of the vertices of an edge wasn't set
        for submobject, target_submobject in self.matching_submobject_pairs:
            animations.append(Transform(submobject, target_submobject))

        super().__init__(*animations)

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
