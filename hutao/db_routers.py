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
        app1 = obj1._meta.app_label
        app2 = obj2._meta.app_label
        model1 = obj1._meta.model_name
        model2 = obj2._meta.model_name
        # Cho phép quan hệ giữa company.Employee và auth.User
        if (app1 == 'company' and model1 == 'employee' and app2 == 'auth' and model2 == 'user') or \
           (app2 == 'company' and model2 == 'employee' and app1 == 'auth' and model1 == 'user'):
            return True
        # Cho phép quan hệ giữa homa.Resident và auth.User
        if (app1 == 'homa' and model1 == 'resident' and app2 == 'auth' and model2 == 'user') or \
           (app2 == 'homa' and model2 == 'resident' and app1 == 'auth' and model1 == 'user'):
            return True
        # Chỉ cho phép quan hệ nếu cùng app hoặc cùng nhóm (admin với admin, homa với homa, company với company)
        if app1 == app2:
            return True
        # Cho phép quan hệ giữa các app không phải homa/company (ví dụ: admin với auth)
        if app1 not in ['homa', 'company'] and app2 not in ['homa', 'company']:
            return True
        # Ngăn homa/company truy cập admin hoặc ngược lại
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'homa':
            return db == 'homa'
        elif app_label == 'company':
            return db == 'company'
        elif db == 'default':
            # Django admin sử dụng default database
            return True
        return False
