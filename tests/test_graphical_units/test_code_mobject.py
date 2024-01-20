from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

import pytest
from manim import YELLOW

from code_curator.code.curator_code import CuratorCode
from code_curator.utils.testing.curator_frames_comparison import curator_frames_comparison

if TYPE_CHECKING:
    from code_curator.base_scene import BaseScene

__module_test__ = "code_mobject"


@pytest.fixture
def default_code_kwargs() -> dict[str, Any]:
    return {
        "file_name": None,
        "tab_width": 1,
        "indentation_chars": " ",
        "font": "Monospace",
        "font_size": 24,
        "stroke_width": 0,
        "margin": 0.1,
        "background": None,
        "background_stroke_width": 0,
        "background_stroke_color": "#FFFFFF",
        "corner_radius": 0,
        "insert_line_no": False,
        "line_spacing": 0.6,
        "line_no_buff": 0.2,
        "style": "vim",
        "language": "python",
        "background_color": None,
    }


@curator_frames_comparison
@pytest.mark.parametrize(
    "highlighter_start_line",
    (
        1,
        2,
        3,
        4,
    ),
)
class test_highlighter:
    def __init__(self, scene: BaseScene, default_code_kwargs: dict[str, Any], highlighter_start_line: int) -> None:
        default_code_kwargs["code"] = "\n".join(
            (
                "class ListNode:",
                "    def __init__(self, val=0, next=None):",
                "        self.val = val",
                "        self.next = next",
            ),
        )
        code = CuratorCode(**default_code_kwargs)
        code.add_highlighter(
            start_line=highlighter_start_line,
            color=YELLOW,
            opacity=0.2,
            height_buff=0.05,
            width_buff=0.1,
        )

        scene.add(code)


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    ("start_line", "stop_line"),
    (
        (1, 2),
        (1, 3),
        (4, 2),
        (3, 3),
    ),
)
class test_moving_highlighter_from_line_to_line:
    def __init__(self, scene: BaseScene, default_code_kwargs: dict[str, Any], start_line: int, stop_line: int) -> None:
        default_code_kwargs["code"] = "\n".join(
            (
                "class ListNode:",
                "",
                "    def __init__(self, val=0, next=None):",
                "        self.val = val",
                "        self.next = next",
            ),
        )
        self.code = CuratorCode(**default_code_kwargs)
        self.code.add_highlighter(
            start_line=start_line,
            color=YELLOW,
            opacity=0.5,
            height_buff=0.05,
            width_buff=0.1,
        )

        scene.add(self.code)

        self.stop_line = stop_line

    def animation(self):
        return self.code.animate.move_highlighter_to_line(self.stop_line)


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    ("start_line", "substring", "occurrence"),
    (
        (1, "next", 1),
        (1, "val", 2),
        (4, "val", 2),
    ),
)
class test_moving_highlighter_from_line_to_substring:
    def __init__(
        self,
        scene: BaseScene,
        default_code_kwargs: dict[str, Any],
        start_line: int,
        substring: str,
        occurrence: int,
    ) -> None:
        default_code_kwargs["code"] = "\n".join(
            (
                "class ListNode:",
                "",
                "    def __init__(self, val=0, next=None):",
                "        self.val = val",
                "        self.next = next",
            ),
        )
        self.code = CuratorCode(**default_code_kwargs)
        self.code.add_highlighter(
            start_line=start_line,
            color=YELLOW,
            opacity=0.5,
            height_buff=0.05,
            width_buff=0.1,
        )

        scene.add(self.code)

        self.substring = substring
        self.occurrence = occurrence

    def animation(self):
        return self.code.animate.move_highlighter_to_substring(substring=self.substring, occurrence=self.occurrence)


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    ("start_substring", "start_occurrence", "stop_substring", "stop_occurrence"),
    (("next", 1, "ListNode", 1),),
)
class test_moving_highlighter_from_substring_to_substring:
    def __init__(
        self,
        scene: BaseScene,
        default_code_kwargs: dict[str, Any],
        start_substring: str,
        start_occurrence: int,
        stop_substring: str,
        stop_occurrence: int,
    ) -> None:
        default_code_kwargs["code"] = "\n".join(
            (
                "class ListNode:",
                "",
                "    def __init__(self, val=0, next=None):",
                "        self.val = val",
                "        self.next = next",
            ),
        )
        self.code = CuratorCode(**default_code_kwargs)
        self.code.add_highlighter(
            start_line=1,
            color=YELLOW,
            opacity=0.5,
            height_buff=0.05,
            width_buff=0.1,
        )

        scene.add(self.code)

        self.code.move_highlighter_to_substring(
            substring=start_substring,
            occurrence=start_occurrence,
        )

        self.stop_substring = stop_substring
        self.stop_occurrence = stop_occurrence

    def animation(self):
        return self.code.animate.move_highlighter_to_substring(
            substring=self.stop_substring,
            occurrence=self.stop_occurrence,
        )


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    ("start_substring", "start_occurrence", "end_line_num"),
    (("next", 1, 1),),
)
class test_moving_highlighter_from_substring_to_line:
    def __init__(
        self,
        scene: BaseScene,
        default_code_kwargs: dict[str, Any],
        start_substring: str,
        start_occurrence: int,
        end_line_num: int,
    ) -> None:
        default_code_kwargs["code"] = "\n".join(
            (
                "class ListNode:",
                "",
                "    def __init__(self, val=0, next=None):",
                "        self.val = val",
                "        self.next = next",
            ),
        )
        self.code = CuratorCode(**default_code_kwargs)
        self.code.add_highlighter(
            start_line=1,
            color=YELLOW,
            opacity=0.5,
            height_buff=0.05,
            width_buff=0.1,
        )

        scene.add(self.code)

        self.code.move_highlighter_to_substring(
            substring=start_substring,
            occurrence=start_occurrence,
        )

        self.end_line_num = end_line_num

    def animation(self):
        return self.code.animate.move_highlighter_to_line(self.end_line_num)
