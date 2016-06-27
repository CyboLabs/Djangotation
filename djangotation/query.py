from django.db.models.query import QuerySet as DjangoQuerySet

__all__ = (
    'QuerySet'
)


class QuerySet(DjangoQuerySet):

    def set_annotation(self, annotation_name):
        try:
            annotation_function = self.model.__dict__[annotation_name]
        except KeyError:
            pass
        else:
            if getattr(annotation_function, '_djangotation', False):
                annotation_name = annotation_function._djangotation.target_annotation_name
                annotation_expression = annotation_function._djangotation.annotation
                return lambda: self.annotate(**{annotation_name: annotation_expression})
        raise AttributeError(annotation_name)

    def __getattr__(self, item):
        if item.startswith('annotate_'):
            annotation_name = item[9:]
            return self.set_annotation(annotation_name)
        raise AttributeError(item)
