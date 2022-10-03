import inspect
import types
from typing import Callable, ParamSpec, Type, TypeVar

from .exceptions import ImplicitAbstractError, ImplicitCastError, ImplicitUnionError

T = TypeVar("T")


def cast(type_: Type[T], value: object) -> T:
    try:
        return type_(value)  # type: ignore[call-arg]
    except Exception as error:
        raise ImplicitCastError(error)


FP = ParamSpec("FP")
FT = TypeVar("FT")
Function = Callable[FP, FT]  # type: ignore[misc]


def implicit(function: Function | None = None, *, exclude: list[str] | None = None):
    def inner(function: Function) -> Function:
        signature = inspect.signature(function)
        params = signature.parameters

        exclude_: list[str] = [] if exclude is None else exclude

        for i in params:
            if i not in exclude_:
                type_ = params[i].annotation

                if isinstance(type_, types.UnionType):
                    raise ImplicitUnionError(str(params[i].name))

                elif hasattr(type_, "__abstractmethods__"):
                    raise ImplicitAbstractError(str(params[i].name))

        def wrapper(*args: FP.args, **kwargs: FP.kwargs) -> FT:  # type: ignore[type-var]
            args = dict(enumerate(args))

            check = lambda i, j, args: (
                j not in exclude_
                and not params[j].annotation is inspect._empty
                and not isinstance(args[i], params[j].annotation)
            )

            for i, j in zip(args, params):
                if check(i, j, args):
                    args[i] = cast(params[j].annotation, args[i])

            for i in kwargs:
                if check(i, i, kwargs):
                    kwargs[i] = cast(params[i].annotation, kwargs[i])

            args = list(args.values())

            return function(*args, **kwargs)

        return wrapper

    if function:
        return inner(function)

    return inner
