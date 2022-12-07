class CommitmentRouter:
    """
    A router to control all database operations on models in the
    commitment application.
    """
    route_app_labels = {'commitment'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read commitment models go to commitment_db.
        """
        if model._meta.app_label == 'commitment':
            return 'commitment_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write commitment models go to commitment_db.
        """
        if model._meta.app_label == 'commitment':
            return 'commitment_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the commitment app is involved.
        """
        if obj1._meta.app_label == 'commitment' or \
           obj2._meta.app_label == 'commitment':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the commitment app only appears in the 'commitment_db'
        database.
        """
        if app_label == 'commitment':
            return db == 'commitment_db'
        return None