from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Sequence
from types import MethodType

from manim import Animation
from manim import Group
from manim import MathTex
from manim import Mobject
from manim import Scene
from manim import prepare_animation

from .utils.math_ import value_from_range_to_range


# NOTE: I believe a mobject must be added to Animation.mobject for it to be animated!!!

# TODO: REFACTOR!
# TODO: Overriding animations
# TODO: Consider using a frame counter rather than mapping alpha to self.alphas element
# TODO: DO prepare_animation before animation start?!


class _MobjectSentinel(Mobject):
    def __new__(cls):
        if not hasattr(cls, 'singleton_instance'):
            cls.instance = super().__new__(cls)

        return cls.instance


class ExcludeDuplicationSubmobjectsMobject(Mobject):

    def remove(self, *mobjects: Mobject) -> Mobject:
        # If more than one mobject has been passed to a single FadeOut animation,
        # all the mobjects will be wrapped in a Group. So, we need to iterate over
        # the group to remove each mobject.
        for mobject_to_remove in mobjects:
            if isinstance(mobject_to_remove, Group):
                for submobject_to_remove in mobject_to_remove:
                    self.remove(submobject_to_remove)

            self._remove(
                mobject_to_remove=mobject_to_remove,
                mobject_to_search=self,
                mobject_container=None,
            )

        self._remove_all_sentinels()

        return self

    def _remove(
        self,
        *,
        mobject_to_remove: Mobject,
        mobject_to_search: Mobject,
        mobject_container: Mobject | None,
    ) -> None:
        try:
            problem_tex_parent = mobject_to_search.problem_tex_parent
        except AttributeError:
            pass
        else:
            if mobject_to_remove is problem_tex_parent:
                self._place_sentinel(
                    mobject_container=mobject_container,
                    mobject_to_remove=mobject_to_search,
                )
                # mobject_container.remove(mobject_to_search)

        if mobject_to_remove in mobject_to_search.submobjects:
            self._place_sentinel(
                mobject_container=mobject_to_search,
                mobject_to_remove=mobject_to_remove,
            )
            # mobject_to_search.submobjects.remove(mobject_to_remove)

        # FIXME: I think some mobjects aren't being removed because we're modifying
        #   the length of mobject_to_search.submobjects while iterating?

        for mobject in mobject_to_search.submobjects:
            self._remove(
                mobject_to_remove=mobject_to_remove,
                mobject_to_search=mobject,
                mobject_container=mobject_to_search,
            )

    def _place_sentinel(
        self,
        *,
        mobject_container: Mobject,
        mobject_to_remove: Mobject,
    ) -> None:
        # try:
        #     self.scene.mobjects.remove(mobject_to_remove)
        # except ValueError:
        #     pass

        index: int = mobject_container.submobjects.index(mobject_to_remove)
        mobject_container.submobjects[index] = _MobjectSentinel()

    def _remove_all_sentinels(self) -> None:
        # TODO: Remove empty Groups?
        new_submobjects = []
        for submobject in self.submobjects:
            if isinstance(submobject, _MobjectSentinel):
                continue

            try:
                submobject.submobjects = self._remove_all_sentinels_helper(submobject)
            except AttributeError:
                pass
            finally:
                new_submobjects.append(submobject)

        self.submobjects = new_submobjects

    def _remove_all_sentinels_helper(self, mobject: Mobject):
        new_submobjects: list[Mobject] = []
        for submobject in mobject.submobjects:
            if isinstance(submobject, _MobjectSentinel):
                continue

            try:
                submobject.submobjects = self._remove_all_sentinels_helper(submobject)
            except AttributeError:
                pass
            finally:
                new_submobjects.append(submobject)

        return new_submobjects


