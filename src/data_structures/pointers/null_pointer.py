from __future__ import annotations

from .base_pointer import BasePointer
from src.null_vmobject import NullVMobject


class NullPointer(NullVMobject, BasePointer):
    """A null pointer"""
