from django.db.models.manager import Manager as DjangoManager

from .query import QuerySet

__all__ = (
    'Manager'
)


class Manager(DjangoManager.from_queryset(QuerySet)):
    pass
