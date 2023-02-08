from manim import *

# from .base_scene import BaseScene

# TODO: Make lexer
# TODO: Make theme
# TODO: See dev taoism for above

class BaseCodeScene(Scene):
    config.background_color = '#2E3440'
    # config.background_color = '#1c1f26'
    def __init__(self, problem_dir, aligned_animation_scene):
        super().__init__()

    def setup(self):
        pass

    def construct(self):
        code = Code(
            file_name=r'C:\Users\brand\Documents\ManimCS\src\leetcode\problems\Delete_Node_in_a_Linked_List\required_files\solution.java',
            font='Monospace',
            tab_width=4,
            background='rectangle',
            background_stroke_width=0,
            language='java',
            insert_line_no=False,
            style='nord',
            margin=1
        )

        # background rectangle: code.code[0]
        # Dot                 : code.code[1]
        # paragraph of lines  : code.code[2]
        # Each line is broken up into characters

        colors = [RED, BLACK, GREEN, YELLOW, BLUE, ORANGE, PURPLE, RED, BLACK, GREEN, YELLOW, BLUE, ORANGE, PURPLE, RED, BLACK, GREEN, YELLOW, BLUE, ORANGE, PURPLE, RED, BLACK, GREEN, YELLOW, BLUE, ORANGE, PURPLE]


        highlight_bar = Rectangle(color=YELLOW, height=code.code[2].height, fill_color=YELLOW, stroke_opacity=0.5, stroke_width=0, width=code.code[2].width).set_opacity(0.5)
        highlight_bar.align_to(code.code[2])
        highlight_bar.align_to(code.code[2], UP)
        self.play(FadeIn(code), FadeIn(highlight_bar))
        self.wait()



    def tear_down(self):
        pass