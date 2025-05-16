# session_requests/apps.py
from django.apps import AppConfig

class SessionRequestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'session_requests'

    def ready(self):
        import session_requests.signals  # This is CRUCIAL
