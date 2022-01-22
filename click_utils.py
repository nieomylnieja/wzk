import functools

from PIL import Image, UnidentifiedImageError
import click


class ImageParamType(click.ParamType):
    name = "Image"

    def convert(self, value, param, ctx):
        try:
            return Image.open(value, "r")
        except UnidentifiedImageError:
            self.fail(f"{value!r} file is not a valid image", param, ctx)
        except FileNotFoundError:
            self.fail(f"{value!r} file does not exist", param, ctx)


def rename_kwargs(**replacements):
    def actual_decorator(func):
        @functools.wraps(func)
        def decorated_func(*args, **kwargs):
            for internal_arg, external_arg in replacements.items():
                if external_arg in kwargs:
                    kwargs[internal_arg] = kwargs.pop(external_arg)
            return func(*args, **kwargs)

        return decorated_func

    return actual_decorator
