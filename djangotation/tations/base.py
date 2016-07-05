from ..base import TationDjangoTationManager


class BaseTation:
    def __init__(self, *args, groups=None, **kwargs):
        self.__name__ = None
        self.db_annotate = None
        self.python_annotate = None
        self._djangotation = None
        self.model = None
        self.groups = groups
        self._args = args
        self._kwargs = kwargs

    def setup_tation(self, model_class, name):
        self.__name__ = name
        self.model = model_class

        self.db_annotate = self.setup_db_annotate(*self._args, **self._kwargs)
        self.python_annotate = self.setup_python_annotate(*self._args, **self._kwargs)

        self._djangotation = TationDjangoTationManager(self.db_annotate, name, groups=self.groups)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return instance.__dict__[self.__name__]
        except KeyError:
            return self.python_annotate(instance)

    def __set__(self, instance, value):
        if instance is not None:
            instance.__dict__[self.__name__] = value

    def setup_db_annotate(self, *args, **kwargs):
        raise NotImplementedError()

    def setup_python_annotate(self, *args, **kwargs):
        raise NotImplementedError()
