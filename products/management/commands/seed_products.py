import random
from django_seed import Seed
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from products import models


class Command(BaseCommand):

    help = "This command creates products"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many products you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        categories = models.Category.objects.all()
        brands = models.Brand.objects.all()
        seeder.add_entity(
            models.Product,
            number,
            {
                "category": lambda x: random.choice(categories),
                "brand": lambda x: random.choice(brands),
                "name_en": lambda x: seeder.faker.sentence(),
                "name_kr": lambda x: seeder.faker.bs(),
                "model_number": lambda x: seeder.faker.license_plate(),
                "released": lambda x: seeder.faker.date(),
                "color": lambda x: seeder.faker.color_name(),
                "released_price": lambda x: random.randint(100000, 1000000),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        for pk in created_clean:
            product = models.Product.objects.get(pk=pk)
            for i in range(1, random.randint(2, 3)):
                models.Photo.objects.create(
                    product=product,
                    image=f"product_photos/{random.randint(1, 35)}.webp",
                )

        self.stdout.write(self.style.SUCCESS(f"{number} products created!"))
