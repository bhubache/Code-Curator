from __future__ import annotations
from manim import Animation
from .animation_script_interface import IAnimationScript
from .animation_leaf import AnimationLeaf
from script_handling.components.alignment_script.alignments.aligned_script import AlignedScript

class CompositeAnimationScript(IAnimationScript):
    def __init__(self, unique_id: str, children: list[AnimationLeaf]):
        self._unique_id = unique_id
        self._children = children
        self._parent = None
        self._animations: list[Animation] = []

    def __str__(self):
        new_line = '\n'
        tab = '\t'
        new_line_and_tab = new_line + tab
        return f'{self._unique_id}{new_line}{new_line_and_tab.join([tab+str(child) for child in self._children])}'

    def get_flattened_iterable(self) -> list:
        flattened = []
        for child in self._children:
            flattened += child.get_flattened_iterable()
        return flattened

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent: CompositeAnimationScript):
        self._parent = new_parent
        for child in self.children:
            child.parent = self

    def get_text(self):
        raise NotImplementedError()

    def get_num_words(self):
        total_words = 0
        for child in self.children:
            total_words += child.get_num_words()
        return total_words

    def apply_alignments(self, start, end, aligned_script: AlignedScript):
        for child in self.children:
            # sub_aligned_script = aligned_script.get_words_from_to(start, child.get_num_words() + 1, aligned_script)
            child.apply_alignments(start, start + child.get_num_words() - 1, aligned_script)

            start += child.get_num_words()

    # TODO: Get rid of the try except statement
    def add_animations(self, unique_id: str, animations: list[Animation], is_overriding_animation: bool) -> bool:
        found_composite = False
        if self.unique_id != unique_id:
            for child in self.children:
                if isinstance(child, AnimationLeaf):
                    if child.unique_id != unique_id: continue
                    else:
                        try:
                            child.add_animation(animations[0])
                        except Exception:
                            print(animations)
                            raise
                elif child.add_animations(unique_id, animations, is_overriding_animation): return True
        else:
            assert len(self.children) == len(animations), 'number of children don\'t match number of animations!'
            found_composite = True
            self.is_overriding_animation = is_overriding_animation
            for i, (child, anim) in enumerate(zip(self.children, animations)):
                is_overriding_start = False
                is_overriding_end = False
                if i == 0:
                    is_overriding_start = True
                elif i == len(self.children) - 1:
                    is_overriding_end = True
                child.add_animation(anim, is_overriding_start=is_overriding_start, is_overriding_end=is_overriding_end)
        return found_composite

    @property
    def children(self):
        return self._children

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def audio_duration(self):
        total_duration = 0.0
        for child in self.children:
            total_duration += child.audio_duration
        return total_duration

    @property
    def animation_run_time(self):
        total_run_time = 0.0
        for child in self.children:
            total_run_time += child.animation_run_time
        return total_run_time
