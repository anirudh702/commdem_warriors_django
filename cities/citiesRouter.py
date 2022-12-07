class CitiesRouter:
    """
    A router to control all database operations on models in the
    cities application.
    """
    route_app_labels = {'cities'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read cities models go to cities_db.
        """
        if model._meta.app_label == 'cities':
            return 'cities_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write cities models go to cities_db.
        """
        if model._meta.app_label == 'cities':
            return 'cities_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the cities app is involved.
        """
        if obj1._meta.app_label == 'cities' or \
           obj2._meta.app_label == 'cities':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the cities app only appears in the 'cities_db'
        database.
        """
        if app_label == 'cities':
            return db == 'cities_db'
        return None