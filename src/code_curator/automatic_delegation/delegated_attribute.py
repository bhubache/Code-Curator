from __future__ import annotations


class DelegatedAttribute:
    """A descriptor for delegating access of ``attr_name`` to the object of name ``delegate_name``.

    Args:
        delegate_name: Name of the member variable used to reference the delegate instance.
        attr_name: Name of the attribute being delegated.
    """

    def __init__(self, delegate_name: str, attr_name: str) -> None:
        self.delegate_name: str = delegate_name
        self.attr_name: str = attr_name

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        else:
            # return instance.delegate.attr
            return getattr(self._get_delegate(instance), self.attr_name)

    def __set__(self, instance, value) -> None:
        # instance.delegate.attr = value
        setattr(self._get_delegate(instance), self.attr_name, value)

    def __delete__(self, instance) -> None:
        delattr(self._get_delegate(instance), self.attr_name)

    def _get_delegate(self, instance):
        return getattr(instance, self.delegate_name)

    def __str__(self) -> str:
        return ''
