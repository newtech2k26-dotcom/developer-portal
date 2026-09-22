from .models import PortalMenu, UserMenuPermission


# =====================================================
# Dynamic Portal Menu
# =====================================================

def portal_menu(request):

    # -------------------------------------------------
    # Not Logged In
    # -------------------------------------------------

    if not request.user.is_authenticated:

        return {
            "portal_menu": []
        }

    # -------------------------------------------------
    # Get All Active Menus
    # -------------------------------------------------

    menus = list(
        PortalMenu.objects
        .filter(
            is_active="Y"
        )
        .order_by(
            "display_order",
            "menu_id"
        )
    )

    # -------------------------------------------------
    # Create Menu Map
    # -------------------------------------------------

    menu_map = {}

    for menu in menus:

        menu.children_list = []

        menu_map[menu.menu_id] = menu

    # -------------------------------------------------
    # Get User Permissions
    # -------------------------------------------------

    permitted_menu_ids = set(
        UserMenuPermission.objects
        .filter(
            user_id=request.user.id
        )
        .values_list(
            "menu_id",
            flat=True
        )
    )

    # -------------------------------------------------
    # Default Menus
    #
    # Home  = 1
    # About = 19
    # -------------------------------------------------

    permitted_menu_ids.update({
        1,
        19
    })

    # -------------------------------------------------
    # Superuser
    #
    # Superuser can see all active menus.
    # -------------------------------------------------

    if request.user.is_superuser:

        permitted_menu_ids = {
            menu.menu_id
            for menu in menus
        }

    # -------------------------------------------------
    # Add Public Menus
    #
    # Menus which do not require permission
    # are visible to every logged-in user.
    # -------------------------------------------------

    for menu in menus:

        if menu.requires_permission != "Y":

            permitted_menu_ids.add(
                menu.menu_id
            )

    # -------------------------------------------------
    # Add Parent Menus
    #
    # If a user has permission for a child menu,
    # all of its parents must also be visible.
    #
    # Example:
    #
    # Reports
    #     Sales
    #         Daily Sales
    #
    # If user has Daily Sales permission:
    #
    # Reports
    #     Sales
    #         Daily Sales
    # -------------------------------------------------

    menu_ids_to_show = set(
        permitted_menu_ids
    )

    for menu_id in list(permitted_menu_ids):

        current_menu = menu_map.get(
            menu_id
        )

        while current_menu:

            parent_id = current_menu.parent_id

            if not parent_id:
                break

            menu_ids_to_show.add(
                parent_id
            )

            current_menu = menu_map.get(
                parent_id
            )

    # -------------------------------------------------
    # Build Menu Hierarchy
    #
    # Only menus allowed for this user are included.
    # -------------------------------------------------

    root_menus = []

    for menu in menus:

        # Skip menus that user cannot see
        if menu.menu_id not in menu_ids_to_show:

            continue

        # Root menu
        if not menu.parent_id:

            root_menus.append(
                menu
            )

            continue

        # Child menu
        parent = menu_map.get(
            menu.parent_id
        )

        if parent:

            # Only attach to parent if parent
            # is also allowed to be displayed.
            if parent.menu_id in menu_ids_to_show:

                parent.children_list.append(
                    menu
                )

    # -------------------------------------------------
    # Return Existing Context Variable
    #
    # IMPORTANT:
    # base.html already uses:
    #
    # portal_menu
    # -------------------------------------------------

    return {
        "portal_menu": root_menus
    }