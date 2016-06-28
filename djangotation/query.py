from django.db.models.query import QuerySet as DjangoQuerySet

__all__ = (
    'QuerySet'
)


class QuerySet(DjangoQuerySet):

    def djangotation(self, annotation_name):
        try:
            annotation_function = self.model.__dict__[annotation_name]
        except KeyError:
            pass
        else:
            if getattr(annotation_function, '_djangotation', False):
                annotation_name = annotation_function._djangotation.target_annotation_name
                annotation_expression = annotation_function._djangotation.annotation
                return self.annotate(**{annotation_name: annotation_expression})
        raise AttributeError(annotation_name)

    def djangotation_group(self, group_name):
        pass

    def djangotation_groups(self, group_names):
        pass
