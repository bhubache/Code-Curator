from __future__ import annotations

from typing import TYPE_CHECKING

from .delegated_attribute import DelegatedAttribute
from .simple_property import SimpleProperty
from code_curator.manim_property import manim_property

if TYPE_CHECKING:
    from types import FunctionType


# TODO: This may be too confusing to reasonably keep


def delegate_to(
    delegate_cls: type,
    to: str = "delegate",
    manim_property_include: set = frozenset(),
    normal_include: set = frozenset(),
    ignore: set = frozenset(),
) -> FunctionType:
    """A decorator for a class that delegates method calls to objects it composes.

    Args:
        delegate_cls: The class being delegated to (the class being composed).
        to: Name of the member variable used to hold the instance of ``delegate_cls``. Defaults to 'delegate'.
        manim_property_include: The properties to delegate to that are also used by manim. Defaults to frozenset().
        normal_include: The properties to delegate to. Defaults to frozenset().
        ignore: The properties to not delegate to. Defaults to frozenset().

    Returns:
        The inner function of the decorator
    """
    if not isinstance(manim_property_include, set):
        manim_property_include = set(manim_property_include)

    if not isinstance(normal_include, set):
        normal_include = set(normal_include)

    if not isinstance(ignore, set):
        ignore = set(ignore)

    normal_attributes = normal_include - ignore
    manim_property_attributes = manim_property_include - ignore

    def inner(cls):
        """Delegate desired attributes to ``delegate_cls``."""
        _store_delegate_in_property(cls)
        _add_delegating_methods(cls)
        return cls

    def _store_delegate_in_property(cls):
        """
        Before ``delegate_cls`` is instantiated, assign a ``SimpleProperty``
        to the variable name held by ``to`` as a class attribute of ``delegate_cls``.
        """
        setattr(cls, to, SimpleProperty())

    def _add_delegating_methods(cls):
        """Delegate attributes to ``delegate_cls``, accounting for those that are manim properties"""
        normal_attrs_not_implemented_by_delegator = normal_attributes - set(cls.__dict__.keys())
        for attr in normal_attrs_not_implemented_by_delegator:
            setattr(cls, attr, DelegatedAttribute(to, attr))

        manim_attrs_not_implemented_by_delegator = manim_property_attributes - set(cls.__dict__.keys())
        for attr in manim_attrs_not_implemented_by_delegator:
            delegated_attr = DelegatedAttribute(to, attr)
            attr_manim_property = manim_property(
                delegated_attr.__get__,
                delegated_attr.__set__,
                delegated_attr.__delete__,
            )
            attr_manim_property.__set_name__(cls, attr)
            setattr(cls, attr, attr_manim_property)

    return inner
