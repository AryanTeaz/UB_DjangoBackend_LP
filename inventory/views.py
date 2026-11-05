from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .permissions import ProductPermission
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related(
        "category", "supplier", "created_by"
    ).order_by("id")
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermission]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action != "list":
            return queryset

        category = self.request.query_params.get("category")
        creator = self.request.query_params.get("creator")

        if category:
            queryset = queryset.filter(category__name__icontains=category)

        if creator:
            queryset = queryset.filter(created_by__username__icontains=creator)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


login_view = obtain_auth_token


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def low_stock_list(request):
    if request.method != "GET":
        response = JsonResponse({"error": "Method not allowed"}, status=405)
        response["Allow"] = "GET"
        return response

    products = list(
        Product.objects.filter(stock__lt=10).values("id", "name", "stock")
    )
    return JsonResponse({"low_stock": products})


def product_list_html(request):
    return render(
        request,
        "inventory/product_list.html",
        {"products": Product.objects.all()},
    )