class CuratorAnimation(Animation):
    def __init__(self, stream_map: dict, stream_instances, run_time: float, scene: Scene) -> None:
        super().__init__(ExcludeDuplicationSubmobjectsMobject(), run_time=run_time)
        self.stream_map = stream_map
        self.stream_instance_map = {stream_inst.__class__.__name__: stream_inst for stream_inst in stream_instances}
        self.scene = scene

        setattr(self.scene, "mobjects", [self.mobject])

        self.pending_stream_queue = PendingStreamQueue(self.run_time)
        for stream_name, stream in self.stream_map.items():
            for entry in stream.entries:
                animation_method = getattr(self.stream_instance_map[stream_name], entry["name"])
                animation_method.__func__.start_time = entry["start_time"]
                self.pending_stream_queue.push(stream_name, animation_method)

        self.running_queue = RunningStreamQueue(self.run_time, self.mobject, self.pending_stream_queue, scene=self.scene)

    def begin(self) -> None:
        """Override and do nothing to avoid ``interpolate_mobject`` being called twice with alpha equal to 0."""
        pass

    def interpolate_mobject(self, alpha: float) -> None:
        # clean up from scene for ending animations
        for animation in self.running_queue.get_animations_to_end(alpha):
            animation.clean_up_from_scene(self.scene)

            mobjects_to_remove = self._get_remover_animation_mobjects(animation)
            for mobject in mobjects_to_remove:
                # if alpha > 0.88:
                #     breakpoint()
                self.mobject.remove(mobject)

        # begin new animations
        for stream_name, animation_method in self.pending_stream_queue.get_animation_methods_to_begin(alpha):
            self.running_queue.push(stream_name, animation_method)

        # update running animations
        self.running_queue.run_animations(alpha)

    def _get_remover_animation_mobjects(self, animation: Animation) -> Sequence[Mobject]:
        mobjects_to_be_removed: list[Mobject] = []
        if animation.is_remover():
            mobjects_to_be_removed.append(animation.mobject)
        else:
            try:
                child_animations = animation.animations
            except AttributeError:
                pass
            else:
                for child_anim in child_animations:
                    mobjects_to_be_removed.extend(
                        self._get_remover_animation_mobjects(child_anim)
                    )

        return mobjects_to_be_removed

class _MultiStreamAnimationsQueue:
    def __init__(self, run_time: float) -> None:
        self.stream_to_queue_map: dict[str, list] = {}
        self.run_time = run_time

    @property
    def stream_names(self) -> Iterable[str]:
        return self.stream_to_queue_map.keys()

    def push(self, stream_name: str, element) -> None:
        self.stream_to_queue_map.setdefault(stream_name, [])
        self.stream_to_queue_map[stream_name].append(element)

    def peek(self, stream_name: str):
        return self.stream_to_queue_map[stream_name][0]

    def peek_start_time(self, stream_name: str) -> float:
        return self.peek(stream_name).start_time

    def peek_start_alpha(self, stream_name: str) -> float:
        try:
            next_element = self.peek(stream_name)
            return next_element.start_alpha
        except AttributeError:
            next_element.__func__.start_alpha = value_from_range_to_range(
                next_element.start_time,
                init_min=0.0,
                init_max=self.run_time,
                new_min=0.0,
                new_max=1.0,
            )
            return next_element.start_alpha

    def pop(self, stream_name: str):
        return self.stream_to_queue_map[stream_name].pop(0)


class PendingStreamQueue:
    def __init__(self, run_time: float) -> None:
        self.queue = _MultiStreamAnimationsQueue(run_time)

    def push(self, stream_name, animation_method: MethodType) -> None:
        self.queue.push(stream_name, animation_method)

    def peek_start_alpha(self, stream_name) -> float:
        try:
            return self.queue.peek_start_alpha(stream_name)
        except IndexError:
            return float('inf')

    def get_animation_methods_to_begin(self, curr_alpha: float) -> Sequence[tuple[str, MethodType]]:
        methods = []
        for stream_name in self.queue.stream_names:
            try:
                if curr_alpha >= self.queue.peek_start_alpha(stream_name):
                    methods.append((stream_name, self.queue.pop(stream_name)))
            except IndexError:
                # All animations in stream with name ``stream_name`` have been exhausted
                continue

        return methods


