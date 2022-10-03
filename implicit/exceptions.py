class ImplicitUnionError(Exception):
    def __init__(self, param: str) -> None:
        super().__init__(f"Union types are not supported ({param})")


class ImplicitAbstractError(Exception):
    def __init__(self, param: str) -> None:
        super().__init__(f"Abstract types are not supported ({param})")


class ImplicitCastError(Exception):
    pass
