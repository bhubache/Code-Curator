from __future__ import annotations

from collections.abc import Sequence

from custom_logging.custom_logger import CustomLogger
from manim import VMobject
from manim.constants import DEFAULT_STROKE_WIDTH
from null_vmobject import NullVMobject
logger = CustomLogger.getLogger(__name__)


def disregard_temp_submobjects(func):
    def inner(self, *args, **kwargs):
        # temp_mobj_map: dict = {}
        if self._is_temp():
            raise Exception('self is temp!')

        mobj_copy = self.copy()

        def disregard_temps(mobj):
            for sub in mobj.submobjects:
                try:
                    if sub.is_temp():
                        mobj.remove(sub)
                    else:
                        disregard_temps(sub)
                except AttributeError:
                    disregard_temps(sub)

        disregard_temps(mobj_copy)
        return func(mobj_copy, *args, **kwargs)
    return inner


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

    def _is_temp(self) -> bool:
        return False

    @disregard_temp_submobjects
    def get_left(self) -> Sequence[float]:
        return super().get_left()

    @disregard_temp_submobjects
    def get_right(self) -> Sequence[float]:
        return super().get_right()

    @disregard_temp_submobjects
    def get_top(self) -> Sequence[float]:
        return super().get_top()

    @disregard_temp_submobjects
    def get_bottom(self) -> Sequence[float]:
        return super().get_bottom()

    @disregard_temp_submobjects
    def get_center(self) -> Sequence[float]:
        return super().get_center()

    def make_temp(self) -> CustomVMobject:
        """
        The presence of a submobject that is temporary
        is not taken into consideration when getting
        the relative locations of the parent mobject
        or when moving the parent mobject.
        """
        self._is_temp = lambda: True
        return self

    # def move_to(
    #     self,
    #     point_or_mobject,
    #     aligned_edge=ORIGIN,
    #     coor_mask=np.array([1, 1, 1]),
    # ):
    #     """Move center of the :class:`~.Mobject` to certain coordinate."""
    #     if isinstance(point_or_mobject, Mobject):
    #         target = point_or_mobject.get_critical_point(aligned_edge)
    #     else:
    #         target = point_or_mobject

    #     # mobj_copy = self.copy()
    #     def disregard_temps(mobj):
    #         for sub in mobj.submobjects:
    #             try:
    #                 if 'custom' == sub._label._value:
    #                     print(sub._is_temp())
    #             except Exception:
    #                 pass
    #             try:
    #                 if sub._is_temp():
    #                     print(f'removing {sub}')
    #                     mobj.remove(sub)
    #                 else:
    #                     disregard_temps(sub)
    #             except AttributeError:
    #                 disregard_temps(sub)
    #     disregard_temps(self)
    #     point_to_align = self.get_critical_point(aligned_edge)
    #     self.shift((target - point_to_align) * coor_mask)
    #     return self

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
