from __future__ import annotations

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.script_handling.components.animation_script.animation_leaf import AnimationLeaf
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript
logger = CustomLogger.getLogger(__name__)

# DEVELOPMENT IMPORTS
from .animations.data_structure_animation import DataStructureAnimation


class SceneScheduler:
    def __init__(self):
        self._override_start_time = 0.5
        self._override_end_time = 0.25

    def schedule(self, aligned_animation_scene: CompositeAnimationScript):
        flattened: list[AnimationLeaf] = aligned_animation_scene.get_flattened_iterable()

        logger.critical('!!!!!!!!!!!!!!!!!!!!!!!!!!')
        for elem in flattened:
            print(elem)

        for leaf in flattened:
            if isinstance(leaf.animation, DataStructureAnimation):
                print(leaf)
                print(leaf.animation)
                print(leaf.audio_duration)
                print(leaf.animation_run_time)
                # raise

        # Give spare time from Wait animations to other animations
        for i in range(len(flattened) - 1):
            curr_leaf = flattened[i]
            if not curr_leaf.has_sufficient_audio_duration():
                next_leaf = flattened[i + 1]

                run_time_curr_needs = curr_leaf.get_needed_run_time()

                if not next_leaf.has_time_to_spare(run_time_curr_needs):
                    raise Exception(
                        f'The next leaf {next_leaf.unique_id} does not have time to spare: {run_time_curr_needs}',
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
                # NOTE: We're not appending animations within (excluding start) to rolled_up_animations! Is this bad???
                if leaf not in leaf.parent.children:
                    logger.critical(f'{leaf.unique_id} not in parents children. Adding it')
                    insertion_index = leaf.parent.children.index(flattened[i - 1]) + 1
                    leaf.parent.children.insert(insertion_index, leaf)
                continue
            elif leaf.is_overriding_start:
                logger.critical('leaf is overriding start')
                # parent = leaf.parent
                self.handle_override_start(
                    flattened[i], flattened[i - 1], flattened[i].parent,
                )
                # NOTE: I'm thinking including the parent in rolled_up_animations is what may cause the WAIT_PADDINGs to not be
                # included after each animation of explanation_1. I think this because the WAIT_PADDINGs are only included in
                # the flattened iterable but not the leaf parent itself!!!
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
    # TODO: hopefully end_leaf is a wait animation. If it is, don't worry about taking time from the next_leaf,
    # just remove the time from the end_leaf directly.
    def handle_override_end(self, end_leaf, next_leaf, end_parent):
        if end_leaf.is_wait_animation:
            if not end_leaf.has_time_to_spare(self._override_end_time * 2):
                logger.critical(f'Ignoring inability to give time to overriding animation end for WAIT!')
                pass
                # raise Exception('No time to give overriding animation end for WAIT')
            
            end_leaf.remove_time(self._override_end_time * 2)
            end_parent.override_end_time = self._override_end_time
        else:
            if not next_leaf.has_time_to_spare(self._override_end_time * 2):
                raise Exception('No time to give overriding animation end')

            next_leaf.remove_time(self._override_end_time * 2)
            end_parent.override_end_time = self._override_end_time
