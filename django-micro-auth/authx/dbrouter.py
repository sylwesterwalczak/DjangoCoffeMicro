from django.conf import settings


class AuthRouter:

    def db_for_read(self, model, **hints):
        if model._meta.db_table == settings.AUTH_USER_TABLE:
            return settings.AUTH_DB
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.db_table == settings.AUTH_USER_TABLE or obj2._meta.db_table == settings.AUTH_USER_TABLE:
            return False

    
