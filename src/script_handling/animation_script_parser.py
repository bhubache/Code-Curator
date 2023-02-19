from __future__ import annotations
from abc import ABC, abstractmethod
import re


from .tag import Tag

class AnimationScriptParser(ABC):
    def __init__(self, script_path: str):
        self._script_path:        str  = script_path
        self._start_scene_pattern: str = '<<([^\/].*)>>'
        self._end_scene_pattern: str = '<<\/(.*)>>'
        self._start_scene_format: str = '<<{}>>'
        self._end_scene_format: str = '<</{}>>'

        self._section_split = '\n\n'
        self._section_pattern = '<(.*)>'
        self._name_tag_separator = ':'

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
        animation_chunks = {
            'animation_lines': [],
            'tags': []
        }
        if self._is_explicit_animation_section(section):
            animation_chunks['animation_lines'] = [line for i, line in enumerate(section.splitlines()) if i != 0]
            animation_chunks['tags'] = self._get_animation_section_tags(section)
            # return [line for i, line in enumerate(section.splitlines()) if i != 0]
        else:
            animation_chunks['animation_lines'] = [line for line in section.splitlines()]
        return animation_chunks
        # return [line for line in section.splitlines()]

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

    # FIXME: Duplicate code with _get_animation_section_tags
    # TODO: Make this and the way it's done with scene the same to reduce confusion
    def _get_animation_section_name(self, section: str) -> str:
        first_line = section.splitlines()[0]

        name_with_tags = re.search(pattern=self._section_pattern, string=first_line).group(1).strip()

        name = name_with_tags.split(self._name_tag_separator)[0]
        
        return name

    def _get_animation_section_tags(self, section: str) -> list[str]:
        first_line = section.splitlines()[0]

        name_with_tags = re.search(pattern=self._section_pattern, string=first_line).group(1).strip()

        if len(name_with_tags.split(self._name_tag_separator)) == 1: return []

        tags_str_form = name_with_tags.split(self._name_tag_separator)[1].split(',')

        tags_enum_form = []
        for tag_str in tags_str_form:
            if tag_str == 'code_timing': tags_enum_form.append(Tag.CODE_TIMING)
            else:
                raise ValueError(f'{tag_str} is not a valid tag')
        
        return tags_enum_form