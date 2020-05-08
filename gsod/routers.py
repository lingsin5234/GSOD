class GSODRouter:
    """
    A router to control all database operations
    on models in the gsod app
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'gsod':
            return 'gsod_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'gsod':
            return 'gsod_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if a model is in the gsod
        if obj1._meta.app_label == 'gsod' or obj2._meta.app_label == 'gsod':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'gsod':
            return db == 'gsod_db'
        # allows other apps to go to default database
        return None
