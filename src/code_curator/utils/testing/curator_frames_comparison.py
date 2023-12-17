from __future__ import annotations

from manim.utils.testing.frames_comparison import frames_comparison
from manim import Scene

from code_curator.base_scene import BaseScene


def curator_frames_comparison(
    run_time: float | type | None = None,
    last_frame: bool = True,
    base_scene: Scene | None = None,
):

    def get_cls(cls):
        excluded_attr_names = ("pytestmark")
        animation_functions = []

        for attr_name, attr in cls.__dict__.items():
            if attr_name not in excluded_attr_names and not attr_name.startswith("__") and not attr_name.endswith("__"):
                animation_functions.append(attr)

        class AnimationScript:
            def __init__(self) -> None:
                self.entries = []

        animation_script = AnimationScript()
        animation_script.run_time = run_time

        for func in animation_functions:
            try:
                start_time = func.start_time
            except AttributeError:
                start_time = 0.0

            animation_script.entries.append(
                {
                    "name": func.__name__,
                    "start_time": start_time
                }
            )

        # base_scene = BaseScene(animation_script)

        # for func in animation_functions:
        #     setattr(type(base_scene), func.__name__, func)

        def test_manim_func_wrapper(scene, unique_value, sll):
            breakpoint()
            scene.animation_script = animation_script
            scene.unique_value = unique_value
            scene.sll = sll
            return BaseScene.construct(scene)

        test_manim_func_wrapper.__dict__["pytestmark"] = cls.__dict__["pytestmark"]
        breakpoint()

        nonlocal base_scene
        if base_scene is None:
            base_scene = BaseScene

        return frames_comparison(func=test_manim_func_wrapper, last_frame=last_frame, base_scene=base_scene)

    if callable(run_time):
        _cls = run_time
        run_time = 1.0
        return get_cls(_cls)

    if run_time is None:
        run_time = 1.0

    return get_cls


