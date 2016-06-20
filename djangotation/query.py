from django.db.models.query import QuerySet as DjangoQuerySet

from .constants import IS_ANNOTATION_ATTR_NAME, ANNOTATION_EXPRESSION_ATTR_NAME, ANNOTATION_TARGET_ATTR_NAME


__all__ = (
    'QuerySet'
)


class QuerySet(DjangoQuerySet):

    def __getattr__(self, item):
        if item.startswith('annotate_'):
            annotation_name = item[9:]
            try:
                annotation_function = self.model.__dict__[annotation_name]
            except KeyError:
                pass
            else:
                if getattr(annotation_function, IS_ANNOTATION_ATTR_NAME, False):
                    annotation_name = '__' + annotation_name
                    annotation_expression = getattr(annotation_function, ANNOTATION_EXPRESSION_ATTR_NAME, None)
                    if annotation_expression:
                        ret = lambda: self.annotate(**{annotation_name: annotation_expression})
                        setattr(annotation_function, ANNOTATION_TARGET_ATTR_NAME, annotation_name)
                        return ret
        raise AttributeError(item)
