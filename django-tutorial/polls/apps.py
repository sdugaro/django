from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'
    email = 'info@polls.com'

    def ready(self):
        from .signals import log_request
        print('--> loaded signal handlers')

