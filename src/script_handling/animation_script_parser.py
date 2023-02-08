from __future__ import annotations
from abc import ABC, abstractmethod
import re

class AnimationScriptParser(ABC):
    def __init__(self, script_path: str):
        self._script_path:        str  = script_path
        self._start_scene_pattern: str = '<<([^\/].*)>>'
        self._end_scene_pattern: str = '<<\/(.*)>>'
        self._start_scene_format: str = '<<{}>>'
        self._end_scene_format: str = '<</{}>>'

        self._section_split = '\n\n'
        self._section_pattern = '<(.*)>'

    @abstractmethod
    def parse(self) -> AnimationScriptParser:
        pass

    def _get_file_contents(self) -> str:
        '''
        Returns string contents from text file
        '''
        contents = None
        with open(self._script_path, 'r', encoding='UTF-8') as read_file:
            contents = read_file.read()
        return contents

    def _is_starting_scene_line(self, line: str) -> bool:
        match = re.search(pattern=self._start_scene_pattern, string=line)
        return match is not None

    def get_scene_text(self, start_scene_line: str, file_contents: str) -> str:
        full_scene_pattern = fr'{start_scene_line.strip()}(.*){self._get_end_scene_line(start_scene_line)}'
        return re.search(pattern=full_scene_pattern, string=file_contents, flags=re.DOTALL).group(1).strip()

    def get_section_animation_chunks(self, section: str) -> str:
        if self._is_explicit_animation_section(section):
            return [line for i, line in enumerate(section.splitlines()) if i != 0]
        return [line for line in section.splitlines()]

    def _get_end_scene_line(self, start_scene_line: str) -> str:
        return self._end_scene_format.format(self.get_scene_name_from_start_line(start_scene_line))

    def get_scene_name_from_start_line(self, start_scene_line: str) -> str:
        return re.search(
            pattern=self._start_scene_pattern,
            string=start_scene_line).group(1).strip()

    def _is_explicit_animation_section(self, section: str) -> bool:
        first_line = section.splitlines()[0]
        
        if re.search(pattern=self._section_pattern, string=first_line) is None:
            return False
        return True

    # TODO: Make this and the way it's done with scene the same to reduce confusion
    def _get_animation_section_name(self, section: str) -> str:
        first_line = section.splitlines()[0]
        
        return re.search(pattern=self._section_pattern, string=first_line).group(1).strip()