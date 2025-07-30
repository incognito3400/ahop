from django.apps import AppConfig

class HotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Shop'

    def ready(self):
        import Shop.signals
