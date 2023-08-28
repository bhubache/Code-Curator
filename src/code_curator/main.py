"""Starting point for the creation of a video.

You can either create a video using custom scenes or test some animation code!
"""

from __future__ import annotations

__all__: Sequence[str] = []

import importlib
import logging
import os
import subprocess
import yaml
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

from manim import config
from manim import UP
from manim import DOWN
from manim import Wait
from manim import FadeIn
from manim import Circle
from manim import Scene
from manim import MoveAlongPath
from manim import Line
from manim import Tex
from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip

from code_curator.ai_audio_creator import AIAudioCreator
from code_curator.script_handling.aligned_animation_script import AlignedAnimationScript
from code_curator.alignment_text_creation.alignment_text_creator import AlignmentTextCreator
from code_curator.script_handling.components.alignment_script.alignments.alignment_parser import AlignmentParser
from code_curator.script_handling.simple_script_parser_factory import SimpleScriptParserFactory
from code_curator.animations.fixed_succession import FixedSuccession
from code_curator.data_structures.singly_linked_list import SinglyLinkedList
# from manim.utils.file_ops import open_file as open_media_file


if TYPE_CHECKING:
    from code_curator.script_handling.components.animation_script.animation_script import AnimationScript
    from code_curator.base_scene import BaseScene
    from types import ModuleType
    from collections.abc import Sequence


FRAMES_PER_SECOND = 60


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PROBLEM_NAME = 'Delete_Node_in_a_Linked_List'

# ALIGNED_SCRIPT_PATH = Path('generated_files', 'aligned_script.txt')
ALIGNED_SCRIPT_PATH = Path('generated_files', 'ai_aligned_script.txt')
# ANIMATION_SCRIPT_PATH = Path('required_files', 'animation_script.txt')
# ANIMATION_SCRIPT_PATH = Path('required_files', 'key_points_animation_script.txt')
# ANIMATION_SCRIPT_PATH = Path('required_files', 'animation_script_yaml.yaml')
# ANIMATION_SCRIPT_PATH = Path('required_files', 'present_problem_animation_script.yaml')
ANIMATION_SCRIPT_PATH = Path('required_files', 'problem_analysis_animation_script.yaml')

CONCRETE_PRESENT_PROBLEM_PATH = f'code_curator.leetcode.problems.{PROBLEM_NAME}.scenes.present_problem'
CONCRETE_PROBLEM_ANALYSIS_PATH = f'code_curator.leetcode.problems.{PROBLEM_NAME}.scenes.problem_analysis'
CONCRETE_KEY_POINTS_PATH = f'code_curator.leetcode.problems.{PROBLEM_NAME}.scenes.key_points'
CONCRETE_CODE_SOLUTION_PATH = f'code_curator.leetcode.problems.{PROBLEM_NAME}.scenes.code_solution'


def create_class(scene_classes: Sequence[type], aligned_animation_scene_scripts: Sequence[AnimationScript]) -> type:
    """Create class that will ultimately render the entire video.

    Args:
        scene_classes: A sequence of scene classes for the video.
        aligned_animation_scene_scripts: The animation scripts that correspond to each scene class.

    Returns:
        MyScene - See top.
    """
    class MyScene(Scene):
        """Class that will ultimately render the video.

        Attributes:
            _video_dir: Path to the directory containing the created scenes.
            _scene_instances: The Scene objects to create each scene video.
            config: Manim config for MyScene.
        """

        config.disable_caching = True
        config.frame_rate = FRAMES_PER_SECOND

        def __init__(self, problem_dir: str) -> None:
            """Construct MyScene.

            Args:
                problem_dir: Path to the directory containing all information
                    regarding the leetcode problem for the video.
            """
            super().__init__()
            self._video_dir = Path.home().joinpath('ManimCS', 'Code-Curator', 'media', 'videos', '1080p60')
            self._scene_instances = []
            custom_scene_classes = [scene_classes[1]]
            for i, (cls, scene_script) in enumerate(zip(custom_scene_classes, aligned_animation_scene_scripts)):
                scene_inst = cls(problem_dir, scene_script)
                scene_inst.video_dir = self._video_dir
                self._scene_instances.append(scene_inst)

        def construct(self) -> None:
            """Create the scenes."""
            for i, scene_inst in enumerate(self._scene_instances):
                # Only calling render seems to get the video to save
                scene_inst.render()
                # _give_scene_ordered_name(scene_inst, i)

    return MyScene


def get_scene_classes() -> tuple[list[type], Path]:
    scene_classes: list[type] = []
    present_problem_module: ModuleType = importlib.import_module(
        CONCRETE_PRESENT_PROBLEM_PATH,
    )
    if present_problem_module.__file__ is None:
        raise TypeError(f'file for {present_problem_module} is None.')

    problem_dir = Path(present_problem_module.__file__).parents[1]
    present_problem_cls = getattr(present_problem_module, 'PresentProblem')
    scene_classes.append(present_problem_cls)

    problem_analysis_module = importlib.import_module(CONCRETE_PROBLEM_ANALYSIS_PATH)
    problem_analysis_cls = getattr(problem_analysis_module, 'ProblemAnalysis')
    scene_classes.append(problem_analysis_cls)

    key_points_module = importlib.import_module(CONCRETE_KEY_POINTS_PATH)
    key_points_cls = getattr(key_points_module, 'KeyPoints')
    scene_classes.append(key_points_cls)

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
    return AlignedAnimationScript(
        aligned_script=aligned_script,
        animation_script=animation_script,
    )


def create_scenes(
    scene_classes: list[type],
    problem_dir: Path,
    aligned_animation_scene_scripts: Sequence[AnimationScript],
) -> None:
    scene = create_class(
        scene_classes, aligned_animation_scene_scripts,
    )(problem_dir)
    scene.render()

    # concatenate_scenes(scene._video_dir, len(scene_classes))


