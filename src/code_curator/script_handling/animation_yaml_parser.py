from __future__ import annotations

import yaml
from collections.abc import Mapping

from code_curator.custom_logging.custom_logger import CustomLogger
from .animation_script_parser import AnimationScriptParser
from .components.animation_script.animation_script import AnimationScript
from .components.animation_script.animation_leaf import AnimationLeaf
from .components.animation_script.composite_animation_script import CompositeAnimationScript
from .components.animation_script.animation_stream import AnimationStream


logger = CustomLogger.getLogger(__name__)

# TODO
# Make exceptions/assertions to enforce formatting of animation script


class LeetcodeYAMLParser(AnimationScriptParser):
    def __init__(self, script_path):
        super().__init__(script_path=script_path)
        self._wait_animation_prefix = '_IMPLICIT_WAIT_'

    def parse(self) -> dict:
        animation_script: dict = self._get_file_contents()
        animation_stream_map: dict[str, AnimationStream] = {
            "Video": AnimationStream(name="Video")
        }

        # Collect all stream names
        # for element in animation_script["content"]:
        #     try:
        #         element["word"]
        #     except TypeError:
        #         continue
        #     except KeyError as exc:
        #         raise ValueError(f"Stream missing word entry") from exc
        #     else:
        #         animation_stream_map.update({name: AnimationStream(name=name) for name in element.keys()})

        # "word" is not a stream name
        # del animation_stream_map["word"]

        for stream_name, stream in animation_stream_map.items():
            stream_gap_words: list[str] = []
            for element in animation_script["content"]:
                if isinstance(element, str):
                    stream_gap_words += element.strip().split()
                else:
                    if stream_gap_words:
                        stream.append(text=" ".join(stream_gap_words))
                        stream_gap_words = []

                    stream.append(
                        text=element["word"],
                        is_overriding_start=element.get("is_overriding_start", False),
                        is_overriding_end=element.get("is_overriding_end", False),
                        name=element["name"],
                    )

            if stream_gap_words:
                stream.append(text=" ".join(stream_gap_words))

        # # Change stream names to their aliases
        # for stream_name, stream in animation_stream_map.copy().items():
        #     # A different stream cannot have another stream's alias
        #     if stream_name in animation_stream_map.values():
        #         raise ValueError(f"The stream name {stream_name} conflicts with the alias of another stream")

        #     animation_stream_map[stream_num_to_class_name_map[stream_name]] = stream
        #     del animation_stream_map[stream_name]

        return animation_stream_map

    def _get_file_contents(self) -> dict:
        with open(self._script_path, 'r') as read_yaml:
            return yaml.safe_load(read_yaml)
