from __future__ import annotations

import functools
import inspect
import types
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

        # Because the ``curator_frames_comparison`` decorator is run on every
        # test class before any test case is executed, the ``base_scene`` class
        # will have all test class methods as attributes. To prevent a method
        # from being overwritten by another method with the same name, I'm
        # prepending the method's surrounding class name to make them distinct.
        for func in animation_functions:
            func.__name__ = f"{cls.__name__}_{func.__name__}"

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

        scene_init_attr_name = f"{cls.__name__}_{cls.__init__.__name__}"
        setattr(base_scene, scene_init_attr_name, cls.__init__)

        def test_manim_func_wrapper(scene, **kwargs):
            try:
                kwargs.pop("__")
            except KeyError:
                pass  # See the comments at ``return`` of the outer function for explanation

            getattr(scene, scene_init_attr_name)(scene, **kwargs)
            scene.animation_script = animation_script

            return base_scene.construct(scene)

        try:
            test_manim_func_wrapper.__dict__["pytestmark"] = cls.__dict__["pytestmark"]
        except KeyError:
            pass  # pytestmark not being used

        old_sig = inspect.signature(cls.__init__)
        old_parameters = list(old_sig.parameters.values())
        old_parameters_without_self = [param for param in old_parameters if param.name != "self"]
        new_sig = old_sig.replace(parameters=old_parameters_without_self)
        test_manim_func_wrapper.__signature__ = new_sig
        test_manim_func_wrapper.__globals__["__module_test__"] = cls.__init__.__globals__["__module_test__"]
        test_manim_func_wrapper.__globals__["__file__"] = cls.__init__.__globals__["__file__"]
        test_manim_func_wrapper.__name__ = cls.__name__

        # Three pieces of context for what's happening below:
        # 1. To find the control_path directory for a given test, manim looks at
        #    ``thing.__globals__["__file__"]``, where thing is the func that is
        #    passed into ``frames_comparison``.
        #
        # 2. When ``pytest`` is called on the command line, it rounds up all the tests. This
        #    causes every instance of ``curator_frames_comparison`` decorator to run before
        #    any test is run.
        #
        # 3. The lines above manipulating ``test_manim_func_wrapper``'s ``__globals__``
        #    all refer to the same dictionary.
        #
        # So, if we pass ``test_manim_func_wrapper`` into ``frames_comparison``,
        # ``test_manim_func_wrapper.__globals__["__file__"]`` will be the path to
        # whatever the last file where the ``curator_frames_comparison`` was called.
        # We can't simply assign a copy of a dictionary to ``test_manim_func_wrapper.__globals__``
        # because the attribute is read-only. So, we make a custom function type instead, and
        # makes its globals be a shallow copy of the ``__globals__``.
        # Based on:
        # https://stackoverflow.com/questions/49076566/override-globals-in-function-imported-from-another-module
        independent_func_wrapper = types.FunctionType(
            code=test_manim_func_wrapper.__code__,
            globals=test_manim_func_wrapper.__globals__.copy(),
            name=test_manim_func_wrapper.__name__,
            argdefs=test_manim_func_wrapper.__defaults__,
            closure=test_manim_func_wrapper.__closure__,
        )
        independent_func_wrapper = functools.update_wrapper(independent_func_wrapper, test_manim_func_wrapper)

        output = frames_comparison(func=independent_func_wrapper, last_frame=last_frame, base_scene=base_scene)

        # Static reference:
        # https://github.com/ManimCommunity/manim/blob/ed1b203993382e6cfd0e0ae990f39b0b1679df25/manim/utils/testing/frames_comparison.py#L247
        # The code within ``manim.utils.testing.frames_comparison._control_data_path`` for adding the ".npz" extension
        # to the control data file name does so by using ``pathlib.Path.with_suffix(".npz")``. This just searches for
        # the last ``.`` in the file name (if one exists) and truncates the file name there. The trouble with
        # this implementation is that unique file names are created by appending the stringified test arguments
        # to the file name (this accounts for paramatrized tests). It's very possible that these arguments contain a
        # ``.`` such as with floating-point numbers. This can lead to two different parametrizations pointing to the
        # same file.
        #
        # For example:
        #
        #   {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.0)}
        #   {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.0), "radius": 1}
        #
        # These would both be truncated to:
        #
        #   {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.npz
        #
        # By appending a keyword argument that has a ``.`` as its value, I'm allowing the entirety of the arguments
        # to be present in the file name.
        @functools.wraps(output)
        def wrapper_to_access_test_arguments(*args, **kwargs):
            kwargs |= {"__": "."}
            return output(*args, **kwargs)

        return wrapper_to_access_test_arguments

    if callable(run_time):
        _cls = run_time
        run_time = 1.0
        return get_cls(_cls)

    if run_time is None:
        run_time = 1.0

    return get_cls


def starts_at(time_in_seconds: float):
    def inner(fn):
        fn.start_time = time_in_seconds
        return fn

    return inner
