from __future__ import annotations

from code_curator.animations.curator_animation_new import CuratorAnimation
from code_curator.base_scene import BaseScene


class MockAnimationScript:
    def __init__(self) -> None:
        self.entries = []

    def add_entry(self, *, method_name, start_time: float) -> None:
        self.entries.append(
            {
                "name": method_name,
                "start_time": start_time,
            },
        )
        self.entries.sort(key=lambda entry: entry["start_time"])


class MockBaseScene(BaseScene):
    def __init__(self, **kwargs) -> None:
        super().__init__(None, **kwargs)

        self.animation_script = MockBaseScene.__dict__["animation_script"]
        self.animation_script.run_time = MockBaseScene.__dict__["run_time"]

    @classmethod
    def set_run_time(cls, run_time: float) -> None:
        cls.run_time = run_time
        return cls

    @classmethod
    def add_animation_method(cls, method_name, *, start_time: float):
        if not hasattr(cls, "animation_script"):
            cls.animation_script = MockAnimationScript()

        cls.animation_script.add_entry(method_name=method_name, start_time=start_time)
        return cls

    def register_function(self, animation_function) -> None:
        setattr(MockBaseScene, animation_function.__name__, animation_function)

    def play(
        self,
        *args,
        subcaption=None,
        subcaption_duration=None,
        subcaption_offset=0,
        **kwargs,
    ):
        breakpoint()
        super().play(
            CuratorAnimation(
                animation_script=self.animation_script,
                scene=self,
                run_time=self.animation_script.run_time,
            ),
        )
