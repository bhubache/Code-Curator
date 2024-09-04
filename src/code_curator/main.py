"""Starting point for the creation of a video.

You can either create a video using custom scenes or test some animation code!
"""
from __future__ import annotations

__all__: Sequence[str] = []

import argparse
import importlib
import logging
import os
import yaml
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from manim import config
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import CompositeAudioClip

from code_curator import ai_audio_creator
from code_curator.script_handling.aligned_animation_script import AlignedAnimationScript
from code_curator.alignment_text_creation import alignment_text_creator
from code_curator.script_handling.components.alignment_script.alignments.alignment_parser import (
    AlignmentParser,
)
from code_curator.script_handling.simple_script_parser_factory import (
    SimpleScriptParserFactory,
)


if TYPE_CHECKING:
    from code_curator.base_scene import BaseScene
    from types import ModuleType


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_aligned_animation_script(
    alignment_path: str | os.PathLike,
    script_path: str | os.PathLike,
) -> AlignedAnimationScript:
    aligned_script = AlignmentParser(file_path=alignment_path).parse()
    script_parser_factory = SimpleScriptParserFactory(script_path=script_path)
    animation_script = script_parser_factory.create_script_parser(
        "leetcode",
    ).parse()
    return AlignedAnimationScript(
        aligned_script=aligned_script,
        animation_script=animation_script,
    )


def get_video_and_stream_clses(
    module_import_path: str,
    aligned_animation_script,
) -> Sequence[type]:
    video_module: ModuleType = importlib.import_module(module_import_path)
    if video_module.__file__ is None:
        raise TypeError(f"file for {video_module} is None.")

    return (
        getattr(
            video_module,
            "Video",
        )
        # [
        #     *(
        #         getattr(
        #             video_module,
        #             stream_name,
        #         )
        #         for stream_name in aligned_animation_script.stream_names
        #     ),
        # ],
    )


def _prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ai_audio", help="generate AI audio from script", action="store_true")
    parser.add_argument(
        "--quality",
        help="resolution and frame rate of video",
        choices=("low", "medium", "high"),
        default="low",
    )
    parser.add_argument("--video_path", help="dotted path to video module to render", required=True)
    parser.add_argument("--pdb", help="enter pdb upon program exit due to unhandled exception", action="store_true")
    parser.add_argument("--test", help="Render test scene", action="store_true")
    args = parser.parse_args()

    QUALITY_MAP = {
        "fourk_quality": None,
        "production_quality": None,
        "high_quality": {
            "frame_rate": 60,
            "res": 1080,
        },
        "medium_quality": {
            "frame_rate": 30,
            "res": 720,
        },
        "low_quality": {
            "frame_rate": 15,
            "res": 480,
        },
    }

    config["quality"] = f"{args.quality}_quality"
    # frame_rate = config["frame_rate"]
    # resolution = config["pixel_height"]
    # ALIGNED_SCRIPT_PATH = Path("ai_aligned_script.txt")
    # ANIMATION_SCRIPT_PATH = Path("animation_script.yaml")
    # CONCRETE_VIDEO_SCRIPT_PATH = f"code_curator.videos.interview_problems.{PROBLEM_NAME}.video"

    return args


def _main(args):
    animation_script_path = Path(Path(__file__).parent, "videos", *args.video_path.split("."), "animation_script.yaml")

    animation_script_map = yaml.safe_load(animation_script_path.read_text())

    script_text = " ".join(text for text in animation_script_map.values() if text is not None).strip()

    if args.ai_audio:
        logger.debug("AI speech requested")

        audio_path = ai_audio_creator.create_audio(script_text)

    else:
        raise NotImplementedError("Use of non-AI audio is not yet supported")

    aligned_script_path = alignment_text_creator.create_alignment_text(
        script_text=script_text,
        audio_path=audio_path,
    )

    aligned_animation_script = get_aligned_animation_script(
        alignment_path=aligned_script_path,
        script_path=animation_script_path,
    )
    video_cls = get_video_and_stream_clses(
        module_import_path=f"code_curator.videos.{args.video_path}.video",
        aligned_animation_script=aligned_animation_script,
    )

    video_instance = video_cls(animation_script=aligned_animation_script)

    # def get_attr(self, attr_name: str):
    #     return getattr(video_instance, attr_name)
    #
    # for stream_cls in stream_clses:
    #     stream_cls.__get_attr__ = get_attr
    #     video_instance.__dict__[stream_cls.__name__] = stream_cls

    video_instance.render()
    # create_scenes(
    #     scene_classes, problem_dir,
    #     aligned_animation_script.get_scenes(),
    # )

    # Combine video and audio together!
    video_clip = VideoFileClip(
        str(
            Path(
                Path.cwd() / "media",
                "videos",
                f"{config['pixel_height']}p{config['frame_rate']}",
                "Video.mp4",
            ),
        ),
    )

    audio_clip = AudioFileClip(str(audio_path))
    final_clip = video_clip.set_audio(
        CompositeAudioClip([audio_clip.set_start(aligned_animation_script.run_time - audio_clip.duration)]),
    )
    final_clip.write_videofile(
        str(Path(Path.home(), "Videos", "FULL_VIDEO.mp4")),
        fps=config["frame_rate"],
    )


