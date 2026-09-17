# =====================================================
# Portal Database Router
# =====================================================

class PortalMenuRouter:

    def db_for_read(self, model, **hints):

        if model.__name__ == "PortalMenu":
            return "mysql"

        return None

    def db_for_write(self, model, **hints):

        if model.__name__ == "PortalMenu":
            return "mysql"

        return None

    def allow_relation(
        self,
        obj1,
        obj2,
        **hints
    ):

        portal_models = {
            "PortalMenu"
        }

        if (
            obj1.__class__.__name__ in portal_models
            or
            obj2.__class__.__name__ in portal_models
        ):

            return True

        return None

    def allow_migrate(
        self,
        db,
        app_label,
        model_name=None,
        **hints
    ):

        if model_name == "portalmenu":

            return db == "mysql"

        return None