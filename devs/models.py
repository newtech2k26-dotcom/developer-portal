from django.db import models


# =====================================================
# Portal Menu
# =====================================================

class PortalMenu(models.Model):

    menu_id = models.AutoField(
        primary_key=True
    )

    menu_name = models.CharField(
        max_length=100
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    menu_url = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    has_page = models.CharField(
        max_length=1,
        default="N"
    )

    requires_permission = models.CharField(
        max_length=1,
        default="Y"
    )

    display_order = models.IntegerField(
        default=1
    )

    is_active = models.CharField(
        max_length=1,
        default="Y"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        managed = False

        db_table = "PY_PORTAL_MENU"

        ordering = [
            "display_order",
            "menu_id"
        ]

    def __str__(self):

        return self.menu_name

# =====================================================
# User Menu Permission
# =====================================================

class UserMenuPermission(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    user_id = models.IntegerField()

    menu_id = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.IntegerField(
        null=True,
        blank=True
    )

    class Meta:

        managed = False

        db_table = "PY_USER_MENU_PERMISSION"

    def __str__(self):

        return f"{self.user_id} - {self.menu_id}"