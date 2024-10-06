from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        """
        Override ready() to handle signals
        """

        import dashboard.signals
