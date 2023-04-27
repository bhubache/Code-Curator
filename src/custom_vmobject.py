from __future__ import annotations

from manim import VMobject

from src.custom_logging.custom_logger import CustomLogger
from src.null_vmobject import NullVMobject
logger = CustomLogger.getLogger(__name__)


class CustomVMobject(VMobject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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
