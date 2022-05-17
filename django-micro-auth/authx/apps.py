from django.apps import AppConfig


class AuthxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authx'

    def ready(AppConfig):
    
        from django.contrib.admin.models import LogEntry
        from .models import NoLogEntryManager
        # Manager disabling logging logic
        LogEntry.objects = NoLogEntryManager(LogEntry)

        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        # disconnect update last login date
        user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')