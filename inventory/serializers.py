from rest_framework import serializers

from .models import Category, Product, Supplier


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    supplier_id = serializers.PrimaryKeyRelatedField(
        source="supplier",
        queryset=Supplier.objects.all(),
        required=False,
        allow_null=True,
    )
    category = serializers.StringRelatedField(read_only=True)
    supplier = serializers.StringRelatedField(read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True, allow_null=True
    )

    class Meta:
        model = Product
        fields = (
            "id", "name", "sku", "stock", "price",
            "category_id", "category", "supplier_id", "supplier",
            "created_by", "created_by_username", "created_at", "updated_at",
        )
        read_only_fields = ("created_by", "created_at", "updated_at")
        extra_kwargs = {
            "stock": {"min_value": 0},
            "price": {"min_value": 0},
        }