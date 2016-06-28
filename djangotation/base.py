import weakref

from .exceptions import AnnotationDoesNotExist


class _empty:
    pass


class DjangoTation:
    """Internal class for djangotation representation"""

    __slots__ = ['annotation', 'target_annotation_name']

    def __init__(self, annotation, func_name):

        if not hasattr(annotation, 'resolve_expression') and callable(annotation):
            self.annotation = annotation()
        else:
            self.annotation = annotation
        self.target_annotation_name = func_name

    def __call__(self, model_instance):
        return PopulatedDjangoTation(
            annotation=self.annotation,
            target_annotation_name=self.target_annotation_name,
            model_instance=model_instance
        )


class PopulatedDjangoTation:
    __slots__ = ['annotation', 'model_instance', 'target_annotation_name']

    def __init__(self, annotation, target_annotation_name, model_instance):
        self.annotation = annotation
        self.target_annotation_name = target_annotation_name
        self.model_instance = weakref.ref(model_instance)

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
