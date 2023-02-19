from manim import Animation, Wait
from .animation_script_interface import IAnimationScript
from script_handling.components.alignment_script.alignments.aligned_script import AlignedScript
from script_handling.tag import Tag

class AnimationLeaf(IAnimationScript):
    def __init__(self, unique_id, text: str, is_wait_animation: bool, tags: list[Tag]):
        self._unique_id: str = unique_id
        self._text: str = text
        self._start: float = None
        self._end: float = None
        self._duration: float = None
        self._animation: Animation = None
        self._is_wait_animation = is_wait_animation
        self._is_overriding_start = None
        self._is_overriding_end = None
        self._parent = None
        self._is_overriding_animation = False
        self._tags = tags

    def __str__(self) -> str:
        lines = [
            f'Section Name: {self.unique_id}',
            f'Text        : {self.get_text()}',
            f'Animation               Animation Run Time               Audio Duration',
            f'{self._animation}{" " * ((len("Animation") + 15) - len(str(self._animation)))}{self.animation_run_time}{" " * ((len("Animation Run Time") + 15) - len(str(self.animation_run_time)))}{self.audio_duration}{" " * ((len("Audio Duration") + 15) - len(str(self.audio_duration)))}'
        ]
        return '\n'.join(lines)
        # return f'{self._unique_id}:\n{self._text}\n{self._animation}  {self.audio_duration}  {self.animation_run_time}\n\n'

    # @property
    # def text(self) -> str:
    #     return self.text.strip()

    def get_text(self) -> str:
        return self._text.strip()

    def get_num_words(self) -> int:
        return len(self.get_text().split())

    def apply_alignments(self, start, end, aligned_script: AlignedScript):
        self._start = aligned_script.get_word_start(start)
        self._end = aligned_script.get_word_end(end)
        self._duration = aligned_script.get_word_duration_from_to(start, end)

        # Default animation to Wait
        self._animation = Wait(self._duration)

    # TODO: Ideally, member variables are initialized in __init__
    def add_animation(self, animation: Animation, is_overriding_start: bool = False, is_overriding_end: bool = False):
        self._is_overriding_start = is_overriding_start
        self._is_overriding_end = is_overriding_end
        self._animation = animation

    def get_child(self, unique_id: str) -> IAnimationScript:
        if unique_id != self.unique_id:
            raise RuntimeError(f'This leaf isn\t correct: {self.unique_id} != {unique_id}')
        return self

    @property
    def is_overriding_animation(self):
        return self._is_overriding_animation

    @property
    def is_overriding_start(self):
        return self._is_overriding_start

    @property
    def is_overriding_end(self):
        return self._is_overriding_end

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
        return self._duration

    @audio_duration.setter
    def audio_duration(self, new_duration):
        self._duration = new_duration

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def animation(self):
        return self._animation

    @property
    def animation_run_time(self) -> float:
        return self._animation.run_time
        # if self._animation is None: return -1.0
        # try:
        #     return self._animation.run_time
        # except Exception:
        #     print(self._animation)
        #     print(self.unique_id)
        #     raise

    @animation_run_time.setter
    def animation_run_time(self, new_run_time: float):
        self._animation.run_time = new_run_time

    def get_flattened_iterable(self) -> list:
        # assert self.animation_run_time <= self.audio_duration, f'{self.unique_id}'
        # Separate explicit animation from the extra wait time!
        if not self.is_wait_animation and self.animation_run_time < self.audio_duration:
            wait_padding_explicit_animation_leaf = AnimationLeaf(unique_id='WAIT_PADDING', text=self._text, is_wait_animation=True, tags=[])
            wait_padding_explicit_animation_leaf.add_animation(Wait(round(self.audio_duration - self.animation_run_time, 2)))
            wait_padding_explicit_animation_leaf.audio_duration = wait_padding_explicit_animation_leaf.animation_run_time

            self.audio_duration = self.animation_run_time
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

    def give_time(self, time: float):
        self.audio_duration += time
