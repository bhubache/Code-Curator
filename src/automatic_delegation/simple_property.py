from __future__ import annotations


class SimpleProperty:
    def __init__(self):
        pass

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance._value

    def __set__(self, instance, value):
        instance._value = value
