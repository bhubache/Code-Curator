from __future__ import annotations

class MyClassWithName:
    class_var: int = 5
    def __init__(self) -> None:
        self.arg_one: float = 5.0
        self.arg_two: str | None = None
        self.values: list[int] = [1, 2, 3, 4, 5]

    @my_deco
    def my_method(self, param_one: list[str | int], param_two: float) -> None:
        if not 0:
            ...

        print(f"Hello, you have provided {param_one} and {param_two}")

        local_variable = 10

        self.my_method(local_variable, param_two=17.0)
        raise ValueError(f"blah")

    @property
    def attr(self) -> int:
        return 5

    def my_second_method(self):
        print("bye")
        return
