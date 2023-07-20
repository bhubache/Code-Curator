from __future__ import annotations

import yaml

from code_curator.custom_logging.custom_logger import CustomLogger

from .animation_script_parser import AnimationScriptParser
from .components.animation_script.animation_leaf import AnimationLeaf
from .components.animation_script.composite_animation_script import CompositeAnimationScript
logger = CustomLogger.getLogger(__name__)

# TODO
# Make exceptions/assertions to enforce formatting of animation script


class LeetcodeYAMLParser(AnimationScriptParser):
    def __init__(self, script_path):
        super().__init__(script_path=script_path)
        self._wait_animation_prefix = '_IMPLICIT_WAIT_'

    def parse(self) -> CompositeAnimationScript:
        scene_map = self._get_file_contents()
        import json
        print(json.dumps(scene_map, indent=4, default=str))

        composite_animation_script = self._create_composite_animation_script(
            scene_map,
        )

        return composite_animation_script

    def _get_file_contents(self):
        with open(self._script_path, 'r') as read_yaml:
            return yaml.safe_load(read_yaml)

    def _create_composite_animation_script(self, animation_script_map: dict) -> CompositeAnimationScript:
        composite_scenes = []
        for scene_name, section_map in animation_script_map.items():
            composite_sections = []
            for section_name, section_info in section_map.items():

                is_wait_animation = section_name.startswith(self._wait_animation_prefix)
                if isinstance(section_info, str):
                    composite_sections.append(
                        AnimationLeaf(
                            unique_id=section_name,
                            text=section_info,
                            is_wait_animation=is_wait_animation,
                            tags=(),
                        )
                    )
                else:
                    composite_sections.append(
                        CompositeAnimationScript(
                            unique_id=section_name,
                            children=[
                                AnimationLeaf(
                                    unique_id=f'{section_name}_{key}',
                                    text=value,
                                    is_wait_animation=is_wait_animation,
                                    tags=(),
                                )
                                for key, value in section_info.items()
                            ]
                        )
                    )

            composite_scenes.append(
                CompositeAnimationScript(
                    unique_id=scene_name, children=[
                        composite for composite in composite_sections
                    ],
                ),
            )

        script_composite = CompositeAnimationScript(
            unique_id='script', children=[composite for composite in composite_scenes],
        )

        # Recurively adds parents (this uses @property)
        script_composite.parent = None

        print(script_composite)

        return script_composite
