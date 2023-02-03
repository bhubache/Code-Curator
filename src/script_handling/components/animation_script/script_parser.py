# from .script_section import ScriptSection
import re
import importlib
from .script_scene import ScriptScene
from ..alignment_script.alignments.aligned_script import AlignedScript
from .aligned_animation_script import AlignedAnimationScript

class ScriptParser:
    def __init__(self, script_path: str):
        self._script_path = script_path
        self._scenes = []

        self._present_problem_key = 'Present_Problem'
        self._present_problem_pattern_pair = {
            'start': '<Present_Problem>',
            'end': '</Present_Problem>'
        }
        self._constraints_analysis_patten_pair = {
            'start': '<Constraints_Analysis>',
            'end': '</Constraints_Analysis>'
        }

        self._present_problem_sections_keys = [
            '<title>',
            '<statement_header>',
            '<statement>',
            '<constraints_header>',
            '<constraints>'
        ]

        # FIXME: This is bad! It will change if this module is moved.. which it probably will be
        script_path_parts = self._script_path.split('\\')
        index = script_path_parts.index('src') + 1
        important_module = importlib.import_module(f'{script_path_parts[index]}.{script_path_parts[index + 1]}.{script_path_parts[index + 2]}.scenes.problem_analysis')
        num_constraint_explanations = len(important_module.EXPLANATIONS)

        self._constraints_analysis_section_keys = [
            '<intro>',
            *[f'<explanation_{i + 1}>' for i in range(num_constraint_explanations)]
        ]

    def parse(self):
        self._scenes.append(
            ScriptScene(
                scene_id=self._present_problem_pattern_pair['start'],
                text=self._get_scene_text(self._present_problem_pattern_pair),
                section_keys=self._present_problem_sections_keys
            )
        )

        self._scenes.append(
            ScriptScene(
                scene_id=self._constraints_analysis_patten_pair['start'],
                text=self._get_scene_text(self._constraints_analysis_patten_pair),
                section_keys=self._constraints_analysis_section_keys
            )
        )

        return AlignedAnimationScript(scenes=self._scenes)

    # def get_timed_script_animations(self, aligned_script: AlignedScript):
    #     pass

    def get_scene(self, scene_id: str) -> ScriptScene:
        for scene in self._scenes:
            if scene.scene_id == scene_id: return scene
        return None


    def _get_scene_text(self, pattern_pair):
        '''
        Gets the text for a particular scene
        '''
        pattern = fr"{pattern_pair['start']}(.*){pattern_pair['end']}"
        scene_text = None
        with open(self._script_path, 'r', encoding='UTF-8') as script_file:
            full_script_text = script_file.read()
            scene_text = re.search(pattern=pattern, string=full_script_text, flags=re.DOTALL).group(1).strip()
        return scene_text