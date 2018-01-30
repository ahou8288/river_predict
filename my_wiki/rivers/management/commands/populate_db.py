from django.core.management.base import BaseCommand
from rivers.models import River
import json


class Command(BaseCommand):
    args = ''
    help = 'Loads data'

    def _load_rivers(self):
        with open('', 'r') as handle:
            data = json.load(handle)

        for river in data:
            river_name = river['WATERWAY']
            if River.objects.filter(name=river_name).count() == 0:
                new_river = River(name = river_name, description = '' )
            print('{} has been added.'.format(river_name))
            break
        print('loading rivers')

    def handle(self, *args, **options):
        self._load_rivers()
