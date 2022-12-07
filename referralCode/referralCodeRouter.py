class ReferralCodeRouter:
    """
    A router to control all database operations on models in the
    referralCode application.
    """
    route_app_labels = {'referralCode'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read referralCode models go to referralCode_db.
        """
        if model._meta.app_label == 'referralCode':
            return 'referralCode_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write referralCode models go to referralCode_db.
        """
        if model._meta.app_label == 'referralCode':
            return 'referralCode_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the referralCode app is involved.
        """
        if obj1._meta.app_label == 'referralCode' or \
           obj2._meta.app_label == 'referralCode':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the referralCode app only appears in the 'referralCode_db'
        database.
        """
        if app_label == 'referralCode':
            return db == 'referralCode_db'
        return None