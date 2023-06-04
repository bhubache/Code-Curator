from __future__ import annotations

from code_curator.constants import DEFAULT_MOBJECT_COLOR
from code_curator.constants import DEFAULT_STROKE_WIDTH
from code_curator.custom_logging.custom_logger import CustomLogger
from manim import ArrowTriangleTip
logger = CustomLogger.getLogger(__name__)

# TODO: Take in default value!
# TODO: Once all attributes are set, don't ignore ``AttributeError``

_DEFAULT_PROPERTY_MAP = {
    'color': DEFAULT_MOBJECT_COLOR,
    'stroke_width': DEFAULT_STROKE_WIDTH,
    'tip': ArrowTriangleTip(length=0.2, width=0.2),
}


class manim_property:
    """A lot of mobjects I've made use composition rather than inheritance. :class:`~base_scene.BaseScene`
    One example is :class:`~data_structures.edges.edge.Edge`, which is a :class:`~custom_vmobject.CustomVMobject`
    composed of a :class:`Line` and a :class:`~data_structures.edges.weights.weight.Weight`. I ran into an issue
    when exposing some attributes as part of the public API. ``stroke_width`` for instance, was
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

        # TODO:
        # Put this on the obj, BE CAREFUL WHEN DOING THIS SO IT IS NOT OVERWRITTEN
        # I think there has to one for every manim property on the obj!
        # self._attr_should_exist: bool = False
        self._attr_existence_check_name: str = ''

    def __set_name__(self, owner, name):
        self._name = name
        self._attr_existence_check_name = f'_{self._name}_should_exist'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"property '{self._name}' has no getter")

        try:
            value = self.fget(obj)
        except AttributeError:
            try:
                getattr(obj, self._attr_existence_check_name)
            except AttributeError:
                return _DEFAULT_PROPERTY_MAP[self._name]
            else:
                raise AttributeError(
                    f'Attempting to get: {obj} should have attribute {self._name} but doesn\'t',
                )
        else:
            setattr(obj, self._attr_existence_check_name, True)
            return value

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError(f"property '{self._name}' has no setter")

        try:
            self.fset(obj, value)
        except AttributeError:
            try:
                getattr(obj, self._attr_existence_check_name)
            except AttributeError:
                pass
            else:
                raise AttributeError(
                    f'Attempting to set: {obj} should have attribute {self._name} but doesn\'t',
                )

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
