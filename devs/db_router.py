# =====================================================
# Portal Database Router
# =====================================================

class PortalMenuRouter:

    MYSQL_MODELS = {
        "portalmenu",
        "usermenupermission",
    }

    # =================================================
    # Read
    # =================================================

    def db_for_read(self, model, **hints):

        if model._meta.model_name in self.MYSQL_MODELS:
            return "mysql"

        return None

    # =================================================
    # Write
    # =================================================

    def db_for_write(self, model, **hints):

        if model._meta.model_name in self.MYSQL_MODELS:
            return "mysql"

        return None

    # =================================================
    # Relation
    # =================================================

    def allow_relation(self, obj1, obj2, **hints):

        db1 = obj1._state.db
        db2 = obj2._state.db

        if db1 == "mysql" or db2 == "mysql":

            return db1 == db2

        return None

    # =================================================
    # Migration
    # =================================================

    def allow_migrate(
        self,
        db,
        app_label,
        model_name=None,
        **hints
    ):

        if model_name in self.MYSQL_MODELS:

            return db == "mysql"

        return None