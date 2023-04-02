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
    # config.frame_rate = 240
    # import json
    # print(type(config))
    # print(json.dumps(config, indent=4, default=str))

    def construct(self):
        from data_structures.singly_linked_list.singly_linked_list import SinglyLinkedList
        from data_structures.nodes.singly_linked_list_node import SLLNode
        from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
        self.sll = SinglyLinkedList(1, 2, 3, 4, 5, 6)
        self.play(FadeIn(self.sll))

        # from animations.singly_linked_list.subanimations.fade_out_container import FadeOutContainer
        # from animations.singly_linked_list.subanimations.fade_out_mobject import FadeOutMobject
        # from animations.singly_linked_list.subanimations.strictly_successive.move_trav import SuccessiveMoveTrav
        # from animations.package_animation import PackageAnimation
        # from animations.animation_package import AnimationPackage
        # from animations.subanimation_group import SubanimationGroup

        # some_group = SubanimationGroup(
        #     SubanimationGroup(
        #         SubanimationGroup(
        #             FadeOutMobject(self.sll, self.sll[0].pointer_to_next, self.sll[0]),
        #             SubanimationGroup(
        #                 FadeOutMobject(self.sll, self.sll[0].pointer_to_next, self.sll[0])
        #             ),
        #         ),
        #         SuccessiveMoveTrav(self.sll, self.sll.head_pointer, self.sll[1]),
        #         SuccessiveMoveTrav(self.sll, self.sll.head_pointer, self.sll[2]),
        #         SubanimationGroup(
        #             SubanimationGroup(
        #                 SubanimationGroup(
        #                     SuccessiveMoveTrav(self.sll, self.sll.head_pointer, self.sll[2])
        #                 ),
        #             ),
        #         ),
        #     ),
        #     SuccessiveMoveTrav(self.sll, self.sll.head_pointer, self.sll[3]),
        #     SuccessiveMoveTrav(self.sll, self.sll.head_pointer, self.sll[4]),
        # )

        # animation_package = AnimationPackage(self.sll)
        # animation_package.clean_up_mobject = lambda : 0
        # animation_package._subanimation_group = some_group
        # self.play(PackageAnimation(self.sll, animation_package))


        # nested_subanimation_group = SubanimationGroup(
        #     SuccessiveMoveTrav(self.sll, self.sll.tail_pointer, self.sll[-2]),
        #     FadeOutContainer(self.sll, self.sll[-1].container, self.sll[-1]),
        #     FadeOutMobject(self.sll, self.sll[-2].pointer_to_next, self.sll[-2])
        # )

        # subanimation_group: SubanimationGroup = SubanimationGroup(
        #     SuccessiveMoveTrav(self.sll, self.sll.head_pointer, self.sll[1]),
        #     FadeOutContainer(self.sll, self.sll[0].container, self.sll[0]),
        #     FadeOutMobject(self.sll, self.sll[0].pointer_to_next, self.sll[0]),
        #     lag_ratio=0.25,
        # )
        # subanimation_group.insert(1, nested_subanimation_group)

        # animation_package: AnimationPackage = AnimationPackage(self.sll)
        # animation_package.clean_up_mobject = lambda : 0
        # animation_package._subanimation_group = subanimation_group
        # self.play(PackageAnimation(self.sll, animation_package))

        # FIXME: animation flatten list WITH center sll doesn't work
        # self.play(
        #     self.sll.insert(
        #         index=3,
        #         data=-1,
        #         display_first_trav=False,
        #         display_second_trav=False,
        #         trav_position='start'
        #     )
        #     .subsequently_fade_in_container()
        #     .subsequently_fade_in_pointer()
        #     .subsequently_change_prev_node_pointer()
        #     # .subsequently_fade_out_first_temp_trav()
        #     .subsequently_flatten_list().with_center_sll()
        #     .build_animation()
        # )

        # for sub in self.sll.submobjects:
        #     pass
            # self.play(sub.animate.set_opacity(1))
            # self.play(sub.animate.set_color(RED))
            # self.play(sub.animate.set_opacity(0))

        # for node in self.sll:
        #     self.play(FadeIn(Circle(radius=0.02).move_to(node.get_container_left())))
        #     self.play(FadeIn(Circle(radius=0.02).move_to(node.get_container_top())))
        #     self.play(FadeIn(Circle(radius=0.02).move_to(node.get_container_right())))
        #     self.play(FadeIn(Circle(radius=0.02).move_to(node.get_container_bottom())))

        # from animations.animation_package import AnimationPackage
        # from animations.package_animation import PackageAnimation
        # from animations.subanimation_group import SubanimationGroup
        # from animations.singly_linked_list.subanimations.fade_in_mobject import FadeInMobject
        # from animations.singly_linked_list.subanimations.strictly_successive.move_trav import SuccessiveMoveTrav
        # from data_structures.pointers.pointer import Pointer
        # trav = Pointer(self.sll[0], self.sll, 'trav', direction=UP)

        # some_group = SubanimationGroup(
        #     SubanimationGroup(
        #         SubanimationGroup(
        #             FadeInMobject(self.sll, trav, self.sll),
        #             lag_ratio=1
        #         ),
        #         SuccessiveMoveTrav(self.sll, trav, self.sll[1]),
        #         SuccessiveMoveTrav(self.sll, trav, self.sll[2]),
        #         lag_ratio=1
        #     )
        # )
        # animation_package: AnimationPackage = AnimationPackage(self.sll)
        # animation_package.clean_up_mobject = lambda : 0
        # animation_package._subanimation_group = some_group
        # self.play(PackageAnimation(self.sll, animation_package))

        self.play(
            self.sll.remove_at(
                index=4,
                display_first_trav=True,
                display_second_trav=True,
                trav_position='start'
            )
            .subsequently_shrink_pointer()
            .subsequently_unshrink_pointer()
            .subsequently_curve_pointer()
            .subsequently_fade_out_container().with_fade_out_pointer().with_fade_out_first_temp_trav().with_fade_out_second_temp_trav()
            .subsequently_flatten_list()
            .subsequently_center_sll()
            .build_animation()
        )

        # self.play(self.sll.remove_last_all_together())

        # self.play(self.sll.remove_first_all_together())
        # self.play(self.sll.remove_at_test(3, show_each_pointer_change=True, display_first_trav=True, display_second_trav=True))
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
            script_path=os.path.join(problem_dir, ANIMATION_SCRIPT_PATH)
            )
        create_scenes(scene_classes, problem_dir, aligned_animation_script.get_scenes())
    else:
        test_scene = TestScene()
        test_scene.render()


    # open_media_file(scene.renderer.file_writer.movie_file_path)
