from ..alignment_script.alignments.aligned_script import AlignedScript

class ScriptAnimation:
    def __init__(self, text: str):
        self._text: str = text
        self._num_words: int = len(self._text.split())
        self._duration: float = None
        self._animation_run_time: float = None
        self._wait_run_time: float = None

    def __str__(self):
        return self._text

    @property
    def duration(self):
        return self._duration
    
    @property
    def num_words(self):
        return self._num_words

    @property
    def animation_run_time(self) -> float:
        return self._animation_run_time

    @animation_run_time.setter
    def animation_run_time(self, run_time: float):
        if run_time < 0:
            raise ValueError('Run time of an animation cannot be negative')
        self._animation_run_time = run_time

    @property
    def wait_run_time(self) -> float:
        return self._wait_run_time

    @wait_run_time.setter
    def wait_run_time(self, run_time: float):
        if run_time < 0:
            raise ValueError('Run time of an animation cannot be negative')
        self._wait_run_time = run_time

    def apply_alignments(self, aligned_script: AlignedScript):
        self._duration = aligned_script.get_full_duration()

    def get_animation_timings(self):
        return {
            'text': self._text,
            'duration': self._duration,
            'animation_run_time': self._animation_run_time,
            'wait_run_time': self._wait_run_time
        }