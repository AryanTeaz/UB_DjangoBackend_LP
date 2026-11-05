from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProductPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        if view.action == "destroy":
            return (
                user.groups.filter(name="Inventory Admin").exists()
                and user.has_perm("inventory.delete_product")
            )

        permission = {
            "create": "inventory.add_product",
            "update": "inventory.change_product",
            "partial_update": "inventory.change_product",
        }.get(view.action)

        return bool(
            permission
            and user.groups.filter(name__in=["Staff", "Inventory Admin"]).exists()
            and user.has_perm(permission)
        )