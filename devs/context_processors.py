from .models import PortalMenu


# =====================================================
# Dynamic Portal Menu
# =====================================================

def portal_menu(request):

    if not request.user.is_authenticated:

        return {
            "portal_menu": []
        }

    menus = list(
        PortalMenu.objects.filter(
            is_active="Y"
        ).order_by(
            "display_order",
            "menu_id"
        )
    )

    menu_map = {}

    for menu in menus:

        menu.children_list = []

        menu_map[menu.menu_id] = menu

    root_menus = []

    for menu in menus:

        if menu.parent_id:

            parent = menu_map.get(
                menu.parent_id
            )

            if parent:

                parent.children_list.append(
                    menu
                )

        else:

            root_menus.append(menu)

    return {
        "portal_menu": root_menus
    }