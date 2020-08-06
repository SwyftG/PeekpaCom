from django.apps import AppConfig


class BasefunctionConfig(AppConfig):
    name = 'apps.basefunction'

    def ready(self):
        from .global_peekpa import init_peekpa
        init_peekpa()