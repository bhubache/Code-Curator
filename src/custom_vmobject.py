from __future__ import annotations

from custom_logging.custom_logger import CustomLogger
from manim import VMobject
from manim.constants import DEFAULT_STROKE_WIDTH
from null_vmobject import NullVMobject
logger = CustomLogger.getLogger(__name__)


class CustomVMobject(VMobject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    # def __getattr__(self, name):
    #     try:
    #         value = super().__getattr__(name)
    #     except AttributeError as e:
    #         # print(e)
    #         # value =
    #         print(e)
    #         raise AttributeError()
    #     else:
    #         return value

    def add(self, *mobjects: VMobject) -> None:
        non_null_vmobjects: list[VMobject] = []
        for mob in mobjects:
            if mob is None:
                raise Exception(
                    f'Can\'t add NoneType to submobjects: {mobjects}',
                )
            elif isinstance(mob, VMobject) and not isinstance(mob, NullVMobject):
                non_null_vmobjects.append(mob)
        super().add(*non_null_vmobjects)

    @property
    def stroke_width(self) -> int:
        return DEFAULT_STROKE_WIDTH

    @stroke_width.setter
    def stroke_width(self, _: int) -> None:
        pass
