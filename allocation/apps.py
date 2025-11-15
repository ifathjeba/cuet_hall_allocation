from django.apps import AppConfig

class AllocationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'allocation'

    def ready(self):
        import allocation.signals  # registers signals
