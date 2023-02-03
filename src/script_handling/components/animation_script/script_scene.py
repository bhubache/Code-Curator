from .script_section import ScriptSection
from ..alignment_script.alignments.aligned_script import AlignedScript
from .script_order import ScriptOrder

from typing import Iterable

class ScriptScene:
    def __init__(self, scene_id: str, text: str, section_keys: Iterable[str]):
        self._scene_id = scene_id
        self._text = text
        self._sections = [ScriptSection(section_key, self._get_section_text(section_key, text)) for section_key in section_keys]
        self._num_words = sum([section.num_words for section in self._sections])

    def __str__(self):
        return '\n'.join([str(section) for section in self._sections])

    @property
    def scene_id(self):
        return self._scene_id

    @property
    def num_words(self):
        return self._num_words

    def get_section(self, section_id):
        for section in self._sections:
            if section.section_id == section_id: return section
        return None

    def get_order(self, section_id: str, order_id: str) -> ScriptOrder:
        return self.get_section(section_id).get_order(order_id)

    def apply_alignments(self, aligned_script: AlignedScript, word_count_start: int):
        for section in self._sections:
            section.apply_alignments(aligned_script.get_words_from_to(start=word_count_start, end=word_count_start + section.num_words - 1), word_count_start=word_count_start)
            word_count_start += section.num_words

    def get_animation_timings(self):
        timing_info = {}
        for section in self._sections:
            timing_info[section.section_id] = section.get_animation_timings()
        return timing_info

    def _get_section_text(self, section_key, scene_text):
        '''
        Gets the text for a particular section within a scene
        '''
        scene_lines = scene_text.splitlines()

        if section_key not in scene_lines: return ''
        start_index = scene_lines.index(section_key) + 1
        end_index = start_index
        for index in range(start_index, len(scene_lines)):
            if scene_lines[index].strip() == '':
                end_index = index
                break
            elif index == len(scene_lines) - 1:
                end_index = len(scene_lines)
                break
        return '\n'.join(scene_lines[start_index : end_index]).strip()
    