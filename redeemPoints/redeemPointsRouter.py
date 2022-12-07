class RedeemPointsRouter:
    """
    A router to control all database operations on models in the
    redeemPoints application.
    """
    route_app_labels = {'redeemPoints'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read redeemPoints models go to redeemPoints_db.
        """
        if model._meta.app_label == 'redeemPoints':
            return 'redeemPoints_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write redeemPoints models go to redeemPoints_db.
        """
        if model._meta.app_label == 'redeemPoints':
            return 'redeemPoints_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the redeemPoints app is involved.
        """
        if obj1._meta.app_label == 'redeemPoints' or \
           obj2._meta.app_label == 'redeemPoints':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the redeemPoints app only appears in the 'redeemPoints_db'
        database.
        """
        if app_label == 'redeemPoints':
            return db == 'redeemPoints_db'
        return None