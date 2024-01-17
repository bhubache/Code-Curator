from __future__ import annotations

from pathlib import Path

import yaml

from .components.animation_script.animation_stream import AnimationStream
from code_curator.custom_logging.custom_logger import CustomLogger


logger = CustomLogger.getLogger(__name__)


class LeetcodeYAMLParser:
    def __init__(self, script_path):
        self._script_path = Path(script_path)
        self._wait_animation_prefix = "_IMPLICIT_WAIT_"

    def parse(self) -> dict:
        animation_script: dict = self._get_file_contents()
        animation_stream_map: dict[str, AnimationStream] = {
            "Video": AnimationStream(name="Video"),
        }

        start_is_here = False

        for stream in animation_stream_map.values():
            for animation_func_name, text in animation_script.items():
                if animation_func_name == "__START__":
                    start_is_here = True
                    continue

                stream.append(
                    text=text,
                    is_overriding_start=False,
                    is_overriding_end=False,
                    name=animation_func_name,
                )

                if start_is_here:
                    start_is_here = False
                    stream.entries[-1]["start_here"] = True

        return animation_stream_map

    def _get_file_contents(self) -> dict:
        with self._script_path.open() as read_yaml:
            return yaml.safe_load(read_yaml)
