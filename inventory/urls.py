from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register("products", views.ProductViewSet, basename="product")

urlpatterns = [
    path("login/", obtain_auth_token, name="api-login"),
    path("logout/", views.logout_view, name="api-logout"),
    path("low-stock/", views.low_stock_list, name="low-stock-list"),
    path("html/products/", views.product_list_html, name="product-list-html"),
    path("", include(router.urls)),
]