from django.core.management.base import BaseCommand
from rivers.models import River, Section
import csv


class Command(BaseCommand):
    args = ''
    help = 'Loads data'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)

    def _cull_sections(self):
        with open('section_list2.csv', newline='') as handle:
            spamreader = csv.reader(handle, delimiter=',', quotechar='"')
            for row in spamreader:
                section = Section.objects.get(url_id=row[3])
                if row[5] == '1':
                    # Move full grade info into description
                    desc = section.description
                    desc += '\n\n### Grade\n\n' + section.grade
                    section.description = desc

                    # Write clean grade into model
                    section.grade = row[6]

                    # Flag models with bad data
                    if row[7] == '1':
                        section.flag = True

                    # Update in db
                    section.save()

                else:
                    section.delete()

    def _cull_rivers(self):
        for river in River.objects.all():
            if Section.objects.filter(river=river).count() == 0:
                river.delete()

    def handle(self, *args, **options):
        action = options['action']
        if action == 'cull_sections':
            self._cull_sections()
        elif action == 'cull_rivers':
            self._cull_rivers()
        else:
            print('Unknown command.')
