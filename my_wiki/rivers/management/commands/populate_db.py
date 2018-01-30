from django.core.management.base import BaseCommand
from rivers.models import River
import json
import os
from pprint import pprint

class Command(BaseCommand):
    args = ''
    help = 'Loads data'

    def _load_rivers(self):
        filepath = 'rivers/management/commands/json'
        filelist = os.listdir(filepath)

        for filename in filelist:
            with open(filepath + '/' + filename, 'r') as handle:
                river = json.load(handle)
            pprint(river)
            river_name = river['WATERWAY']

            #Create river if required
            if River.objects.filter(name=river_name).count() == 0:
                new_river = River(name = river_name, description = '' )
                new_river.save()
                print('New river created')
            else:
                print('River already exists')

    def handle(self, *args, **options):
        self._load_rivers()
