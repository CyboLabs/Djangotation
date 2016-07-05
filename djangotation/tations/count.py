from django.db.models import Count

from .base import BaseTation


class CountTation(BaseTation):

    def setup_db_annotate(self, field_name):
        return Count(field_name)

    def setup_python_annotate(self, field_name):
        target_field_name = self.model._meta.get_field(field_name).get_accessor_name()
        def python_annotate(slf):
            related_set = getattr(slf, target_field_name)
            return related_set.count()

        return python_annotate
