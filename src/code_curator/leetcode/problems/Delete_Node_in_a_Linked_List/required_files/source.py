class MyFirstClass:
    def __init__(self) -> None:
        self.arg_one: int = 5

    def my_method(self, param_one: str, param_two: float) -> None:
        print(f"Hello, you've provided {param_one} and {param_two}")
        # Remove this line