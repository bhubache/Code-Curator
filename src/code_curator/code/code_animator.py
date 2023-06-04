from __future__ import annotations

from .custom_code import CustomCode


class CodeAnimator:
    def __init__(self, code: CustomCode):
        self._code: CustomCode = code
