from __future__ import annotations

from null_vmobject import NullVMobject

from .base_pointer import BasePointer


class NullPointer(NullVMobject, BasePointer):
    """A null pointer"""
