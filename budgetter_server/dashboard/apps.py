from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        """
        Override ready() to handle signals
        """

        from dashboard.signals import transactions_created, transaction_post_save
        # Explicitly connect a signal handler.
        transactions_created.connect(transaction_post_save)
