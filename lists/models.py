from django.db import models
from core.models import TimeStampedModel


class List(TimeStampedModel):
    """관심상품 모델에 대한 정의"""

    products = models.ManyToManyField("products.Product", related_name="lists")
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="list"
    )

    def __str__(self) -> str:
        return f"{self.user}의 장바구니"

    def count_products(self):
        return self.products.count()

    count_products.short_description = "Number of Products"
