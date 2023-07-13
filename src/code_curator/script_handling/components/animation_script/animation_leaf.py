from __future__ import annotations

from collections.abc import Callable
from collections.abc import Mapping

from code_curator.custom_logging.custom_logger import CustomLogger
from manim import Animation
from manim import Wait

from ...tag import Tag
from ..alignment_script.alignments.aligned_script import AlignedScript
from .animation_script import AnimationScript
# from code_curator.script_handling.components.alignment_script.alignments.aligned_script import AlignedScript
# from code_curator.script_handling.tag import Tag
logger = CustomLogger.getLogger(__name__)

from .subanimation_time_keeper import SubanimationTimeKeeper


class AnimationLeaf(AnimationScript):
    def __init__(self, unique_id, text: str, is_wait_animation: bool, tags: list[Tag] = None):
        self._unique_id: str = unique_id
        self._text: str = text
        self._start: float = None
        self._end: float = None
        self._audio_duration: float = None
        self._animation: Animation = None
        self._is_wait_animation = is_wait_animation
        self._is_overriding_start = None
        self._is_overriding_end = None
        self._parent = None
        self._is_overriding_animation = False
        self._tags = tags
        self._func = lambda: 0
        self.SUBANIMATION_TIMINGS_NAME = '_subanimation_timings'

    def __str__(self) -> str:
        formatted_info: str = (
            f'{self._animation}'
            f"{' ' * ((len('Animation') + 15) - len(str(self._animation)))}"
            f'{self.animation_run_time}'
            f"{' ' * ((len('Animation Run Time') + 15) - len(str(self.animation_run_time)))}"
            f'{self.audio_duration}'
            f"{' ' * ((len('Audio Duration') + 15) - len(str(self.audio_duration)))}"
        )
        lines = [
            f'Section Name: {self.unique_id}',
            f'Text        : {self.text}',
            f'Tags        : {self.tags}',
            'Animation               Animation Run Time               Audio Duration',
            formatted_info,
        ]
        return '\n'.join(lines)

    @property
    def text(self) -> str:
        try:
            return ' '.join([text for text in self._text.values()])
        except AttributeError:
            return self._text.strip()

    @property
    def num_words(self):
        return len(self.text.split())

    @property
    def start(self) -> float:
        return self._start

    @start.setter
    def start(self, new_start: float) -> None:
        self._start = new_start

    @property
    def tags(self) -> list[Tag]:
        return self._tags

    @property
    def func(self) -> Callable:
        return self._func

    @func.setter
    def func(self, new_func: Callable) -> None:
        self._func = new_func

    @property
    def is_overriding_animation(self):
        return self._is_overriding_animation

    @property
    def is_overriding_start(self):
        return self._is_overriding_start

    @is_overriding_start.setter
    def is_overriding_start(self, value: bool) -> None:
        self._is_overriding_start = value

    @property
    def is_overriding_end(self):
        return self._is_overriding_end

    @is_overriding_end.setter
    def is_overriding_end(self, value: bool) -> None:
        self._is_overriding_end = value

    @property
    def is_wait_animation(self):
        return self._is_wait_animation

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def end(self) -> float:
        return self._end

    @end.setter
    def end(self, new_end):
        self._end = new_end

    @property
    def audio_duration(self) -> float:
        return self._audio_duration

    @audio_duration.setter
    def audio_duration(self, new_duration):
        self._audio_duration = new_duration

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def animation(self):
        return self._animation

    @animation.setter
    def animation(self, new_animation: Animation) -> None:
        self._animation = new_animation

    @property
    def animation_run_time(self) -> float:
        try:
            return self._animation.run_time
        except AttributeError:
            return None

    @animation_run_time.setter
    def animation_run_time(self, new_run_time: float):
        self._animation.run_time = new_run_time

    @property
    def use_code_timing(self) -> bool:
        return Tag.CODE_TIMING in self.tags

    # NOTE: Start of the magic to give subanimation timings to Scenes
    def apply_alignments(self, start, end, aligned_script: AlignedScript):
        if isinstance(self._text, Mapping):
            setattr(self, self.SUBANIMATION_TIMINGS_NAME, {})
            subanimation_time_accumulation: float = 0.0
            for subsection_name, text in self._text.items():
                # subsection_start = aligned_script.get_word_start(start)

                # TODO: This might be getting one word too far (maybe start + len(text.split()) - 1)
                # subsection_end = aligned_script.get_word_end(start + len(text.split()))
                subanimation_time_keeper = SubanimationTimeKeeper(
                    text=text,
                    words=[aligned_script.get_word(word_index) for word_index in range(start, start + len(text.split()))],
                    time_until_start=subanimation_time_accumulation
                    # word_timings=[aligned_script.get_word_duration(word_index) for word_index in range(start, start + len(text.split()))],
                )
                subanimation_time_accumulation += subanimation_time_keeper.total_run_time
                # logger.info(f'{subsection_name} start: {subsection_start}')
                # logger.info(f'{subsection_name} end: {subsection_end}')
                # subsection_audio_duration = aligned_script.get_word_duration_from_to(
                #     start,
                #     start + len(text.split()),
                # )
                getattr(self, self.SUBANIMATION_TIMINGS_NAME)[subsection_name] = subanimation_time_keeper
                # getattr(self, self.SUBANIMATION_TIMINGS_NAME)[subsection_name]['run_time'] = subsection_audio_duration
                # setattr(self, f'{subsection_name}', subsection_audio_duration)
                start = start + len(text.split())
                # logger.info(f'{subsection_name} duration: {subsection_audio_duration}')
                # logger.info(f'new start: {start}')
        else:
            self.start = aligned_script.get_word_start(start)
            self.end = aligned_script.get_word_end(end)
            self.audio_duration = aligned_script.get_word_duration_from_to(
                start, end,
            )

        # Default animation to Wait
        self.animation = Wait(self._audio_duration)

    def add_animation(
        self,
        unique_id: str,
        func: Callable,
        animation,
        is_overriding_start: bool = False,
        is_overriding_end: bool = False,
    ) -> bool:
        if self.unique_id != unique_id:
            return False

        self.is_overriding_start = is_overriding_start
        self.is_overriding_end = is_overriding_end
        self.animation = animation
        self.func = func
        logger.info('!!!!!!!!!!!!!!!!!!!!!1')
        logger.info(self.unique_id)
        logger.info(self.animation)
        logger.info(type(self.animation))
        return True

    # # TODO: Ideally, member variables are initialized in __init__
    # def add_animation(
    # self, unique_id: str, animation: Animation, is_overriding_start: bool = False, is_overriding_end: bool = False
    # ):
    #     if self.unique_id != unique_id: return False

    #     self._is_overriding_start = is_overriding_start
    #     self._is_overriding_end = is_overriding_end
    #     self._animation = animation
    #     return True

    def _unique_id_exists(self, unique_id: str) -> bool:
        return self._unique_id == unique_id

    def get_child(self, unique_id: str) -> AnimationScript:
        if unique_id != self.unique_id:
            raise RuntimeError(
                f'This leaf isn\t correct: {self.unique_id} != {unique_id}',
            )
        return self

    def get_component(self, unique_id: str) -> AnimationScript:
        if unique_id == self.unique_id:
            return self
        return None

    # NOTE: Confusing to me in this moment to have extra animations added in this method.
    # Can this be done in a more reasonable place?
    def get_flattened_iterable(self) -> list:
        # Separate explicit animation from the extra wait time!
        logger.info(self.unique_id)
        if self.unique_id == 'explanation_1_1':
            logger.info(self.animation)
            logger.info(type(self.animation))
            logger.info(self.is_wait_animation)
            logger.info(self.animation_run_time)
            logger.info(self.audio_duration)

        if isinstance(self._text, Mapping):
        #     print(self.unique_id)
        #     print(type(self.animation))
            # for subsection_name, audio_duration in getattr(self, SUBANIMATION_TIMINGS_NAME).items():
                # self.animation.set_timing(subsection_name, 10)
                # if subsection_name == 'move_first_temp_n':
                #     name_prefix = '_'.join(subsection_name.split('_')[:-1])
                #     LIKELY_MAX_NUM_NODES: int = 100
                #     RUN_TIME: float = pass
                #     try:
                #         for i in range(LIKELY_MAX_NUM_NODES):
                #             self.animation.pad_with_wait(f'name_prefix_{i}')
                #         else:
                #             raise RuntimeError('You have actually made a temp trav traverse 100 nodes... goodness gracious')
                #     except LookupError:
                #         pass
                # if subsection_name == 'move_first_temp_trav_n' or subsection_name == 'move_second_temp_trav_n':
                #     continue

                # # TODO: Fix absolutely horrendous workaround for a strange bug. All unique_ids for SubanimationGroups a prefixed with `1`.
                # try:
                #     self.animation.pad_with_wait(subsection_name, audio_duration)
                # except LookupError:
                #     self.animation.pad_with_wait(f'1{subsection_name}', audio_duration)
                # self.animation.set_timing(subsection_name, audio_duration)
                # break
                # pass
            self.audio_duration = self.animation_run_time
        else:
            # TODO: Wait animations should also be padded right???
            if not self.is_wait_animation and self.animation_run_time < self.audio_duration:
                # TODO: Look into making unique_id f'{self.unique_id}_WAIT_PADDING'
                wait_padding_explicit_animation_leaf = AnimationLeaf(
                    unique_id='WAIT_PADDING', text=self._text, is_wait_animation=True, tags=[],
                )
                wait_padding_explicit_animation_leaf.add_animation(
                    'WAIT_PADDING', lambda: 0, Wait(
                        round(self.audio_duration - self.animation_run_time, 2),
                    ), False,
                )
                wait_padding_explicit_animation_leaf.audio_duration = \
                    wait_padding_explicit_animation_leaf.animation_run_time
                
                wait_padding_explicit_animation_leaf.parent = self.parent

                self.audio_duration = self.animation_run_time


                # TODO: Change self.is_overriding_end to False and wait_padding_explicit_animation_leaf.is_overriding_end to True
                if self.is_overriding_end:
                    self.is_overriding_end = False
                    wait_padding_explicit_animation_leaf.is_overriding_end = True

                # TODO: Is this correct? Is end actually shortening because we're taking time and putting it in WAIT_PADDING?
                self.end += self.animation_run_time
                return [self, wait_padding_explicit_animation_leaf]
        return [self]

    def has_sufficient_audio_duration(self):
        return self.animation_run_time <= self.audio_duration

    def get_needed_run_time(self):
        return round(self.animation_run_time - self.audio_duration, 2)

    def has_time_to_spare(self, time_needed: float) -> bool:
        return self.is_wait_animation and self.audio_duration >= time_needed
        # return round(self.audio_duration - (self.animation_run_time + time_needed), 2) >= 0.0

    def give_spare_time_to(self, receiver, time: float):
        self.remove_time(time)

        receiver.give_time(time)

    def remove_time(self, time: float):
        self.animation_run_time -= time
        self.audio_duration -= time

    # TODO: Do I need to add time to self.animation_run_time as well??
    def give_time(self, time: float):
        self.audio_duration += time