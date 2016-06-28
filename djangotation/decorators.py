from functools import partial

from .base import DjangoTation
from .exceptions import AnnotationDoesNotExist


__all__ = (
    'annotation',
    'cached_annotation'
)


def wrap_class_as_func(instance, func):
    for wrapper_attr in ('__module__', '__name__', '__qualname__', '__doc__'):
        try:
            setattr(instance, wrapper_attr, getattr(func, wrapper_attr))
        except AttributeError:
            pass


class AnnotationProperty:
    def __init__(self, annotate, func):
        self.func = func
        self._djangotation = DjangoTation(annotate, func.__name__)
        wrap_class_as_func(self, func)

    def __get__(self, instance, owner):
        return self.func(instance)

    def __set__(self, instance, value):
        if instance is not None:
            instance.__dict__[self.func.__name__] = value


class CachedAnnotationProperty(AnnotationProperty):

    def __get__(self, instance, owner):
        if instance is None:
            return self
        res = instance.__dict__[self.func.__name__] = super(CachedAnnotationProperty, self).__get__(instance, owner)
        return res


def annotation(annotate):
    return partial(AnnotationProperty, annotate)


def cached_annotation(annotate):
    return partial(CachedAnnotationProperty, annotate)
