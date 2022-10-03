from abc import ABC
from pathlib import Path

import pytest

from implicit import implicit
from implicit.exceptions import ImplicitAbstractError, ImplicitUnionError


def test_function_args():
    @implicit
    def foo(x: Path):
        assert isinstance(x, Path)

    foo("aaa")  # ignore: type


def test_function_kwargs():
    @implicit
    def foo(x: Path):
        assert isinstance(x, Path)

    foo(x="aaa")  # ignore: type


def test_function_args_and_kwargs():
    @implicit
    def foo(x: int, y: int):
        assert isinstance(x, int) and x == 12
        assert isinstance(y, int) and y == 45

    foo(12.3, y="45")  # ignore: type


def test_method():
    class Foo:
        @implicit
        def bar(self, x: Path):
            assert isinstance(x, Path)

    foo = Foo()
    foo.bar("aaa")  # ignore: type


def test_exclude():
    @implicit(exclude=["x"])
    def foo(x: int, y: int):
        assert isinstance(x, float) and x == 12.3
        assert isinstance(y, int) and y == 45

    foo(12.3, y="45")  # ignore: type


def test_abstract_type():
    class Abstract(ABC):
        pass

    with pytest.raises(ImplicitAbstractError):

        @implicit
        def foo(x: Abstract):
            pass

    @implicit(exclude=["x"])
    def foo(x: Abstract):
        pass


def test_union_type():
    with pytest.raises(ImplicitUnionError):

        @implicit
        def foo(x: int | float):
            pass

    @implicit(exclude=["x"])
    def foo(x: int | float):
        pass
