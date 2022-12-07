class NotificationsRouter:
    """
    A router to control all database operations on models in the
    notifications application.
    """
    route_app_labels = {'notifications'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read notifications models go to notifications_db.
        """
        if model._meta.app_label == 'notifications':
            return 'notifications_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write notifications models go to notifications_db.
        """
        if model._meta.app_label == 'notifications':
            return 'notifications_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the notifications app is involved.
        """
        if obj1._meta.app_label == 'notifications' or \
           obj2._meta.app_label == 'notifications':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the notifications app only appears in the 'notifications_db'
        database.
        """
        if app_label == 'notifications':
            return db == 'notifications_db'
        return None