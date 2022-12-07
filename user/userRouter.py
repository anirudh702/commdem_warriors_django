

from django.db import connection, connections


class UserRouter:
    """
    A router to control all database operations on models in the
    user application.
    """
    route_app_labels = {'user','commitment'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read user models go to user_db.
        """
        return True
        # if model._meta.app_label == 'user':
        #     return 'user_db'
        # return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write user models go to user_db.
        """
        if model._meta.app_label == 'user':
            return 'user_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the user app is involved.
        """
        return True
        # if obj1._meta.app_label == 'user' or \
        #    obj2._meta.app_label == 'subscription':
        #    return True
        # return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the user app only appears in the 'user_db'
        database.
        """
        return True
        # if app_label == 'user':
        #     return db == 'user_db'
        # return None

    # @classmethod
    # def refresh_view(cl):
    #         with connection.cursor() as cursor:
    #             cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY materialized_user_model")
    
    # @classmethod
    # def create_user_materialized_view(cl):
    #         with connection.cursor() as cursor:
    #             # cursor = connections['commitment_db'].cursor()
    #             cursor.execute("CREATE MATERIALIZED VIEW materialized_user_model as select * from public.user_usermodel")

