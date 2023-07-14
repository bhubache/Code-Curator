from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Sequence

from manim import Animation
from manim import AnimationGroup
from manim import Wait
from script_handling.components.animation_script.subanimation_time_keeper import SubanimationTimeKeeper

# TODO: The 'and' time that extends to the next time keeper is getting lost

class ParallelAnimation(Animation):
    def __init__(
        self,
        *string_alignments: str,
        time_keepers: list[SubanimationTimeKeeper],
        animations: Iterable[Animation]
    ):
        """*string_alignments MUST BE CONTIGUOUS strings from the animation_script yaml!!!"""
        self.string_alignments: tuple[str] = string_alignments
        self.time_keepers = time_keepers
        self.animations = animations

        # TODO:
        # animation: (first animation at least)
        #   1. Wait animation before start
        #   2. Time start for full string length or default time
        #   3. If timing default and time left over in string, pad with Wait

        self.finalized_animations = self._build()

    def __str__(self) -> str:
        raise NotImplementedError()

    def build(self):
        # breakpoint()
        animation_group = AnimationGroup(
            *self.finalized_animations,
            lag_ratio=1,
        )
        # animation_group.is_overriding_animation = True
        return animation_group

    def _build(self):
        animations = []
        initial_wait_animation = Wait(self.time_keepers[0].time_until_start)
        animations.append(initial_wait_animation)

        animations = self._get_animation_timings()
        for time_keeper in self.time_keepers:
            time_keeper.reset()

        animations.insert(0, initial_wait_animation)
        return animations
    
    def _get_animation_timings(self) -> Sequence[Animation]:
        # self.time_keepers[0].partition(string_alignment)
        # If resulting tuple has an empty string as the second element, shrink string_alignment by one token from the right
        # and perform partition again. Repeat until resulting tuple as second element. Then, take the string that was chopped
        # off from the right of string_alignment and do self.time_keepers[1].partition(``that string``). If the resulting tuple
        # has something other than the empty string as its first element AND something other than the empty string as its second
        # element, then an exception should be raised because the requested string_alignment is not contiguous. If the resulting
        # tuple as something other than the empty string as its first element and an empty string as its second element, the
        # string_alignment stretches across more time_keepers and further searching is necessary.

        # TODO: If the first string_alignment can't at all be found in the first time_keeper, the incorrect time_keeper start has been passed in
        # raise an exception saying so.
        latest_exhausted_time_keeper = -1

        animation_timings = []
        animations = []

        while latest_exhausted_time_keeper < (len(self.time_keepers) - 2):
            for string_alignment in self.string_alignments:
                # if string_alignment == 'to p2.':
                #     breakpoint()
                partition = self.time_keepers[latest_exhausted_time_keeper + 1].partition(string_alignment)
                while True:
                    overflow_sequence: list[str] = []
                    while not self._substring_found(partition):
                        overflow_sequence.insert(0, string_alignment.split()[-1])
                        string_alignment = ' '.join(string_alignment.split()[:-1])
                        partition = self.time_keepers[latest_exhausted_time_keeper + 1].partition(string_alignment)

                    # partition[0] will be wait animation
                    # TODO: Only run this once per string_alignment
                    if bool(partition[0]):
                        animation_timings.append(self.time_keepers[latest_exhausted_time_keeper + 1].get_sequence_time(partition[0]))
                        animations.append(
                            Wait(animation_timings[-1])
                        )
                        animation_timings.append(0.0)

                    if len(overflow_sequence) == 0:
                        DEFAULT_RUN_TIME = 1
                        animation_timings[-1] += self.time_keepers[latest_exhausted_time_keeper + 1].get_sequence_time(partition[1])
                        next_animation = self.animations.pop(0)
                        if animation_timings[-1] > DEFAULT_RUN_TIME:
                            next_animation.run_time = DEFAULT_RUN_TIME
                            animations.append(next_animation)
                            animations.append(Wait(animation_timings[-1] - DEFAULT_RUN_TIME))
                        else:
                            next_animation.run_time = animation_timings[-1]
                            animations.append(
                                next_animation,
                            )
                        animation_timings.append(0.0)

                        if bool(partition[1]) and bool(partition[2]) and partition[1] in self.time_keepers[latest_exhausted_time_keeper + 1].text:
                            self._remove_words(time_keeper_index=latest_exhausted_time_keeper + 1, tokens=partition[1].split())
                        elif bool(partition[1]) and partition[1] in self.time_keepers[latest_exhausted_time_keeper + 1].text:
                            self._remove_words(time_keeper_index=latest_exhausted_time_keeper + 1, tokens=partition[1].split())
                            latest_exhausted_time_keeper += 1


                        break
                    else:
                        # TODO: Strip strings?
                        animation_timings[-1] += self.time_keepers[latest_exhausted_time_keeper + 1].get_sequence_time(partition[1])
                        latest_exhausted_time_keeper += 1
                        partition = self.time_keepers[latest_exhausted_time_keeper + 1].partition(' '.join(overflow_sequence))
                        # # NOTE: Error if overflow_sequence extends past curr_time_keeper?
                        self._check_non_contiguous_string(partition)

        if animation_timings[-1] == 0.0:
            animation_timings = animation_timings[:-1]

        return animations

    def _remove_words(self, time_keeper_index: int, tokens: Sequence[str]) -> None:
        curr_time_keeper_text_tokens = self.time_keepers[time_keeper_index].text.split()
        curr_time_keeper_text_tokens = curr_time_keeper_text_tokens[len(tokens):]
        self.time_keepers[time_keeper_index].text = ' '.join(curr_time_keeper_text_tokens)

        curr_time_keeper_word_tokens = self.time_keepers[time_keeper_index].words
        curr_time_keeper_word_tokens = curr_time_keeper_word_tokens[len(tokens):]
        self.time_keepers[time_keeper_index].words = curr_time_keeper_word_tokens

        curr_time_keeper_word_timing_tokens = self.time_keepers[time_keeper_index].word_timings
        curr_time_keeper_word_timing_tokens = curr_time_keeper_word_timing_tokens[len(tokens):]
        self.time_keepers[time_keeper_index].word_timings = curr_time_keeper_word_timing_tokens     

    def _substring_found(self, partition: tuple[str, str, str]) -> bool:
        return bool(partition[1])
    
    def _check_non_contiguous_string(self, partition: tuple[str, str, str]) -> None:
        if bool(partition[0]) and bool(partition[1]):
            raise ValueError('string_alignment is non-contiguous.')