
# Note: Should be indicated in settings, and configure DATABASES and DATABASE_ROUTERS
# the mysql server should be runing be for try to run the following commands.
# CMDand Terminal Commands: 
# 1. python manage.py makemigrations or python manage.py makemigrations peshang_petrol   
# 2. python manage.py migrate --database= auth_bd  
# 3. python manage.py migrate --database=peshang_petrol_db
# 4. python manage.py migrate --database=awat_petrol_db
# Authentication Router saved in sqlLite db which is taked as defualt db
# sometimes when we try to migrate there is not changed in mysql server, so to solve this issue we need to remove 000x.initial.py in migrations folder
# and remove mysql db in sql server, but we must beware !! while our db contains data!! espacially when we add new fields to database table!!

class AuthRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    route_app_labels = {"auth", "contenttypes","admin","sessions"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "auth_db"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "auth_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            return db == "auth_db"
        return None

# Peshang Petrol Station is saved in MySQL server db
class PeshangRouter:

    route_app_labels = {"peshang_petrol"}

    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return "peshang_petrol_db"
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return "peshang_petrol_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):

        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label in self.route_app_labels:
            return db == "peshang_petrol_db"
        return None 
       
# Awat Petrol Station is saved in MySQL server db
class AwatRouter:

    route_app_labels = {"awat_petrol"}

    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return "awat_petrol_db"
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return "awat_petrol_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):

        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label in self.route_app_labels:
            return db == "awat_petrol_db"
        return None        