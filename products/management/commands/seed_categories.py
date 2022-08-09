from django.core.management.base import BaseCommand
from products import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = ["신발", "의류", "패션잡화", "라이프", "테크"]
        for c in categories:
            models.Category.objects.create(name=c)
        self.stdout.write(self.style.SUCCESS("Categories created!"))
