"""Starting point for the creation of a video.

You can either create a video using custom scenes or test some animation code!
"""

from __future__ import annotations

__all__: Sequence[str] = []

import importlib
import logging
import os
import subprocess
import yaml
from collections.abc import Iterable
from collections.abc import Mapping
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip

from code_curator.ai_audio_creator import AIAudioCreator
from code_curator.script_handling.aligned_animation_script import AlignedAnimationScript
from code_curator.alignment_text_creation.alignment_text_creator import AlignmentTextCreator
from code_curator.script_handling.components.alignment_script.alignments.alignment_parser import AlignmentParser
from code_curator.script_handling.simple_script_parser_factory import SimpleScriptParserFactory


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


QUALITY = 'low_quality'
FRAME_RATE = QUALITY_MAP[QUALITY]["frame_rate"]
RESOLUTION = QUALITY_MAP[QUALITY]["res"]
PROBLEM_NAME = 'Delete_Node_in_a_Linked_List'
ALIGNED_SCRIPT_PATH = Path('generated_files', 'ai_aligned_script.txt')
ANIMATION_SCRIPT_PATH = Path('required_files', 'animation_script.yaml')
CONCRETE_VIDEO_SCRIPT_PATH = f"code_curator.leetcode.problems.{PROBLEM_NAME}.required_files.video"


def concatenate_scenes(video_dir: str, num_scenes: int) -> None:
    scene_video_paths = [
        VideoFileClip(
            os.path.join(
                video_dir, f'{str(i)}.mp4',
            ),
        ) for i in range(num_scenes)
    ]
    final_clip = concatenate_videoclips(scene_video_paths)
    final_clip.write_videofile(os.path.join(video_dir, 'output.mp4'))


def get_aligned_animation_script(alignment_path: str | os.PathLike, script_path: str | os.PathLike) -> AlignedAnimationScript:
    aligned_script = AlignmentParser(file_path=alignment_path).parse()
    script_parser_factory = SimpleScriptParserFactory(script_path=script_path)
    animation_script = script_parser_factory.create_script_parser(
        'leetcode',
    ).parse()
    return AlignedAnimationScript(
        aligned_script=aligned_script,
        animation_script=animation_script,
    )


def _give_scene_ordered_name(scene_instance: BaseScene, index: int) -> None:
    old_file_path = Path(
        scene_instance.video_dir,
        f'{type(scene_instance).__name__}.mp4',
    )
    new_file_path = Path(
        scene_instance.video_dir,
        f'{index}.mp4',
    )

    new_file_path.unlink()

    subprocess.getoutput(f'mv {old_file_path} {new_file_path}')
    subprocess.getoutput(f'chmod 777 {new_file_path}')


def get_video_and_stream_clses(module_import_path: str, aligned_animation_script) -> Sequence[type]:
    video_module: ModuleType = importlib.import_module(module_import_path)
    if video_module.__file__ is None:
        raise TypeError(f'file for {video_module} is None.')

    return (
        getattr(
            video_module,
            "Video",
        ),
        [
            *(
                getattr(
                    video_module,
                    stream_name,
                )
                for stream_name in aligned_animation_script.stream_names
            )
        ]
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
    generate_ai_speech: bool = True
    problem_dir = Path(
        Path.home(),
        "ManimCS",
        "Code_Curator",
        "src",
        "code_curator",
        "leetcode",
        "problems",
        "Delete_Node_in_a_Linked_List",
    )

    if generate_ai_speech:
        # Generate ai_script.txt from the animation script
        ai_script_path: Path = problem_dir / 'dev_files' / 'MFA' / 'input' / 'ai_script.txt'

        script = get_script_text_from_animation_script(
            yaml.safe_load(
                (problem_dir / ANIMATION_SCRIPT_PATH).read_text()
            )
        )
        ai_script_path.write_text(script)

        # with open(ai_script_path, 'w', encoding='UTF-8') as write_file:
        #     write_file.write(script)

        # Generate audio from text
        audio_path: Path = AIAudioCreator.create_audio(ai_script_path)
        ALIGNED_SCRIPT_PATH = AlignmentTextCreator.create_alignment_text(problem_dir / 'dev_files')



    aligned_animation_script = get_aligned_animation_script(
        alignment_path=problem_dir/ALIGNED_SCRIPT_PATH,
        script_path=problem_dir/ANIMATION_SCRIPT_PATH,
    )
    video_cls, stream_clses = get_video_and_stream_clses(
        module_import_path=CONCRETE_VIDEO_SCRIPT_PATH,
        aligned_animation_script=aligned_animation_script,
    )

    video_instance = video_cls(aligned_animation_script, stream_clses)

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
        str(Path(Path.cwd() / 'media', 'videos', f'{RESOLUTION}p{FRAME_RATE}', 'Video.mp4'))
    )
    audio_clip = AudioFileClip(str(audio_path))
    final_clip: VideoFileClip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(str(Path(Path.home(), 'Videos', 'FULL_VIDEO.mp4')), fps=FRAME_RATE)


def postmortem_main():
    try:
        main()
    except Exception:
        import pdb; pdb.post_mortem()



if __name__ == '__main__':
    main()
