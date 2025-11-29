from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'
    verbose_name = 'Dashboard'
    def ready(self):
        from django.conf import settings
        if getattr(settings, 'USE_AI_CATEGORIZATION', False):
            from utils.ai_categorizer import preload_model
            import threading
            
            # Run in a separate thread to avoid blocking startup completely,
            # but ensure it starts downloading immediately
            threading.Thread(target=preload_model, daemon=True).start()
