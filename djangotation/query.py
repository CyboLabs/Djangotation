from django.db.models.query import QuerySet as DjangoQuerySet

__all__ = (
    'QuerySet'
)


class QuerySet(DjangoQuerySet):

    def _apply_tation(self, tation):
        annotation_name = tation._djangotation.target_annotation_name
        annotation_expression = tation._djangotation.annotation
        return self.annotate(**{annotation_name: annotation_expression})

    def _apply_djangotation(self, annotation_name):
        try:
            annotation_function = self.model.__dict__[annotation_name]
        except KeyError:
            pass
        else:
            if getattr(annotation_function, '_djangotation', False):
                return self._apply_tation(annotation_function)
        raise AttributeError(annotation_name)

    def djangotation(self, *annotation_names):
        assert annotation_names
        current_queryset = self
        for annotation_name in annotation_names:
            current_queryset = self._apply_djangotation(annotation_name)
        return current_queryset

    def djangotation_group(self, group_name):
        current_queryset = self
        for tation in self.model._djangotation.tations_for_group(group_name):
            current_queryset = current_queryset._apply_tation(tation)
        return current_queryset

    def djangotation_groups(self, group_names):
        # TODO: this will cause duplicates. needs to be handled somehow!
        current_queryset = self
        for group_name in group_names:
            current_queryset = current_queryset.djangotation_group(group_name)
        return current_queryset
