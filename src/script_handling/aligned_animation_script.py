from .components.alignment_script.alignments.aligned_script import AlignedScript
from .components.animation_script.composite_animation_script import CompositeAnimationScript
from .components.animation_script.animation_leaf import AnimationLeaf

from typing import Union

class AlignedAnimationScript:
    def __init__(self, aligned_script: AlignedScript, animation_script: CompositeAnimationScript):
        self._aligned_script:   AlignedScript            = aligned_script
        self._animation_script: CompositeAnimationScript = animation_script

        self._animation_script.apply_alignments(1, len(self._aligned_script._words), self._aligned_script)

    def get_scenes(self) -> list[Union[CompositeAnimationScript, AnimationLeaf]]:
        return self._animation_script.children
        