class RunningStreamQueue:
    def __init__(self, run_time: float, animation_mobject: Mobject, pending_stream_queue: PendingStreamQueue, scene: Scene) -> None:
        self.queue = _MultiStreamAnimationsQueue(run_time)
        self.animation_mobject = animation_mobject
        self.pending_queue = pending_stream_queue
        self.scene = scene

    def push(self, stream_name: str, animation_method: MethodType) -> None:
        try:
            self.queue.peek(stream_name)
            # running_animation = self.queue.pop(stream_name)
        except (IndexError, KeyError):
            # No running animation in stream, proceed normally!
            animation_to_start = animation_method()
            animation_to_start = self._prepare_animation(animation_to_start)
            # animation_to_start = prepare_animation(animation_to_start)
            try:
                self.animation_mobject.add(animation_to_start.mobject)
            except ValueError:
                # Attempting to add ExcludeDuplicationSubmobjectsMobject to itself
                self.animation_mobject.add(
                    *animation_to_start.mobject.submobjects,
                )

            # self._add_mobjects(animation_to_start)
            print(f"STARTING ANIMATION {animation_to_start} with run_time {animation_to_start.run_time}")
            # TODO: Possible some floating point innaccuracies going on!
            stop_alpha = animation_method.start_alpha + value_from_range_to_range(
                animation_to_start.run_time,
                init_min=0.0,
                init_max=self.queue.run_time,
                new_min=0.0,
                new_max=1.0,
            )

            if stop_alpha > (next_start_alpha := self.pending_queue.peek_start_alpha(stream_name)):
                if hasattr(animation_method, "run_time_can_be_truncated"):
                    stop_alpha = next_start_alpha
                else:
                    raise RuntimeError(f"{animation_to_start} is too long and can't be shortened")

            animation_to_start = self.animation_alpha_converter(
                animation_to_start,
                start_alpha=animation_method.start_alpha,
                stop_alpha=stop_alpha,
            )
            animation_to_start.start_alpha = animation_method.start_alpha
            animation_to_start.stop_alpha = stop_alpha
            # if animation_to_start.__class__.__name__ == "Circumscribe":
            #     animation_to_start.scene = self.scene

            animation_to_start.begin()
            self.queue.push(stream_name, animation_to_start)
        else:
            # There is an animation running, it should already be cleaned up and removed!
            raise

    # TODO: Figure this out with  out as well
    def _add_mobjects(self, animation: Animation) -> None:
        try:
            subanimations = animation.animations
        except AttributeError:
            self.animation_mobject.add(animation.mobject)
        else:
            for sub_anim in subanimations:
                self._add_mobjects(sub_anim)

    def _prepare_animation(self, animation) -> Animation:
        if isinstance(animation, Mobject):
            animation = animation.build_animation()
        else:
            animation = prepare_animation(animation)

        return animation

    def peek_stop_alpha(self, stream_name: str) -> float:
        return self.queue.peek(stream_name).stop_alpha

    def get_animation_methods_to_begin(self, curr_alpha: float) -> Sequence[tuple[str, MethodType]]:
        methods = []
        for stream_name in self.queue.stream_names:
            if curr_alpha >= self.queue.peek_start_alpha(stream_name):
                methods.append((stream_name, self.queue.pop(stream_name)))

        return methods

    def get_animations_to_end(self, curr_alpha: float) -> Sequence[Animation]:
        animations: list[Animation] = []
        for stream_name in self.queue.stream_names:
            try:
                if curr_alpha >= self.peek_stop_alpha(stream_name):
                    animations.append(self.queue.pop(stream_name))
            except IndexError:
                # There are currently no running animations in stream ``stream_name``
                continue

        return animations

    def run_animations(self, curr_alpha: float) -> None:
        # TODO: Maybe performing interpolate again for animations that just started
        for stream_name in self.queue.stream_names:
            try:
                self.queue.peek(stream_name).interpolate(curr_alpha)
            except IndexError:
                # There might not be any animations running in the stream currently
                continue

    def animation_alpha_converter(self, animation: Animation, start_alpha: float, stop_alpha: float, first_call: bool = True):
        new_interpolate_name = "_curator_interpolate"

        def interpolate_wrapper(curr_overall_alpha: float):
            converted_alpha = value_from_range_to_range(
                curr_overall_alpha,
                init_min=start_alpha,
                init_max=stop_alpha,
                new_min=0.0,
                new_max=1.0,
            )

            nonlocal first_call
            if first_call:
                converted_alpha = 0.0
                first_call = False

            getattr(animation, new_interpolate_name)(converted_alpha)

        setattr(animation, new_interpolate_name, animation.interpolate)
        setattr(animation, 'interpolate', interpolate_wrapper)
        return animation
