from functools import partial

from .constants import IS_ANNOTATION_ATTR_NAME, ANNOTATION_EXPRESSION_ATTR_NAME, ANNOTATION_TARGET_ATTR_NAME

__all__ = (
    'annotation',
    'cached_annotation'
)


class _empty:
    pass


class AnnotationProperty:
    def __init__(self, annotate, func):
        self.func = func
        if not hasattr(annotate, 'resolve_expression') and callable(annotate):
            annotate = annotate()

        setattr(self, ANNOTATION_EXPRESSION_ATTR_NAME, annotate)

        for wrapper_attr in ('__module__', '__name__', '__qualname__', '__doc__'):
            try:
                setattr(self, wrapper_attr, getattr(func, wrapper_attr))
            except AttributeError:
                pass

    def __get__(self, instance, owner):
        if instance is not None:
            annotation_target_attr = getattr(self.func, ANNOTATION_TARGET_ATTR_NAME, None)
            if annotation_target_attr:
                annotation_result = getattr(instance, annotation_target_attr, _empty)
                if annotation_result is not _empty:
                    return annotation_result
        return self.func(instance)

setattr(AnnotationProperty, IS_ANNOTATION_ATTR_NAME, True)


class CachedAnnotationProperty(AnnotationProperty):

    def __get__(self, instance, owner):
        if instance is None:
            return self
        res = instance.__dict__[self.func.__name__] = super().__get__(instance, owner)
        return res


def annotation(annotate):
    return partial(AnnotationProperty, annotate)


def cached_annotation(annotate):
    return partial(CachedAnnotationProperty, annotate)
