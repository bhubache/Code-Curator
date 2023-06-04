from __future__ import annotations
class RowFactory:
    """
    Factory abstracts creation details of rows
    """

    def __init__(self):
        self._builders = {}

    def register_builder(self, key: str, builder):
        self._builders[key] = builder

    def create(self, key: str, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)
