import importlib
import os
import time

from base_scene import BaseScene
from script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript

from script_handling.simple_script_parser_factory import SimpleScriptParserFactory
from script_handling.aligned_animation_script import AlignedAnimationScript

from script_handling.components.alignment_script.alignments.alignment_parser import AlignmentParser

from typing import Iterable

# To open the movie after render.
from manim.utils.file_ops import open_file as open_media_file
from manim import *

from moviepy.editor import VideoFileClip, concatenate_videoclips

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PROBLEM_NAME = 'Delete_Node_in_a_Linked_List'

ALIGNED_SCRIPT_PATH = r'generated_files\aligned_script.txt'
ANIMATION_SCRIPT_PATH = r'required_files\animation_script.txt'

CONCRETE_PRESENT_PROBLEM_PATH = f'leetcode.problems.{PROBLEM_NAME}.scenes.present_problem'
CONCRETE_PROBLEM_ANALYSIS_PATH = f'leetcode.problems.{PROBLEM_NAME}.scenes.problem_analysis'
CONCRETE_CODE_SOLUTION_PATH = f'leetcode.problems.{PROBLEM_NAME}.scenes.code_solution'

def create_class(scene_classes: list[BaseScene], aligned_animation_scene_scripts: list[CompositeAnimationScript]):
    class MyScene(Scene):
        # config.disable_caching = True

        def __init__(self, problem_dir: str):
            super().__init__()
            self._video_dir = r'C:\Users\brand\Documents\ManimCS\media\videos\1080p60'
            self._scene_instances = []
            for cls, scene_script in zip(scene_classes, aligned_animation_scene_scripts):
                scene_inst = cls(problem_dir, scene_script)
                scene_inst.video_dir = self._video_dir
                self._scene_instances.append(scene_inst)

        def setup(self):
            pass

        def construct(self):
            for i, scene_inst in enumerate(self._scene_instances):
                # Only calling render seems to get the video to save
                scene_inst.render()
                _give_scene_ordered_name(scene_inst, i)

        def tear_down(self):
            pass

    return MyScene


def get_scene_classes():
    scene_classes = []
    present_problem_module = importlib.import_module(CONCRETE_PRESENT_PROBLEM_PATH)
    present_problem_cls = getattr(present_problem_module, 'PresentProblem')
    problem_dir = '\\'.join(present_problem_module.__file__.split('\\')[:-2])
    scene_classes.append(present_problem_cls)

    problem_analysis_module = importlib.import_module(CONCRETE_PROBLEM_ANALYSIS_PATH)
    problem_analysis_cls = getattr(problem_analysis_module, 'ProblemAnalysis')
    scene_classes.append(problem_analysis_cls)

    code_solution_module = importlib.import_module(CONCRETE_CODE_SOLUTION_PATH)
    code_solution_cls = getattr(code_solution_module, 'CodeSolution')
    # scene_classes.append(code_solution_cls)
    
    # FIXME: Bad practice returning a tuple with loosely understood ordering
    return scene_classes, problem_dir

def concatenate_scenes(video_dir, num_scenes):
    scene_video_paths = [VideoFileClip(os.path.join(video_dir, f'{str(i)}.mp4')) for i in range(num_scenes)]
    final_clip = concatenate_videoclips(scene_video_paths)
    final_clip.write_videofile(os.path.join(video_dir, 'output.mp4'))

def get_aligned_animation_script(alignment_path: str, script_path: str):
    aligned_script = AlignmentParser(file_path=alignment_path).parse()
    script_parser_factory = SimpleScriptParserFactory(script_path=script_path)
    animation_script = script_parser_factory.create_script_parser('leetcode').parse()
    aligned_animation_script = AlignedAnimationScript(aligned_script=aligned_script, animation_script=animation_script)
    return aligned_animation_script

def create_scenes(scene_classes: list[BaseScene], problem_dir: str, aligned_animation_scene_scripts: Iterable[CompositeAnimationScript]):
    scene = create_class(scene_classes, aligned_animation_scene_scripts)(problem_dir)
    scene.render()

    concatenate_scenes(scene._video_dir, len(scene_classes))

def _give_scene_ordered_name(scene_instance, index):
    old_file_path = os.path.join(scene_instance.video_dir, f'{scene_instance.__class__.__name__}.mp4')
    new_file_path = os.path.join(scene_instance.video_dir, f'{index}.mp4')

    if os.path.exists(new_file_path):
        os.remove(new_file_path)

    os.rename(old_file_path, new_file_path)

def _get_animation_timing_iterable(aligned_animation_script) -> Iterable[dict]:
    animation_timings_list = []
    for timing_info in aligned_animation_script.get_animation_timings().values():
        animation_timings_list.append(timing_info)
    return animation_timings_list

class TestScene(Scene):
    config.disable_caching = True
    def construct(self):
        from data_structures.singly_linked_list.singly_linked_list import SinglyLinkedList
        sll = SinglyLinkedList(1, 2, 3, 4)
        print(self.mobjects)
        print()
        self.play(FadeIn(sll))
        for sub in sll.submobjects:
            print(sub.submobjects)

        # self.play(sll.add_first(-10, num_animations=2))
        # self.wait(0.5)
        self.play(sll.add_first(-2, num_animations=2))
        self.wait(0.5)
        self.play(sll.remove_first(num_animations=2))
        self.wait(0.5)
        self.play(sll.add_first(-101, num_animations=2))
        self.wait(0.5)
        self.play(sll.remove_first(num_animations=2))
        self.wait(0.5)
        self.play(sll.add_first(-101, num_animations=2))
        self.wait(0.5)
        self.play(sll.remove_first(num_animations=2))
        self.wait(0.5)
        self.play(sll.add_first(-101, num_animations=2))
        self.wait(0.5)
        self.play(sll.remove_first(num_animations=2))
        self.wait(0.5)
        self.play(sll.add_first(-101, num_animations=2))
        self.wait(0.5)
        self.play(sll.remove_first(num_animations=2))
        self.wait(0.5)
        # self.wait(0.5)
        # self.play(sll.add_first(-10, num_animations=2))
        # self.wait(0.5)
        # self.play(sll.add_first(-2, num_animations=2))
        # self.wait(0.5)
        # self.play(sll.remove_first(num_animations=2))
        # self.wait(0.5)
        # self.play(sll.remove_first(num_animations=2))
        # self.wait(0.5)
        # self.play(sll.add_first(7, num_animations=1))
        # self.play(sll.add_first(0, num_animations=2))
        # self.play(sll.remove_first(num_animations=2))
        # self.play(sll.add_first(101, num_animations=2))
        # self.play(sll.remove_first(num_animations=1))
        # self.play(sll.remove_first(num_animations=1))
        # self.play(sll.add_first(0, num_animations=1))
        self.wait()


if __name__ == '__main__':
    test_data_structure = True
    if not test_data_structure:
        scene_classes, problem_dir = get_scene_classes()
        aligned_animation_script = get_aligned_animation_script(
            alignment_path=os.path.join(problem_dir, ALIGNED_SCRIPT_PATH),
            script_path=os.path.join(problem_dir, ANIMATION_SCRIPT_PATH)
            )
        create_scenes(scene_classes, problem_dir, aligned_animation_script.get_scenes())
    else:
        test_scene = TestScene()
        test_scene.render()


    # open_media_file(scene.renderer.file_writer.movie_file_path)