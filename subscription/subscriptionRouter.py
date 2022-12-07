class SubscriptionRouter:
    """
    A router to control all database operations on models in the
    subscription application.
    """
    route_app_labels = {'subscription'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read subscription models go to subscription_db.
        """
        return True
        # if model._meta.app_label == 'subscription':
        #     return 'subscription_db'
        # return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write subscription models go to subscription_db.
        """
        if model._meta.app_label == 'subscription':
            return 'subscription_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the subscription app is involved.
        """
        return True
        # if obj1._meta.app_label == 'subscription' or \
        #    obj2._meta.app_label == 'subscription':
        #    return True
        # return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the subscription app only appears in the 'subscription_db'
        database.
        """
        return True
        # if app_label == 'subscription':
        #     return db == 'subscription_db'
        # return None