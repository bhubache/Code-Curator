"""Starting point for the creation of a video.

You can either create a video using custom scenes or test some animation code!
"""
from __future__ import annotations

__all__: Sequence[str] = []

import sys
sys.path.insert(0, "/".join(sys.path[0].split("/")[:-1]))

import importlib
import logging
import os
import subprocess
import yaml
from collections.abc import Mapping
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip

from code_curator.ai_audio_creator import AIAudioCreator
from code_curator.script_handling.aligned_animation_script import AlignedAnimationScript
from code_curator.alignment_text_creation.alignment_text_creator import (
    AlignmentTextCreator,
)
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


QUALITY = "low_quality"
FRAME_RATE = QUALITY_MAP[QUALITY]["frame_rate"]
RESOLUTION = QUALITY_MAP[QUALITY]["res"]
PROBLEM_NAME = "Delete_Node_in_a_Linked_List"
ALIGNED_SCRIPT_PATH = Path("generated_files", "ai_aligned_script.txt")
ANIMATION_SCRIPT_PATH = Path("required_files", "animation_script.yaml")
CONCRETE_VIDEO_SCRIPT_PATH = f"code_curator.leetcode.problems.{PROBLEM_NAME}.required_files.video"


def concatenate_scenes(video_dir: str, num_scenes: int) -> None:
    scene_video_paths = [
        VideoFileClip(
            os.path.join(
                video_dir,
                f"{str(i)}.mp4",
            ),
        )
        for i in range(num_scenes)
    ]
    final_clip = concatenate_videoclips(scene_video_paths)
    final_clip.write_videofile(os.path.join(video_dir, "output.mp4"))


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


def _give_scene_ordered_name(scene_instance: BaseScene, index: int) -> None:
    old_file_path = Path(
        scene_instance.video_dir,
        f"{type(scene_instance).__name__}.mp4",
    )
    new_file_path = Path(
        scene_instance.video_dir,
        f"{index}.mp4",
    )

    new_file_path.unlink()

    subprocess.getoutput(f"mv {old_file_path} {new_file_path}")
    subprocess.getoutput(f"chmod 777 {new_file_path}")


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


def get_script_text_from_animation_script(animation_script_info: Mapping) -> str:
    script_text = ""
    animation_spec: list[str | Mapping[str | int, str]] = animation_script_info["content"]
    for element in animation_spec:
        try:
            script_text += f" {element['word']}"
        except TypeError:
            script_text += f" {element}"

    return script_text.strip()


def main() -> None:
    ai_speech_requested = True
    problem_dir = Path(
        Path.home(),
        "ManimCS",
        "Code-Curator",
        "src",
        "code_curator",
        "leetcode",
        "problems",
        "Delete_Node_in_a_Linked_List",
    )

    # if ai_speech_requested:
    #     script_text = get_script_text_from_animation_script(
    #         yaml.safe_load(
    #             (problem_dir / ANIMATION_SCRIPT_PATH).read_text(),
    #         ),
    #     )

    #     ai_script_path = Path("/tmp", "curator", "MFA", "input", "ai_script.txt")
    #     ai_script_path.parent.mkdir(parents=True, exist_ok=True)
    #     ai_script_path.write_text(script_text)

    #     audio_path: Path = AIAudioCreator.create_audio(ai_script_path)
    #     ALIGNED_SCRIPT_PATH = AlignmentTextCreator.create_alignment_text(
    #         ai_script_path.parents[2],
    #     )

    aligned_animation_script = get_aligned_animation_script(
        alignment_path=problem_dir / ALIGNED_SCRIPT_PATH,
        script_path=problem_dir / ANIMATION_SCRIPT_PATH,
    )
    video_cls = get_video_and_stream_clses(
        module_import_path=CONCRETE_VIDEO_SCRIPT_PATH,
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
                f"{RESOLUTION}p{FRAME_RATE}",
                "Video.mp4",
            ),
        ),
    )
    # audio_clip = AudioFileClip(str(audio_path))
    # final_clip: VideoFileClip = video_clip.set_audio(audio_clip)
    # final_clip.write_videofile(
    #     str(Path(Path.home(), "Videos", "FULL_VIDEO.mp4")),
    #     fps=FRAME_RATE,
    # )


def postmortem_main():
    try:
        main()
    except Exception:
        import pdb

        pdb.post_mortem()


from manim import Scene
from manim import config
from manim import FadeIn
from manim import Circle
from manim import Square
from code_curator.animations.curator_animation_new import CuratorAnimation
from code_curator.utils.testing.curator_frames_comparison import starts_at
from code_curator.base_scene import BaseScene
from manim import Rotate
from manim import FadeOut


class TestVideo(BaseScene):
    def __init__(self) -> None:
        class TestAnimationScript:
            def __init__(self) -> None:
                self.entries = []

        animation_script = TestAnimationScript()
        animation_script.run_time = 1.5

        excluded_attr_names = ("construct")


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
            )
        )

    def first_animation(self):
        square = Square().move_to((1, 1, 0))
        self.add(square)

        return FadeOut(square)

    @starts_at(0.5)
    def second_animation(self):
        return FadeIn(Circle())


if __name__ == "__main__":
    main()
    # TestVideo().render()
