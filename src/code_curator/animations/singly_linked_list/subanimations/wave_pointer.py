from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from code_curator.animations.utils import math_
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
# from code_curator.data_structures.nodes.singly_linked_list_node import SLLNode
from code_curator.data_structures.pointers.pointer import Pointer
from manim import Dot
from manim import Line
from manim import smooth

from .leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


class WavePointer(LeafSubanimation):
    def __init__(
        self,
        sll: SinglyLinkedList,
        pointer: Pointer,
        run_time: float = 1.0,
        num_waves: int = 1,
    ) -> None:
        super().__init__(sll, run_time=run_time)
        self._pointer: Pointer = pointer
        self._max_angle: float = 30.0
        self._wave_angle_calc = WaveAngleCalculator(max_angle=self._max_angle, num_waves=num_waves)

    def begin(self) -> None:
        self._sll.add(self._pointer)
        self._pointer.save_state()
        # self._path = Line(start=self._pointer.end, start=self._pointer.start)

    def interpolate(self, alpha: float) -> None:
        self._pointer.restore()
        rotation_angle: float = self._alpha_to_angle(alpha)

        pointer_start, pointer_end = self._pointer.get_start_and_end()
        new_pointer_end = Dot(pointer_end).rotate(
            angle=rotation_angle,
            about_point=pointer_start,
        ).get_center()
        self._pointer.put_start_and_end_on(
            pointer_start,
            new_pointer_end,
        )

    def clean_up_from_animation(self) -> None:
        super().clean_up_from_animation()

    # NOTE: This will probably need a different successive counterpart implementation
    def create_successive_counterpart(self) -> LeafSubanimation:
        return WavePointer(
            self._sll,
            self._pointer,
        )

    def _alpha_to_angle(self, alpha: float) -> float:
        angle_in_degrees = self._wave_angle_calc.calculate_angle(smooth(alpha))
        return math_.degrees_to_radians(angle_in_degrees)


class WaveAngleCalculator:
    def __init__(self, max_angle: float, num_waves: int = 1) -> None:
        self.max_angle = max_angle
        self.num_waves = num_waves

        initial_alpha_lower_bounds = [val for val in np.linspace(0.0, 1.0, num=(4 * self.num_waves) + 1)]
        self.alpha_lower_bounds = initial_alpha_lower_bounds + [initial_alpha_lower_bounds[1] + initial_alpha_lower_bounds[-1]]

        self.angle_lower_bounds: list[float] = ([0, self.max_angle, 0, -self.max_angle] * self.num_waves) + [0, self.max_angle]

    def calculate_angle(self, alpha: float) -> float:
        (input_start, input_end), (output_start, output_end) = self._get_range_mappings(alpha)

        return (alpha - input_start) / (input_end - input_start) * (output_end - output_start) + output_start

    def _get_range_mappings(self, alpha: float) -> tuple[tuple[float, float], tuple[float, float]]:
        for i, alpha_lower_bound in enumerate(self.alpha_lower_bounds):
            if alpha < alpha_lower_bound:
                return (
                    (self.alpha_lower_bounds[i - 1], self.alpha_lower_bounds[i]),
                    (self.angle_lower_bounds[i - 1], self.angle_lower_bounds[i]),
                )
        else:
            raise ValueError(f'Unexpected alpha ``{alpha}`` for WavePointer animation')
