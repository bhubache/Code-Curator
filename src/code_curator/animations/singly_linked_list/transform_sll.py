from __future__ import annotations

from typing import TYPE_CHECKING

from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut
from manim import Mobject
from manim import Transform

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList


class TransformSinglyLinkedList(AnimationGroup):
    def __init__(self, mobject: SinglyLinkedList, target_mobject: SinglyLinkedList, **kwargs) -> None:
        self.length_change: int = len(target_mobject) - len(mobject)

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

        short_node = next(iter(self.shorter_list))
        for long_node in self.longer_list:
            if short_node.value == long_node.value:
                if self.length_change < 0:
                    self.matching_submobject_pairs.append((long_node, short_node))
                    self.matching_submobject_pairs.append((long_node.next_pointer, short_node.next_pointer))

                if self.length_change > 0:
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
            list(original_labeled_line_labels - target_labeled_line_labels),
        )
        self.submobjects_to_fade_in.extend(
            list(target_labeled_line_labels - original_labeled_line_labels),
        )

        for label in original_labeled_line_labels.intersection(target_labeled_line_labels):
            self.matching_submobject_pairs.append(
                (mobject.labeled_pointers[label], target_mobject.labeled_pointers[label]),
            )

        animations: list[Animation] = []
        for submobject in self.submobjects_to_fade_out:
            animations.append(FadeOut(submobject))

        for submobject in self.submobjects_to_fade_in:
            animations.append(FadeIn(submobject))

        for submobject, target_submobject in self.matching_submobject_pairs:
            animations.append(Transform(submobject, target_submobject))

        super().__init__(*animations)