def _give_scene_ordered_name(scene_instance: BaseScene, index: int) -> None:
    old_file_path = Path(
        scene_instance.video_dir,
        f'{type(scene_instance).__name__}.mp4',
    )
    new_file_path = Path(
        scene_instance.video_dir,
        f'{index}.mp4',
    )

    new_file_path.unlink()

    subprocess.getoutput(f'mv {old_file_path} {new_file_path}')
    subprocess.getoutput(f'chmod 777 {new_file_path}')


class TestScene(Scene):
    config.disable_caching = True

    def construct(self) -> None:
        from code_curator.data_structures.singly_linked_list import SinglyLinkedList
        sll = SinglyLinkedList(0)
        self.play(
            sll.add_last(data=1)
            .subsequently_fade_in_container()
            .with_fade_in_pointer()
            .with_move_tail()
            .with_center_sll()
            .build_animation()
        )

        self.play(
            FadeIn(Circle()),
            FadeIn(Circle(0.1)),
        )
        return
        t = Tex(
            r'There is a singly linked list head and we want to delete a node node in it. You are given the node to be deleted node. You will not be given access to the first node of head. All the values of the linked list are unique, and it is guaranteed that the given node node is not the last node in the linked list. Delete the given node. Note that by deleting the node, we do not mean removing it from memory. We mean',
            font_size=20,
        )

        self.play(FadeIn(t))


        return

        c = Circle()
        self.play(
            FixedSuccession(
                FadeIn(c),
                MoveAlongPath(c, Line(c.get_center(), c.get_center() + [0, 2.5, 0])),
                MoveAlongPath(c, Line(c, [0, -2.5, 0])),
                # c.animate.to_edge(DOWN),
                # c.animate.to_edge(UP),
                Wait(),
                scene=self,
            ),
        )

        return

        from code_curator.code.custom_code import CustomCode
        code = CustomCode(Path.home() / 'ManimCS' / 'Code_Curator' / 'src' / 'code_curator' / 'leetcode' / 'problems' / 'Delete_Node_in_a_Linked_List' / 'required_files' / 'two_pointer_sll_node_removal.java')

        code.set_opacity(0)
        self.add(code)
        self.play(code.get_opacity_animation('p1.next'))
        self.play(code.get_opacity_animation('='))
        self.play(code.get_opacity_animation('p2;'))
        self.play(code.get_fade_out_animation())
        # self.play(FadeIn(self.create_highlighter()))

        # self.play(code.move_highlighter_to_token('Solution', 1))
        # self.wait()

        # self.play(code.move_highlighter_to_token('class', 1))
        # self.wait()

        # self.play(code.move_highlighter_to_token('lass Sol', 1))
        # self.wait()

        # self.play(code.move_highlighter(2))
        # self.wait()


        from code_curator.data_structures.singly_linked_list import SinglyLinkedList
        # from code_curator.data_structures.nodes.singly_linked_list_node import SLLNode
        # from code_curator.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
        # self.sll = SinglyLinkedList(1)
        # self.play(FadeIn(self.sll))

        # from code_curator.animations.data_structure_animation import DataStructureAnimation
        # from code_curator.animations.singly_linked_list.data_structure_animator import DataStructureAnimator
        # from code_curator.animations.subanimation_group import SubanimationGroup
        # from code_curator.animations.singly_linked_list.subanimations.move_and_flip_trav import MoveAndFlipTrav

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




def main() -> None:
    test_data_structure = False
    generate_ai_speech: bool = True
    if not test_data_structure:
        scene_classes, problem_dir = get_scene_classes()

        if generate_ai_speech:
            # Generate ai_script.txt from the animation script
            ai_script_path: Path = problem_dir / 'dev_files' / 'MFA' / 'input' / 'ai_script.txt'
            animation_script_dict = yaml.safe_load((problem_dir / ANIMATION_SCRIPT_PATH).read_text())

            def flatten_iterable(animation_script_dict: dict):
                # result = []
                for element in animation_script_dict.values():
                    if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
                        # result.append(extract_text(element))
                        yield from flatten_iterable(element)
                    else:
                        yield element
                        # result.append(element)

                # return ' '.join(result)
                # return ' '.join(list(result))

            script = ' '.join(flatten_iterable(animation_script_dict))
            with open(ai_script_path, 'w', encoding='UTF-8') as write_file:
                write_file.write(script)

            # Generate audio from text
            audio_path: Path = AIAudioCreator.create_audio(ai_script_path)
            ALIGNED_SCRIPT_PATH = AlignmentTextCreator.create_alignment_text(problem_dir / 'dev_files')



        aligned_animation_script = get_aligned_animation_script(
            alignment_path=os.path.join(problem_dir, ALIGNED_SCRIPT_PATH),
            script_path=os.path.join(problem_dir, ANIMATION_SCRIPT_PATH),
        )
        create_scenes(
            scene_classes, problem_dir,
            aligned_animation_script.get_scenes(),
        )

        # Combine video and audio together!
        video_clip = VideoFileClip(str(Path(Path.cwd() / 'media', 'videos', f'1080p{FRAMES_PER_SECOND}', 'ProblemAnalysis.mp4')))
        audio_clip = AudioFileClip(str(audio_path))
        final_clip: VideoFileClip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(str(Path(Path.home(), 'Videos', 'FULL_VIDEO.mp4')), fps=FRAMES_PER_SECOND)
    else:
        test_scene = TestScene()
        test_scene.render()

    # open_media_file(scene.renderer.file_writer.movie_file_path)

def postmortem_main():
    try:
        main()
    except Exception:
        import pdb; pdb.post_mortem()



if __name__ == '__main__':
    main()
