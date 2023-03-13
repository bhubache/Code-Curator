from abc import ABC, abstractmethod

from ..animation_package import AnimationPackage
from ..package_animation import PackageAnimation

class BaseSLLPackager:
    def __init__(self, sll):
        self._sll = sll
        self._animation_package = None

    def _assign_subanimations_and_animate(sll_animation_func):
        '''Decorator for all public animation methods.
        '''
        def inner(self, *args, **kwargs):
            kwargs = self._set_kwargs_defaults()
            self._animation_package = AnimationPackage(self._sll)
            self._assign_subanimations()
            # Create animations with all dependencies
            return PackageAnimation(self._animation_package)
        return inner

    @abstractmethod
    def _set_kwargs_defaults(self, **kwargs):
        pass

    @abstractmethod
    def _assign_subanimations(self):
        pass