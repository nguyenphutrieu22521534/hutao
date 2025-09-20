class DatabaseRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'homa':
            return 'homa'
        elif model._meta.app_label == 'company':
            return 'company'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'homa':
            return 'homa'
        elif model._meta.app_label == 'company':
            return 'company'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'homa', 'company'}
        if obj1._state.db in db_set or obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'homa':
            return db == 'homa'
        elif app_label == 'company':
            return db == 'company'
        elif db == 'default':
            # Django admin sử dụng default database
            return True
        return False
