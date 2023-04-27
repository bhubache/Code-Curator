from __future__ import annotations

from manim import Line
from manim import smooth

from .leaf_subanimation import LeafSubanimation
from .strictly_successive.flatten_tail import SuccessiveFlattenTail
from src.custom_logging.custom_logger import CustomLogger
from src.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from src.data_structures.nodes.singly_linked_list_node import SLLNode
logger = CustomLogger.getLogger(__name__)


class FlattenTail(LeafSubanimation):
    def __init__(self, sll, index: int, added_node: SLLNode):
        super().__init__(sll)
        self._index: int = index
        self._added_node: SLLNode = added_node

        self._added_node_original_start = None
        self._container_path = None

    def begin(self):
        self._added_node_original_start = self._added_node.container.get_center()
        self._container_path = Line(
            start=self._added_node_original_start,
            end=self._sll_post_subanimation_group[-1].container.get_center(),
        )

    def interpolate(self, alpha: float):
        self._added_node.container.move_to(
            self._container_path.point_from_proportion(smooth(alpha)),
        )

        self._sll[self._index - 1].pointer_to_next.become(
            SinglyDirectedEdge(
                start=self._sll[self._index - 1].get_container_right(),
                end=self._added_node.get_container_left(),
            ),
        )

        # def rotate_start():
        #     start = self._added_node.get_container_top()
        #     curr_x = start[0]
        #     curr_y = start[1]

        #     origin_x, origin_y, _ = self._added_node.get_container_center()
        #     angle = -(math.pi / 2 * smooth(alpha))
        #     sine = math.sin(angle)
        #     cosine = math.cos(angle)

        #     new_x = origin_x + cosine * (curr_x - origin_x) - sine * (curr_y - origin_y)
        #     new_y = origin_y - sine * (curr_x - origin_x) + cosine * (curr_y - origin_y)
        #     return [new_x, new_y, 0]

        # def rotate_end():
        #     # FIXME: Hardcoded bottom of container
        #     curr_x, curr_y, _ = self._sll[self._index + 1].get_container_bottom()

        #     angle = -(math.pi / 2 * smooth(alpha))
        #     sine = math.sin(angle)
        #     cosine = math.cos(angle)

        #     origin_x, origin_y, _ = self._sll[self._index + 1].get_container_center()
        #     curr_x = curr_x - origin_x
        #     curr_y = curr_y - origin_y

        #     new_x = curr_x * cosine - curr_y * sine
        #     new_y = curr_x * sine + curr_y * cosine

        #     new_x += origin_x
        #     new_y += origin_y
        #     return [new_x, new_y, 0]

        # Move next pointer on node being inserted
        # self._added_node.pointer_to_next.become(
        #     SinglyDirectedEdge(
        #         start=rotate_start(),
        #         end=rotate_end()
        #     )
        # )

    def clean_up_from_animation(self):
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveFlattenTail(self._sll, self._index, self._added_node)
