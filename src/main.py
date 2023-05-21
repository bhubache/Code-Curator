from __future__ import annotations

import importlib
import logging
import os
from collections.abc import Sequence
from types import ModuleType

from base_scene import BaseScene
from manim import config
from manim import FadeIn
from manim import Scene
from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip
from script_handling.aligned_animation_script import AlignedAnimationScript
from script_handling.components.alignment_script.alignments.alignment_parser import AlignmentParser
from script_handling.components.animation_script.animation_script import AnimationScript
from script_handling.simple_script_parser_factory import SimpleScriptParserFactory
# import time
# from manim.utils.file_ops import open_file as open_media_file


# To open the movie after render.


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PROBLEM_NAME = 'Delete_Node_in_a_Linked_List'

ALIGNED_SCRIPT_PATH = r'generated_files\aligned_script.txt'
ANIMATION_SCRIPT_PATH = r'required_files\animation_script.txt'

CONCRETE_PRESENT_PROBLEM_PATH = f'leetcode.problems.{PROBLEM_NAME}.scenes.present_problem'
CONCRETE_PROBLEM_ANALYSIS_PATH = f'leetcode.problems.{PROBLEM_NAME}.scenes.problem_analysis'
CONCRETE_CODE_SOLUTION_PATH = f'leetcode.problems.{PROBLEM_NAME}.scenes.code_solution'


def create_class(scene_classes: list[type], aligned_animation_scene_scripts: Sequence[AnimationScript]) -> type:
    class MyScene(Scene):
        # config.disable_caching = True

        def __init__(self, problem_dir: str) -> None:
            super().__init__()
            self._video_dir = r'C:\Users\brand\Documents\ManimCS\media\videos\1080p60'
            self._scene_instances = []
            for cls, scene_script in zip(scene_classes, aligned_animation_scene_scripts):
                scene_inst = cls(problem_dir, scene_script)
                scene_inst.video_dir = self._video_dir
                self._scene_instances.append(scene_inst)

        def setup(self) -> None:
            pass

        def construct(self) -> None:
            for i, scene_inst in enumerate(self._scene_instances):
                # Only calling render seems to get the video to save
                scene_inst.render()
                _give_scene_ordered_name(scene_inst, i)

        def tear_down(self) -> None:
            pass

    return MyScene


def get_scene_classes() -> tuple[list[type], str]:
    scene_classes = []
    present_problem_module: ModuleType = importlib.import_module(
        CONCRETE_PRESENT_PROBLEM_PATH,
    )
    if present_problem_module.__file__ is None:
        raise Exception(f'File for {present_problem_module} is null')
    present_problem_cls = getattr(
        present_problem_module, 'PresentProblem',
    )
    problem_dir = '\\'.join(present_problem_module.__file__.split('\\')[:-2])
    scene_classes.append(present_problem_cls)

    problem_analysis_module = importlib.import_module(
        CONCRETE_PROBLEM_ANALYSIS_PATH,
    )
    problem_analysis_cls = getattr(problem_analysis_module, 'ProblemAnalysis')
    scene_classes.append(problem_analysis_cls)

    # code_solution_module = importlib.import_module(CONCRETE_CODE_SOLUTION_PATH)
    # code_solution_cls = getattr(code_solution_module, 'CodeSolution')
    # scene_classes.append(code_solution_cls)

    # FIXME: Bad practice returning a tuple with loosely understood ordering
    return scene_classes, problem_dir


def concatenate_scenes(video_dir: str, num_scenes: int) -> None:
    scene_video_paths = [
        VideoFileClip(
            os.path.join(
                video_dir, f'{str(i)}.mp4',
            ),
        ) for i in range(num_scenes)
    ]
    final_clip = concatenate_videoclips(scene_video_paths)
    final_clip.write_videofile(os.path.join(video_dir, 'output.mp4'))


def get_aligned_animation_script(alignment_path: str, script_path: str) -> AlignedAnimationScript:
    aligned_script = AlignmentParser(file_path=alignment_path).parse()
    script_parser_factory = SimpleScriptParserFactory(script_path=script_path)
    animation_script = script_parser_factory.create_script_parser(
        'leetcode',
    ).parse()
    aligned_animation_script = AlignedAnimationScript(
        aligned_script=aligned_script, animation_script=animation_script,
    )
    return aligned_animation_script


def create_scenes(
    scene_classes: list[type],
    problem_dir: str,
    aligned_animation_scene_scripts: Sequence[AnimationScript],
) -> None:
    scene = create_class(
        scene_classes, aligned_animation_scene_scripts,
    )(problem_dir)
    scene.render()

    concatenate_scenes(scene._video_dir, len(scene_classes))


def _give_scene_ordered_name(scene_instance: BaseScene, index: int) -> None:
    old_file_path = os.path.join(
        scene_instance.video_dir, f'{scene_instance.__class__.__name__}.mp4',
    )
    new_file_path = os.path.join(scene_instance.video_dir, f'{index}.mp4')

    if os.path.exists(new_file_path):
        os.remove(new_file_path)

    os.rename(old_file_path, new_file_path)


# def _get_animation_timing_iterable(aligned_animation_script: AlignedAnimationScript) -> Iterable[dict]:
#     animation_timings_list = []
#     for timing_info in aligned_animation_script.get_animation_timings().values():
#         animation_timings_list.append(timing_info)
#     return animation_timings_list


