from __future__ import annotations

from .animation_script_parser import AnimationScriptParser
from .leetcode_script_parser import LeetcodeScriptParser
from .animation_yaml_parser import LeetcodeYAMLParser


class SimpleScriptParserFactory:
    def __init__(self, script_path: str):
        self._script_path = script_path

    def create_script_parser(self, parser_type: str) -> AnimationScriptParser:
        animation_script_parser: AnimationScriptParser = None

        if parser_type.lower() == 'leetcode':
            # animation_script_parser = LeetcodeScriptParser(
            #     script_path=self._script_path,
            # )
            animation_script_parser = LeetcodeYAMLParser(
                script_path=self._script_path,
            )
        else:
            raise NotImplementedError(f'{parser_type} is not supported')

        return animation_script_parser
