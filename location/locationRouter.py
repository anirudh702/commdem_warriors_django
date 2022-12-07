class LocationRouter:
    """
    A router to control all database operations on models in the
    location application.
    """
    route_app_labels = {'location'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read location models go to location_db.
        """
        if model._meta.app_label == 'location':
            return 'location_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write location models go to location_db.
        """
        if model._meta.app_label == 'location':
            return 'location_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the location app is involved.
        """
        if obj1._meta.app_label == 'location' or \
           obj2._meta.app_label == 'location':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the location app only appears in the 'location_db'
        database.
        """
        if app_label == 'location':
            return db == 'location_db'
        return None