from django.apps import AppConfig


class HomepageConfig(AppConfig):
    name = 'homepage'
    from . import custom_webscraper

    def ready(self):
        from homepage import automat
        automat.start()