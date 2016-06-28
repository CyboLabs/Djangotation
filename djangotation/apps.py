from django.apps import AppConfig, apps
from .base import register_djangotation_models

class DjangoTationAppConfig(AppConfig):
    name = 'djangotation'
    verbose_name = "DjangoTation"

    def ready(self):
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                register_djangotation_models(model)