class TestScene(Scene):
    config.disable_caching = True
    # config.frame_rate = 240
    # import json
    # print(type(config))
    # print(json.dumps(config, indent=4, default=str))

    def construct(self) -> None:
        from data_structures.singly_linked_list import SinglyLinkedList
        # from data_structures.nodes.singly_linked_list_node import SLLNode
        # from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
        self.sll = SinglyLinkedList(1, 2)
        self.play(FadeIn(self.sll))

        # from animations.data_structure_animation import DataStructureAnimation
        # from animations.singly_linked_list.data_structure_animator import DataStructureAnimator
        # from animations.subanimation_group import SubanimationGroup
        # from animations.singly_linked_list.subanimations.move_and_flip_trav import MoveAndFlipTrav

        # sub_group = SubanimationGroup(
        #     MoveAndFlipTrav(
        #     sll=self.sll,
        #     trav=self.sll.head_pointer,
        #     to_node=self.sll[1]
        #     )
        # )

        # self.play(
        #     DataStructureAnimation(
        #     sll=self.sll,
        #     data_structure_animator=sub_group
        #     )
        # )

        self.play(
            self.sll.add_last(
                data=17,
                display_first_trav=False,
                first_trav_name='custom',
                trav_position='start',
            )
            .subsequently_fade_in_container()
            .subsequently_fade_in_pointer()
            .subsequently_move_tail()
            .with_center_sll()
            .build_animation(),
        )

        # for sub in self.sll.submobjects:
        #     self.play(sub.animate.set_color('#FF0000'))
        #     self.play(sub.animate.set_opacity(0))
        #     self.play(sub.animate.set_opacity(1))

        # for sub in self.sll.submobjects:
        #     sub.set_opacity(1)

        # self.play(
        #     self.sll.remove_at(
        #         index=4,
        #         display_first_trav=True,
        #         display_second_trav=True,
        #         trav_position='start'
        #     )
        #     .subsequently_shrink_pointer()
        #     .subsequently_unshrink_pointer()
        #     .subsequently_curve_pointer()
        #     .subsequently_fade_out_container()
        #     .with_fade_out_pointer()
        #     .with_fade_out_first_temp_trav()
        #     .with_fade_out_second_temp_trav().with_flatten_list().with_center_sll()
        #     .build_animation()
        # )

        # self.play(self.sll.remove_last_all_together())

        # self.play(self.sll.remove_first_all_together())
        # self.play(
        #   self.sll.remove_at_test(
        #       3,
        #       show_each_pointer_change=True,
        #       display_first_trav=True,
        #       display_second_trav=True)
        # )
        # self.play(self.sll.add_first_all_together(-1, pointer_animation_type='fade'))
        # self.play(self.sll.add_last_test(-1, pointer_animation_type='fade', display_trav=True, trav_position='start'))
        # self.play(self.sll.insert_at_front_all_together(2, -1, pointer_animation_type='fade'))
        # self.play(self.sll.insert_test(2, -1, display_trav=True))
        # self.sll.insert_test(2, -1, display_trav=True)

        # for sub in self.sll.submobjects:
        #     logger.info(sub)
        #     self.play(sub.animate.set_opacity(1))
        #     self.play(FadeOut(sub))

        # for node in self.sll:
        #     self.play(FadeIn(Circle(radius=0.02).next_to(node, RIGHT, buff=0)))
        # self.play(FadeIn(Circle(radius=0.02).move_to(node.get_right())))
        # self.play(self.sll.insert_test(1, -1))

        # self.play(FadeIn(Circle(radius=0.02).move_to(self.sll.get_right())))
        # self.play(FadeIn(Circle(radius=0.02).move_to(self.sll.get_left())))
        # self.play(FadeIn(Circle(radius=0.02).move_to(self.sll.get_top())))
        # self.play(FadeIn(Circle(radius=0.02).move_to(self.sll.get_bottom())))
        # self.play(FadeIn(Circle(radius=0.02).move_to(self.sll.get_center())))
        # self.play(FadeIn(Circle(radius=0.02, color=BLUE).move_to([0, 0, 0])))
        # self.play(self.sll.insert_all_together(1, -1))

        # self.wait()
        # self.play(self.sll.insert_all_together(1, 70))
        # self.play(self.sll.insert_all_together(1, 'code'))
        # self.play(self.sll.insert_test(2, -1))
        # self.play(self.sll.insert_test(2, -1))
        # self.play(self.sll.add_first_all_together(-1))
        # self.play(self.sll.add_first(-1))
        # self.play(self.sll.add_first(-1))
        # self.play(self.sll.remove_at(3))
        # self.play(self.sll.remove_at(2))
        # self.play(self.sll.remove_first())
        # self.play(self.sll.insert(3, -1))
        # self.play(self.sll.add_first(0))
        # self.play(self.sll.add_first(1000, 1))
        # self.play(self.sll.add_last(7, 1))
        # self.play(self.sll.insert(3, 1111))
        # self.wait(1)
        # self.play(self.sll.add_last(10, 1))
        # self.wait(1)
        # self.play(self.sll.remove_at_index(3))
        # self.wait(1)
        # self.play(self.sll.insert(1, 10))
        # self.wait(1)
        # self.play(self.sll.remove_at_index(2))
        # self.wait(1)
        # self.play(self.sll.insert(2, 10))
        self.wait()


if __name__ == '__main__':
    test_data_structure = True
    if not test_data_structure:
        scene_classes, problem_dir = get_scene_classes()
        aligned_animation_script = get_aligned_animation_script(
            alignment_path=os.path.join(problem_dir, ALIGNED_SCRIPT_PATH),
            script_path=os.path.join(problem_dir, ANIMATION_SCRIPT_PATH),
        )
        create_scenes(
            scene_classes, problem_dir,
            aligned_animation_script.get_scenes(),
        )
    else:
        test_scene = TestScene()
        test_scene.render()

    # open_media_file(scene.renderer.file_writer.movie_file_path)
