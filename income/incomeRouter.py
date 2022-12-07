class IncomeRouter:
    """
    A router to control all database operations on models in the
    income application.
    """
    route_app_labels = {'income'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read income models go to income_db.
        """
        if model._meta.app_label == 'income':
            return 'income_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write income models go to income_db.
        """
        if model._meta.app_label == 'income':
            return 'income_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the income app is involved.
        """
        if obj1._meta.app_label == 'income' or \
           obj2._meta.app_label == 'income':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the income app only appears in the 'income_db'
        database.
        """
        if app_label == 'income':
            return db == 'income_db'
        return None