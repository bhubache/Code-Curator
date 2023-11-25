from __future__ import annotations

class MyClassWithName:
    def __init__(self) -> None:
        self.arg_one: float = 5.0
        self.arg_two: str = "name"

    def my_method(self, param_one: str, param_two: float) -> None:
        print(f"Hello, you have provided {param_one} and {param_two}")

    def my_second_method(self):
        print("bye")
        return
