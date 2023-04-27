from __future__ import annotations

from src.custom_logging.custom_logger import CustomLogger
from src.script_handling.components.animation_script.animation_leaf import AnimationLeaf
from src.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript
logger = CustomLogger.getLogger(__name__)


class SceneScheduler:
    def __init__(self):
        self._override_start_time = 1
        self._override_end_time = 0.5

    def schedule(self, aligned_animation_scene: CompositeAnimationScript):
        flattened: list[AnimationLeaf] = aligned_animation_scene.get_flattened_iterable(
        )

        # Give spare time from Wait animations to other animations
        for i in range(len(flattened) - 1):
            curr_leaf = flattened[i]
            if not curr_leaf.has_sufficient_audio_duration():
                next_leaf = flattened[i + 1]

                run_time_curr_needs = curr_leaf.get_needed_run_time()

                if not next_leaf.has_time_to_spare(run_time_curr_needs):
                    raise Exception(
                        f'The next leaf does not have time to spare: {run_time_curr_needs}',
                    )

                next_leaf.give_spare_time_to(curr_leaf, run_time_curr_needs)

        # Roll up overriding animations
        in_overriding_animation_group = False
        rolled_up_animations = []
        for i, leaf in enumerate(flattened):
            if leaf.is_overriding_end:
                logger.critical('leaf is overriding end')
                self.handle_override_end(
                    flattened[i], flattened[i + 1], flattened[i].parent,
                )
                in_overriding_animation_group = False
            elif in_overriding_animation_group:
                continue
            elif leaf.is_overriding_start:
                logger.critical('leaf is overriding start')
                # parent = leaf.parent
                self.handle_override_start(
                    flattened[i], flattened[i - 1], flattened[i].parent,
                )
                rolled_up_animations.append(leaf.parent)
                in_overriding_animation_group = True
            else:
                rolled_up_animations.append(leaf)

        return rolled_up_animations

        # TODO: Make sure the last leaf doesn't end up with insufficient audio_duration

    # TODO: Rather than throwing an exception if the entire fading time can't be provided, make it such
    # that whatever is available is used
    # TODO: Change sucky method name

    def handle_override_start(self, start_leaf, prev_leaf, start_parent):
        if not prev_leaf.has_time_to_spare(self._override_start_time):
            raise Exception('No time to give overriding animation start')

        prev_leaf.remove_time(self._override_start_time)
        start_parent.override_start_time = self._override_start_time

    # TODO: Change sucky method name
    def handle_override_end(self, end_leaf, next_leaf, end_parent):
        if not next_leaf.has_time_to_spare(self._override_end_time * 2):
            raise Exception('No time to give overriding animation end')

        next_leaf.remove_time(self._override_end_time * 2)
        end_parent.override_end_time = self._override_end_time
