import csv
import datetime

from django.core.management.base import BaseCommand
from recipes.models import Ingredient

csv_file = "ingredients.csv"
fields = ("name", "measurement_unit")


class Command(BaseCommand):
    help = "Load ingredients from csv file"

    def handle(self, *args, **options):
        print("старт импорта ингредиентов")
        start_time = datetime.datetime.now()
        try:
            with open(
                "recipes/management/data/ingredients.csv",
                "r",
                encoding="utf-8",
            ) as file:
                if not file:
                    raise FileNotFoundError
                reader = csv.DictReader(file, delimiter=",")
                for row in reader:
                    print(row)
                    Ingredient.objects.get_or_create(**row)
        except Exception as error:
            print(f"импорт завершен с ошибкой: {error}")
        print(f"импорт завершен за {datetime.datetime.now() - start_time}")
        self.stdout.write(self.style.SUCCESS("Импорт завершен"))
