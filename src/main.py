from manim import *
import importlib
import os
import time

from leetcode.script_scene import ScriptScene

from leetcode.aligned_script import AlignedScript
from leetcode.aligned_animation_script import AlignedAnimationScript

from leetcode.alignment_parser import AlignmentParser
from leetcode.script_parser import ScriptParser

from typing import Iterable

# To open the movie after render.
from manim.utils.file_ops import open_file as open_media_file

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PROBLEM_NAME = 'Delete_Node_in_a_Linked_List'

def create_class(*bases):
    class MyScene(*bases):
        # config.disable_caching = True

        def __init__(self, problem_dir, aligned_animation_script):
            self._video_dir = r'C:\Users\brand\Documents\ManimCS\media\videos\1080p60'
            self._classes = bases
            for cls in self._classes:
                cls.__init__(self, problem_dir=problem_dir, aligned_animation_script=aligned_animation_script)

        def setup(self):
            pass

        def construct(self):
            for cls in self._classes:
                cls.setup(self)
                cls.construct(self)
                cls.tear_down(self)

        def tear_down(self):
            pass

    return MyScene


def get_scene_classes():
    scene_classes = []
    present_problem_module = importlib.import_module(f'leetcode.problems.{PROBLEM_NAME}.present_problem')
    present_problem_cls = getattr(present_problem_module, 'PresentProblem')
    problem_dir = os.path.split(present_problem_module.__file__)[0]
    # scene_classes.append(present_problem_cls)

    problem_analysis_module = importlib.import_module(f'leetcode.problems.{PROBLEM_NAME}.problem_analysis')
    problem_analysis_cls = getattr(problem_analysis_module, 'ProblemAnalysis')
    scene_classes.append(problem_analysis_cls)
    
    # FIXME: Bad practice returning a tuple with loosely understood ordering
    return scene_classes, problem_dir

def get_aligned_animation_script(alignment_path: str, script_path: str):
    aligned_script = AlignmentParser(alignment_path=alignment_path).parse()
    parsed_script = ScriptParser(script_path=script_path).parse()
    parsed_script.apply_alignments(aligned_script)
    return parsed_script

def create_scenes(scene_classes: list, problem_dir: str, aligned_animation_scene_scripts: Iterable[dict]):
    for index, (cls, script_scene) in enumerate(zip(scene_classes, aligned_animation_scene_scripts)):
        # scene = create_class(cls)(problem_dir=problem_dir, aligned_animation_script=script_scene)
        scene = create_class(cls)(problem_dir=problem_dir, aligned_animation_script=script_scene)
        scene.render()
        _give_scene_ordered_name(scene, index)

def _give_scene_ordered_name(scene_instance, index):
    old_file_path = os.path.join(scene_instance._video_dir, f'{scene_instance.__class__.__name__}.mp4')
    new_file_path = os.path.join(scene_instance._video_dir, f'{index}.mp4')

    if os.path.exists(new_file_path):
        os.remove(new_file_path)

    os.rename(old_file_path, new_file_path)

def _get_animation_timing_iterable(aligned_animation_script: AlignedAnimationScript) -> Iterable[dict]:
    animation_timings_list = []
    for timing_info in aligned_animation_script.get_animation_timings().values():
        animation_timings_list.append(timing_info)
    return animation_timings_list


if __name__ == '__main__':
    scene_classes, problem_dir = get_scene_classes()
    aligned_animation_script = get_aligned_animation_script(
        alignment_path=os.path.join(problem_dir, 'generated/aligned_script.txt'),
        script_path=os.path.join(problem_dir, 'required/script.txt')
        )
    # create_scenes(scene_classes, problem_dir, _get_animation_timing_iterable(aligned_animation_script))
    create_scenes(scene_classes, problem_dir, [_get_animation_timing_iterable(aligned_animation_script)[1]])

    aligned_animation_script.print_animation_timings()

    # open_media_file(scene.renderer.file_writer.movie_file_path)