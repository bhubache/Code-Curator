import os

from manim import config, Scene, Code, FadeIn, FadeOut, LEFT, UP, Animation, FadeIn, YELLOW, Rectangle

from code.custom_code import CustomCode
from animations.code_transform import CodeTransform

# from .base_scene import BaseScene

class BaseCodeScene(Scene):
    config.background_color = '#000E15'
    def __init__(self, problem_dir: str, aligned_animation_scene) -> None:
        super().__init__()
        source_file: str = os.path.join(os.getcwd(), 'src', 'leetcode', 'problems', 'Delete_Node_in_a_Linked_List', 'required_files', 'src.java')
        destination_file: str = os.path.join(os.getcwd(), 'src', 'leetcode', 'problems', 'Delete_Node_in_a_Linked_List', 'required_files', 'dst.java')
        self._code_src = CustomCode(file_name=source_file, background_color=config.background_color)
        self._code_dst = CustomCode(file_name=destination_file, background_color=config.background_color)
        self._align_codes(self.code_src, self.code_dst)

    @property
    def code_src(self):
        return self._code_src

    @code_src.setter
    def code_src(self, new_src: CustomCode) -> None:
        self._code_src = new_src

    @property
    def code_dst(self):
        return self._code_dst

    @code_dst.setter
    def code_dst(self, new_dst: CustomCode) -> None:
        self._code_dst = new_dst

    def create_highlighter(self):
        return self.code_src.create_highlighter()

    def code_transform(self):
        animation = CodeTransform(self.code_src, self.code_dst).animation
        self.code_dst.highlighter = self.code_src.highlighter
        self.code_src, self.code_dst = self.code_dst, self.code_src
        return animation


    def _align_codes(self, code_src: CustomCode, code_dst: CustomCode):
        most_vertical_code, most_width_code = self._get_aligning_codes(self.code_src, self.code_dst)

        self.code_src.align_to(most_vertical_code, UP)
        self.code_dst.align_to(most_vertical_code, UP)

        self.code_src.align_to(most_width_code, LEFT)
        self.code_dst.align_to(most_width_code, LEFT)

    def _get_aligning_codes(self, *codes: CustomCode) -> tuple[CustomCode, CustomCode]:
        most_vertical_code = codes[0]
        most_width_code = codes[0]

        codes = codes[1:]

        for code in codes:
            if code.has_more_height(most_vertical_code):
                most_vertical_code = code
            if code.has_more_width(most_width_code):
                most_width_code = code

        return most_vertical_code, most_width_code


    def setup(self):
        pass

    def construct(self):
        self.play(FadeIn(self.code_src))
        self.play(FadeIn(self.create_highlighter()))

        self.play(self.code_src.move_highlighter_to_token('Solution', 1))
        self.wait()

        self.play(self.code_src.move_highlighter_to_token('class', 1))
        self.wait()

        self.play(self.code_src.move_highlighter_to_token('lass Sol', 1))
        self.wait()

        self.play(self.code_src.move_highlighter(2))
        self.wait()

        # self.play(self.code_src.move_highlighter(3))
        # self.wait()

        self.play(self.code_transform())
        self.wait()

        self.play(self.code_src.move_highlighter(3))
        self.wait()

        self.play(self.code_src.move_highlighter_to_token('node', 1))
        self.wait()

        self.play(self.code_src.move_highlighter_to_token('node.next', 2))
        self.wait()

        self.play(self.code_src.move_highlighter(-1))
        self.wait()

        self.play(self.code_src.move_highlighter(1))
        self.wait()

        self.play(self.code_src.move_highlighter_to_token('node.next', 2))
        self.wait()

        self.play(self.code_src.move_highlighter_to_token('val', occurrence=1, num_lines=-1))
        self.wait()

        self.play(self.code_src.move_highlighter_to_token('=', occurrence=1))
        self.wait()
