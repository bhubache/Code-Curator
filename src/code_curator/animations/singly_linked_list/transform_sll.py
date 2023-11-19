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
        self.length_change: int = len(target_mobject) - len(mobject)
        self.kwargs = kwargs

        self.mobject = mobject
        self.target_mobject = target_mobject
        self.submobjects_to_fade_out = []
        self.submobjects_to_fade_in = []
        self.matching_submobject_pairs: list[tuple[Mobject, Mobject]] = []

        # If the lengths are the same, we cannot rely on output of min/max because they will choose arbitrarily
        if self.length_change == 0:
            self.shorter_list = mobject
            self.longer_list = target_mobject
        else:
            self.shorter_list = min(mobject, target_mobject, key=len)
            self.longer_list = max(mobject, target_mobject, key=len)

        # TODO: Seprate handling of nodes and pointers
        short_node = next(iter(self.shorter_list))
        for long_node in self.longer_list:
            if short_node.value == long_node.value:
                if self.length_change < 0:
                    self.matching_submobject_pairs.append((long_node, short_node))
                    self.matching_submobject_pairs.append((long_node.next_pointer, short_node.next_pointer))
                else:
                    self.matching_submobject_pairs.append((short_node, long_node))
                    self.matching_submobject_pairs.append((short_node.next_pointer, long_node.next_pointer))

                try:
                    short_node = next(self.shorter_list)
                except StopIteration:
                    break
            else:
                if self.length_change < 0:
                    self.submobjects_to_fade_out.append(long_node)
                    self.submobjects_to_fade_out.append(long_node.next_pointer)
                elif self.length_change > 0:
                    self.submobjects_to_fade_in.append(long_node)
                    self.submobjects_to_fade_in.append(long_node.next_pointer)
                else:
                    raise NotImplementedError("The node's value has changed")

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
