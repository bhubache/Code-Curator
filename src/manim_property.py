from __future__ import annotations

from manim.constants import DEFAULT_STROKE_WIDTH

# TODO: Take in default value!
# TODO: Once all attributes are set, don't ignore ``AttributeError``


class manim_property:
    """A lot of mobjects I've made use composition rather than inheritance. :class:`~base_scene.BaseScene`
    One example is :class:`Edge`, which is a :class:`custom_vmobject.CustomVMobject` composed
    of a :class:`Line` and a :class:`Weight`. I ran into an issue when exposing
    some attributes as part of the public API. ``stroke_width`` for instance, was
    originally written as follows:

    .. code-block:: python

        @property
        def stroke_width(self) -> int:
            return self._line.stroke_width

        @stroke_width.setter
        def stroke_width(self, new_stroke_width: int) -> None:
            self._line.stroke_width = new_stroke_width

    The issue with this arises when the constructor of :class:`Edge`s parent class
    :class:`CustomVMobject` is called (which is called **before** the initialization
    of any member variables of :class:`Edge`). The __init__ of :class:`CustomVMobject`
    in turn calls the __init__ of :class:`VMobject`, wherein, the initialization of
    several public variables takes place, including ``self.stroke_width``. When that
    occurs, the stroke_width setter property inside :class:`Edge` is used, throwing
    an ``AttributeError`` because ``self._line`` has yet to be initialized. Introducing
    :class:`manim_property`, which:

    1. Allows the code to proceed normally when manim variable initialization is happening
       and composed mobjects necessary for variable access have yet to be initialized
    2. Appropriately raises an ``AttributeError`` once all the manim variable initialization has
       completed
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._name = ''
        self._attr_should_exist: bool = False

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"property '{self._name}' has no getter")

        try:
            value = self.fget(obj)
        except AttributeError:
            if self._attr_should_exist:
                raise AttributeError(
                    f'{obj} should have attribute {self._name} but doesn\'t',
                )
            else:
                return DEFAULT_STROKE_WIDTH
        else:
            self._attr_should_exist = True
            return value

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError(f"property '{self._name}' has no setter")

        try:
            self.fset(obj, value)
        except AttributeError:
            if self._attr_should_exist:
                raise AttributeError(
                    f'{obj} should have attribute {self._name} but doesn\'t',
                )
            else:
                pass
        else:
            self._attr_should_exist = True

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError(f"property '{self._name}' has no deleter")
        self.fdel(obj)

    def getter(self, fget):
        prop = type(self)(fget, self.fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def setter(self, fset):
        prop = type(self)(self.fget, fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def deleter(self, fdel):
        prop = type(self)(self.fget, self.fset, fdel, self.__doc__)
        prop._name = self._name
        return prop
