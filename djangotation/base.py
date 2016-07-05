from collections import defaultdict
import weakref

from .exceptions import AnnotationDoesNotExist, AnnotationGroupDoesNotExist


class _empty:
    pass


class TationDjangoTationManager:
    """Internal class for djangotation representation on tations"""

    __slots__ = ['annotation', 'target_annotation_name', 'groups']

    def __init__(self, annotation, func_name, groups=None):

        if not hasattr(annotation, 'resolve_expression') and callable(annotation):
            self.annotation = annotation()
        else:
            self.annotation = annotation
        self.target_annotation_name = func_name
        self.groups = groups or []

    def __call__(self, model_instance):
        return PopulatedTationDjangoTationManager(
            target_annotation_name=self.target_annotation_name,
            model_instance=model_instance
        )


class PopulatedTationDjangoTationManager:
    __slots__ = ['model_instance', 'target_annotation_name']

    def __init__(self, target_annotation_name, model_instance):
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


class ModelDjangoTationManager:
    def __init__(self, model_class):
        self.model_class = model_class
        self.__groups = defaultdict(lambda: [])
        for tation_name in self.model_class.__dict__:
            tation = model_class.__dict__[tation_name]
            if hasattr(tation, '_djangotation'):
                self.setup_tation(tation, tation_name)
                self.register_groups(tation)

    def register_groups(self, tation):
        for group_name in tation._djangotation.groups:
            self.__groups[group_name].append(tation)

    def setup_tation(self, tation, name):
        if hasattr(tation, 'setup_tation'):
            tation.setup_tation(self.model_class, name)

    def tations_for_group(self, group_name):
        if group_name not in self.__groups:
            raise AnnotationGroupDoesNotExist(group_name)
        return [t for t in self.__groups[group_name]]


def register_djangotation_models(model):
    setup_model = False
    for name in model.__dict__:
        potential_tation = model.__dict__[name]
        if hasattr(potential_tation, '_djangotation'):
            setup_model = True
    if setup_model:
        model._djangotation = ModelDjangoTationManager(model)
