from django.core.management.base import BaseCommand
from rivers.models import River, Section, Point
from pprint import pprint
import json
import os

access_point_list = os.listdir('rivers/management/commands/adv_pro')


class Command(BaseCommand):
    args = ''
    help = 'Loads data'

    def _load_rivers(self):
        filepath = 'rivers/management/commands/adv_pro'
        filelist = os.listdir(filepath)

        for filename in filelist:
            with open(filepath + '/' + filename, 'r') as handle:
                river = json.load(handle)
            # pprint(river)

            river_name = river['river_name']
            section_name = river['section_name']

            # Create river if required
            if River.objects.filter(name=river_name).count() == 0:
                new_river = River(name=river_name, description='')
                new_river.save()
                print('{} created'.format(river_name))
            else:
                print('River already exists')

            if Section.objects.filter(name=section_name).count() == 0:
                my_section = Section()
                my_section.name = section_name

                if 'Class:' in river and river['Class:']:
                    my_section.grade = river['Class:']
                else:
                    my_section.grade = 'Unknown'

                # Section Description
                description_text = ''
                description_fields = set(river.keys())
                exclude_fields = {'download_url', 'river_name', 'section_name',
                                  'Class:'}

                for field in description_fields:
                    if field in river and river[field]:
                        description_text += '\n\n### {}\n\n{}'.format(
                            field.title(), river[field])

                my_section.description = description_text
                my_section.url_id = river['download_url']
                my_section.river = River.objects.get(name=river_name)
                my_section.save()

                print('{} section has been created.'.format(section_name))
            else:
                print('{} section already exists.'.format(section_name))

    def handle(self, *args, **options):
        self._load_rivers()
