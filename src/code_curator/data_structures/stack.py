from __future__ import annotations

from typing import Any
from typing import Self
from typing import TYPE_CHECKING

from manim import Animation
from manim import config
from manim import DOWN
from manim import Rectangle
from manim import Text
from manim import UP
from manim.mobject.mobject import _AnimationBuilder

from code_curator.animations.singly_linked_list.transform_sll import TransformSinglyLinkedList
from code_curator.custom_vmobject import CustomVMobject

if TYPE_CHECKING:
    from manim import ParsableManimColor


class Stack(CustomVMobject):
    def __init__(self, height: float, width: float, color: ParsableManimColor, **kwargs) -> None:
        super().__init__(**kwargs)

        self.rectangle = Rectangle(
            height=height,
            width=width,
            color=color,
        )
        self.stack: list[StackElement] = []

        self.add(self.rectangle)

    @property
    def animate(self) -> AnimationBuilder:
        return AnimationBuilder(self)

    def push(self, obj: Any, /) -> Self:
        top_element = StackElement(
            str(obj),
            height=self.height * 0.1,
            width=self.width * 0.90,
            color=self.rectangle.color,
            fill_color=self.rectangle.color,
            fill_opacity=1,
            stroke_width=self.rectangle.stroke_width / 2,
        )

        self.stack.append(top_element)

        try:
            top_element.next_to(self.stack[-2], UP, buff=0.1)
        except IndexError:
            top_element.move_to(self.rectangle)
            top_element.align_to(self.rectangle, DOWN)
            top_element.shift(UP * 0.1)

        self.add(top_element)

        return self

    def pop(self) -> Self:
        self.remove(self.stack.pop())
        return self


class StackElement(CustomVMobject):
    def __init__(self, text: str, /, height: float, width: float, color, **kwargs) -> None:
        super().__init__(**kwargs)
        self.rectangle = Rectangle(
            height=height,
            width=width,
            color=color,
            **kwargs,
        )
        self.text = text
        self.text_mobject = Text(self.text, width=width * 0.65, color=config["background_color"]).move_to(
            self.rectangle.get_center(),
        )

        self.rectangle.add(self.text_mobject)

        self.add(self.rectangle)


class AnimationBuilder(_AnimationBuilder):
    def build(self) -> Animation:
        if self.overridden_animation:
            anim = self.overridden_animation
        else:
            anim = TransformSinglyLinkedList(self.mobject, self.methods)

        for attr, value in self.anim_args.items():
            setattr(anim, attr, value)

        return anim
