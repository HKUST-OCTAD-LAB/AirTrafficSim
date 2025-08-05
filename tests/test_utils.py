from airtrafficsim import hook


def test_hook() -> None:
    @hook
    def sub(a, b):  # type: ignore
        return a - b

    params = []

    @sub.intercept
    def sub_(original_fn, *args, **kwargs):  # type: ignore
        params.append((args, kwargs))
        return original_fn(*args, **kwargs)

    args = (3.1, 1.3)
    _ = sub(*args)
    assert (args, {}) in params
