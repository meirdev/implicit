# implicit

Implicit is a decorator that converts arguments to the correct type in the function signature.

## Example

```python
from implicit import implicit


@implicit
def add(a: int, b: int) -> int:
    return a + b


add("1", "2")  # 3
```

Use `exclude` to exclude a argument from being converted:

```python
from implicit import implicit


@implicit(exclude=["a"])
def add(a: int, b: int) -> int:
    return a + b


add("1", "2")  # TypeError: can only concatenate str (not "int") to str
```

# Disclaimer

This is only idea, don't use it.