def main() -> None:
    args = _prepare_args()
    try:
        if args.test:
            TestVideo().render()
        else:
            _main(args)
    except Exception:
        if args.pdb:
            import pdb

            pdb.post_mortem()
        else:
            raise


def postmortem_main(args):
    try:
        _main(args)
    except Exception:
        import pdb

        pdb.post_mortem()


from manim import config
from code_curator.animations.curator_animation import CuratorAnimation
from code_curator.base_scene import BaseScene
from code_curator.data_structures.stack import Stack
from code_curator.code.curator_code import CuratorCode
from code_curator.data_structures.singly_linked_list import SinglyLinkedList
from code_curator.code.curator_code import add, remove
from code_curator.animations.composition import CuratorAnimationGroup, CuratorSuccession
from code_curator.data_structures.stack import Stack

from manim import *
from manim import RoundedRectangle

def set_start_time(start_time: float):
    def inner(fn):
        fn.start_time = start_time
        return fn

    return inner



class TestVideo(BaseScene):
    def __init__(self) -> None:
        class TestAnimationScript:
            def __init__(self) -> None:
                self.entries = []

        animation_script = TestAnimationScript()
        animation_script.run_time = 6

        excluded_attr_names = "construct"

        for attr_name, func in type(self).__dict__.items():
            if attr_name in excluded_attr_names or (attr_name.startswith("__") and attr_name.endswith("__")):
                continue

            try:
                start_time = func.start_time
            except AttributeError:
                start_time = 0.0

            animation_script.entries.append(
                {
                    "name": func.__name__,
                    "start_time": start_time,
                },
            )

        super().__init__(animation_script)

    def construct(self) -> None:
        self.play(
            CuratorAnimation(
                self.mobjects[0],
                animation_script=self.animation_script,
                scene=self,
                run_time=self.animation_script.run_time,
            ),
        )

    def first_animation(self):
        self.first_recursive_solution_code = CuratorCode(
            code="\n".join(
                (
                    "class Solution:",
                    "    def reverseList(self, head):",
                    "        if head is None or head.next is None:",
                    "            return head",
                    "",
                    "        reverseList(head.next)",
                ),
            ),
        ).add_highlighter(1)

        # self.add(self.first_recursive_solution_code)

        new_code_string = "\n".join(
            (
                "class Solution:",
                "    def reverseList(self, head):",
                "        if head is None or head.next is None:",
                "            return head",
                add("# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"),
                "        reverseList(head.next)",
            ),
        )

        self.black_box_before_call = Rectangle().move_to((3, 3, 0))
        self.four_node_linked_list = SinglyLinkedList.create_sll(0, 1, 2, 3).add_head_pointer().add_null().scale(0.75)
        # self.add(self.four_node_linked_list)

        self.pondering_rectangle = Rectangle().move_to((-2, 2, 0))

        self.two_node_sll = SinglyLinkedList.create_sll(0, 1).add_null()
        self.two_node_sll.add_labeled_pointer(self.two_node_sll.head, "head")
        # self.add(self.two_node_sll)
        self.call_stack = Stack(4, 2, BLACK)
        # self.add(self.call_stack)


        # return (
        #     # FadeIn(self.black_box_before_call),
        #     # FadeIn(self.two_node_sll),
        #     self.two_node_sll.animate.move_to((1, 1, 0)),
        #     # FadeIn(Circle())
        # )

        # return (
        #     FadeIn(self.black_box_before_call),
        #     FadeOut(self.four_node_linked_list),
        #     # FadeIn(Circle())
        #     # FadeIn(self.two_node_sll),
        #     FadeIn(self.two_node_sll.move_to(self.pondering_rectangle).scale(0.75)),
        #     self.call_stack.animate.push("reverseList(0)"),
        # )
        self.heads_original_next_node = self.two_node_sll.get_next(self.two_node_sll.head)

        # return FadeIn(self.two_node_sll.move_to(self.pondering_rectangle).scale(0.75))
        breakpoint()

        return CuratorSuccession(
            # self.call_stack.animate.push("reverseList(0)"),
            # self.call_stack.animate.push("reverseList(1)"),
            # CuratorAnimationGroup(
            #     # self.call_stack.animate.push("reverseList(0)"),
            #     # self.first_recursive_solution_code.animate.move_highlighter_to_line(3),
            # ),
            # CuratorAnimationGroup(
            #     # self.call_stack.animate.push("reverseList(1)"),
            #     # self.first_recursive_solution_code.animate.move_highlighter_to_line(5),
            # ),
            # self.call_stack.animate.push("reverseList(0)"),
            # self.call_stack.animate.push("reverseList(1)"),

            FadeIn(self.two_node_sll.move_to(self.pondering_rectangle).scale(0.75)),

            # CuratorAnimationGroup(
            #     # self.first_recursive_solution_code.animate.change_source_code(
            #     #     new_code_string=new_code_string,
            #     #     saturate_edits=False,
            #     # ),
            #     # self.first_recursive_solution_code.animate.move_highlighter_to_line(2),
            #     # FadeIn(self.black_box_before_call),
            #     # FadeOut(self.four_node_linked_list),
            #     # FadeIn(self.two_node_sll.move_to(self.pondering_rectangle).scale(0.75)),
            #      #self.call_stack.animate.push("reverseList(0)")
            # ),
            # CuratorAnimationGroup(
            #     self.first_recursive_solution_code.animate.move_highlighter_to_line(3),
            # ),
            # CuratorAnimationGroup(
            #     # self.two_node_sll.animate.move_labeled_pointer("head", self.two_node_sll.get_next(self.two_node_sll.head)),
            #     # self.call_stack.animate.push("reverseList(1)"),
            #     self.first_recursive_solution_code.animate.move_highlighter_to_line(5),
            # ),
            self.two_node_sll.animate.set_next(self.two_node_sll.head, self.two_node_sll.null, angle_in_degrees=90),
            # CuratorSuccession(
            #     self.two_node_sll.animate.set_next(self.two_node_sll.head, self.heads_original_next_node, angle_in_degrees=90),
            # ),
            # CuratorAnimationGroup(
                # self.two_node_sll.animate.move_labeled_pointer("head", self.two_node_sll.get_next(self.two_node_sll.head)),
                # self.call_stack.animate.push("reverseList(1)"),
                # self.first_recursive_solution_code.animate.move_highlighter_to_line(2),
            # )
            # AnimationGroup(
            #     self.two_node_sll.animate.move_labeled_pointer("head", self.two_node_sll.get_next(self.two_node_sll.get_next(self.two_node_sll.head))),
            #     self.call_stack.animate.push("reverseList(1)"),
            #     self.first_recursive_solution_code.animate.move_highlighter_to_line(3),
            # ),
        )

    # @set_start_time(1)
    # def animation_two(self):
    #     return self.two_node_sll.animate.set_next(self.two_node_sll.head, self.two_node_sll.null, angle_in_degrees=90)

    # @set_start_time(1)
    # def animation_two(self):
    #     # self.two_node_sll.animate.move_labeled_pointer("head", self.two_node_sll.get_next(self.two_node_sll.head))
    #     # return self.two_node_sll.animate.set_next(self.two_node_sll.head, self.two_node_sll.null, angle_in_degrees=90)
    #     return self.first_recursive_solution_code.animate.move_highlighter_to_line(3)

    # @set_start_time(2)
    # def animation_three(self):
    #     return self.first_recursive_solution_code.animate.move_highlighter_to_line(5)

    # @set_start_time(1)
    # def animation_four(self):
    #     self.heads_original_next_node = self.two_node_sll.get_next(self.two_node_sll.head)
    #     return self.two_node_sll.animate.set_next(self.two_node_sll.head, self.two_node_sll.null, angle_in_degrees=90)

    # @set_start_time(2)
    # def animation_five(self):
    #     ...
    #     # return self.two_node_sll.animate.move_to((1, 1, 0))

    # @set_start_time(3)
    # def animation_six(self):
    #     return self.two_node_sll.animate.set_next(self.two_node_sll.head, self.heads_original_next_node)
    #   # return self.two_node_sll.animate.move_labeled_pointer("head", self.heads_original_next_node)

    # @set_start_time(4)
    # def animation_seven(self):
    #     return (
    #         self.two_node_sll.animate.move_labeled_pointer("head", self.heads_original_next_node),
    #         self.call_stack.animate.push("reverseList(1)"),
    #         self.first_recursive_solution_code.animate.move_highlighter_to_line(2),
    #     )


if __name__ == "__main__":
    # main()
    TestVideo().render()
