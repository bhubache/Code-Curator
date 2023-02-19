from __future__ import annotations
from .animation_script_parser import AnimationScriptParser
from .components.animation_script.composite_animation_script import CompositeAnimationScript
from .components.animation_script.animation_leaf import AnimationLeaf

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# TODO
# Make exceptions/assertions to enforce formatting of animation script

class LeetcodeScriptParser(AnimationScriptParser):
    def __init__(self, script_path):
        super().__init__(script_path=script_path)
        self._wait_animation_prefix = '_IMPLICIT_WAIT_'

    def parse(self) -> LeetcodeScriptParser:
        contents = self._get_file_contents()

        scene_map = self._get_scene_map(file_contents=contents)

        animation_parsed_map = {}
        for scene_name, scene_text in scene_map.items():
            animation_parsed_map[scene_name] = self._get_scene_animation_sections(scene_name, scene_text)

        composite_animation_script = self._create_composite_animation_script(animation_parsed_map)

        return composite_animation_script

    def _get_scene_animation_sections(self, scene_name: str, scene_text: str) -> dict:
        section_map = {}
        sections = scene_text.split(self._section_split)
        wait_animation_index = 0
        for section in sections:
            section_name = None
            if not self._is_explicit_animation_section(section):
                section_name = f'{self._wait_animation_prefix}{wait_animation_index}'
                wait_animation_index += 1
            else:
                section_name = self._get_animation_section_name(section)
            section_map[section_name] = self.get_section_animation_chunks(section)

        return section_map

    def _get_scene_map(self, file_contents: str) -> dict:
        scene_map = {}
        for line in file_contents.splitlines():
            if not self._is_starting_scene_line(line): continue

            scene_name = self.get_scene_name_from_start_line(line)
            scene_map[scene_name] = self.get_scene_text(start_scene_line=line, file_contents=file_contents)
        return scene_map

    def _create_composite_animation_script(self, animation_script_map: dict) -> CompositeAnimationScript:
        composite_animation_script = None
        composite_scenes = []
        for scene_name, section_map in animation_script_map.items():
            composite_sections = []
            for section_name, section_info in section_map.items():
                animation_lines = section_info['animation_lines']
                tags = section_info['tags']
                assert len(animation_lines) > 0, 'Every section should have at least one animation'


                if len(animation_lines) == 1:
                    # Leaf
                    is_wait_animation = False
                    if section_name.startswith(self._wait_animation_prefix):
                        is_wait_animation = True
                    composite_sections.append(AnimationLeaf(unique_id=section_name, text=animation_lines[0], is_wait_animation=is_wait_animation, tags=tags))
                else:
                    # Composite)
                    composite_sections.append(
                        CompositeAnimationScript(
                            unique_id=section_name,
                            children=[AnimationLeaf(unique_id=f'{section_name}_{i}', text=line, is_wait_animation=False, tags=tags) for i, line in enumerate(animation_lines)]
                        )
                    )

            composite_scenes.append(CompositeAnimationScript(unique_id=scene_name, children=[composite for composite in composite_sections]))

        script_composite = CompositeAnimationScript(unique_id='script', children=[composite for composite in composite_scenes])

        # Recurively adds parents (this uses @property)
        script_composite.parent = None

        return script_composite

            
        