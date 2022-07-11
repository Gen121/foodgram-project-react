import csv
import os

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Заполнение БД тестовыми данными'

    csv_model = {
        'ingredients.csv': (
            Ingredient.objects.get_or_create,
            'dict(name=row[0], measurement_unit=row[1])',
            ),
        }

    def handle(self, *args, **kwargs):
        os.chdir(os.path.join('..', 'data'))
        for key in self.csv_model:
            with open(key, encoding='utf-8') as r_file:
                file_reader = csv.reader(r_file, delimiter=',')
                count = 0
                for row in file_reader:
                    if count == 0:
                        pass
                    else:
                        self.csv_model[key][0](**eval(self.csv_model[key][1]))
                    count += 1
                print(f'{key} содержит {count} строк.')
