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
            opacity=0.5,
        )

        scene.add(code)
