from django.urls import path
from products import views


app_name = "products"

urlpatterns = [
    path("", views.PostList.as_view(), name="list"),
    path("<int:pk>", views.ProductDetail.as_view(), name="detail"),
    path("search", views.SearchView.as_view(), name="search"),
]
