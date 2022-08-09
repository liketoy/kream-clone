from django.db import models
from core.models import TimeStampedModel
from core.utils import upload_to


class Photo(TimeStampedModel):
    file = models.ImageField(upload_to=upload_to("posts", True))
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="photos")


class Post(TimeStampedModel):
    """Post Model Definition"""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )
    caption = models.TextField("내용")
    products = models.ManyToManyField(
        "products.Product", related_name="posts", blank=True
    )

    def __str__(self) -> str:
        return f"{self.user.username}의 STYLE"

    def count_products(self):
        return self.products.count()

    count_products.short_description = "상품 태그 수"
