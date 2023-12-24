from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

from manim.utils.testing.frames_comparison import frames_comparison

from code_curator.base_scene import BaseScene

if TYPE_CHECKING:
    from manim import Scene


def curator_frames_comparison(
    run_time: float | type | None = None,
    last_frame: bool = True,
    base_scene: Scene | None = None,
):
    def get_cls(cls):
        excluded_attr_names = "pytestmark"
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
                    "start_time": start_time,
                },
            )

        nonlocal base_scene
        if base_scene is None:
            base_scene = BaseScene

        for func in animation_functions:
            setattr(base_scene, func.__name__, func)

        def test_manim_func_wrapper(scene, **kwargs):
            # Because :class:`code_curator.base_scene.ExcludeDuplicateSubmobjectsMobject`
            # is a singleton, even though a new scene instantiation is passed in with each
            # parametrized call through pytest, ``scene`` contains whatever mobjects were
            # added in the previous call. So to fix this side effect, we clear the mobjects
            # from the scene.

            scene.scene = scene
            scene.animation_script = animation_script

            for attr_name, value in kwargs.items():
                setattr(scene, attr_name, value)

            return base_scene.construct(scene)

        test_manim_func_wrapper.__dict__["pytestmark"] = cls.__dict__["pytestmark"]

        old_sig = inspect.signature(cls.__init__)
        old_parameters = list(old_sig.parameters.values())
        old_parameters_without_self = [param for param in old_parameters if param.name != "self"]
        new_sig = old_sig.replace(parameters=old_parameters_without_self)
        test_manim_func_wrapper.__signature__ = new_sig
        test_manim_func_wrapper.__globals__["__module_test__"] = cls.__init__.__globals__["__module_test__"]
        test_manim_func_wrapper.__globals__["__file__"] = cls.__init__.__globals__["__file__"]
        test_manim_func_wrapper.__name__ = cls.__name__

        return frames_comparison(func=test_manim_func_wrapper, last_frame=last_frame, base_scene=base_scene)

    if callable(run_time):
        _cls = run_time
        run_time = 1.0
        return get_cls(_cls)

    if run_time is None:
        run_time = 1.0

    return get_cls
