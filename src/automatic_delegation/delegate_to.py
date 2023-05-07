from __future__ import annotations

from .delegated_attribute import DelegatedAttribute
from .simple_property import SimpleProperty


def delegate_to(delegate_cls, to='delegate', include=frozenset(), ignore=frozenset()):
    if not isinstance(include, set):
        include = set(include)
    if not isinstance(ignore, set):
        ignore = set(ignore)
    delegates_attrs = set(delegate_cls.__dict__.keys())
    attributes = include | delegates_attrs - ignore

    def decorator(cls):
        _store_delegate_in_property(cls)
        _add_delegating_methods(cls)
        # def inner(*args, **kwargs):
        #     _store_delegate_in_property(cls)
        #     _add_delegating_methods(cls)
        #     print(args)
        #     print(kwargs)
        #     print(type(cls))
        #     print(type(cls()))
        # return cls(*args, **kwargs)
        return cls

    def _store_delegate_in_property(cls):
        setattr(cls, to, SimpleProperty())

    def _add_delegating_methods(cls):
        # Don't delegate attributes already implemented by ``cls``
        attrs_not_implemented_by_delegator = attributes - \
            set(cls.__dict__.keys())
        print(attrs_not_implemented_by_delegator)
        for attr in attrs_not_implemented_by_delegator:
            setattr(cls, attr, DelegatedAttribute(to, attr))

        # return cls

    return decorator
