from django.apps import AppConfig


class WatcherConfig(AppConfig):
    name = 'watcher'

    def ready(self):
        from .libs.search_helpers import updater
        updater()
