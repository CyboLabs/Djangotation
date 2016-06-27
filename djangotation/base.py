import weakref

from .exceptions import AnnotationDoesNotExist


class _empty:
    pass


class DjangoTation:
    """Internal class for djangotation representation"""

    __slots__ = ['annotation', 'func', 'target_annotation_name']

    def __init__(self, annotation, func):

        if not hasattr(annotation, 'resolve_expression') and callable(annotation):
            self.annotation = annotation()
        else:
            self.annotation = annotation
        self.func = func
        self.target_annotation_name = '__djangotation_' + func.__name__

    def __call__(self, model_instance):
        return PopulatedDjangoTation(
            annotation=self.annotation,
            func=self.func,
            model_instance=model_instance
        )


class PopulatedDjangoTation(DjangoTation):
    __slots__ = ['model_instance']

    def __init__(self, annotation, func, model_instance):
        super(PopulatedDjangoTation, self).__init__(annotation, func)
        self.model_instance = weakref.ref(model_instance)

    def model_instance_factory(self, model_instance):
        raise AttributeError

    @property
    def is_annotated(self):
        return getattr(self.model_instance, self.target_annotation_name, _empty) is not _empty

    @property
    def annotation_result(self):
        try:
            return getattr(self.model_instance, self.target_annotation_name)
        except AttributeError:
            pass
        raise AnnotationDoesNotExist()
