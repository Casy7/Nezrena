from django.apps import AppConfig
from .modules.imap_modules.imap_subscription import IMAPSubscription


class NezrenaappConfig(AppConfig):    
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NezrenaApp'
    def ready(self):
        s1 = IMAPSubscription()

        notification_flag = True
