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
        self._djangotation = DjangoTation(annotate, func)
        wrap_class_as_func(self, func)

    def __get__(self, instance, owner):
        if instance is not None:
            djangotation = self._djangotation(instance)
            try:
                return djangotation.annotation_result
            except AnnotationDoesNotExist:
                pass
        return self._djangotation.func(instance)


class CachedAnnotationProperty(AnnotationProperty):

    def __get__(self, instance, owner):
        if instance is None:
            return self
        res = instance.__dict__[self._djangotation.func.__name__] = super(CachedAnnotationProperty, self).__get__(instance, owner)
        return res


def annotation(annotate):
    return partial(AnnotationProperty, annotate)


def cached_annotation(annotate):
    return partial(CachedAnnotationProperty, annotate)