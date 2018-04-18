from django.core.management.base import BaseCommand
from rivers.models import River, Section, Point
from pprint import pprint
import json
import os

access_point_list = os.listdir('rivers/management/commands/json_points')

def get_data(point_num):
    if str(point_num)+'.json' in access_point_list:
        with open('rivers/management/commands/json_points/{}.json'.format(point_num),'r') as handle:
            return json.load(handle)
    else:
        return False

class Command(BaseCommand):
    args = ''
    help = 'Loads data'

    def _load_rivers(self):
        filepath = 'rivers/management/commands/json'
        filelist = os.listdir(filepath)

        for filename in filelist:
            with open(filepath + '/' + filename, 'r') as handle:
                river = json.load(handle)
            river_name = river['WATERWAY']

            # Create river if required
            if River.objects.filter(name=river_name).count() == 0:
                new_river = River(name=river_name, description='')
                new_river.save()
                print('New river created')
            else:
                print('River already exists')

            # Get put in and takeout info if avaliable
            put_in_data, take_out_data = None, None
            if 'ENTRY POINT' in river and river['ENTRY POINT'] and river['ENTRY POINT'][:20] == '/accesspoint-detail/':
                put_in_num = river['ENTRY POINT'][20:]
                put_in_data = get_data(put_in_num)
            else:
                continue

            if 'EXIT POINT' in river and river['EXIT POINT'] and river['EXIT POINT'][:20] == '/accesspoint-detail/':
                take_out_num = river['EXIT POINT'][20:]
                take_out_data = get_data(take_out_num)
            else:
                continue

            if not put_in_data or not take_out_data or not'title' in put_in_data or not 'title' in take_out_data :
                print('Section end points are invalid')
                continue

            section_name = '{} to {}'.format(
                put_in_data['title'], take_out_data['title'])

            # Begin creating instance
            if Section.objects.filter(name=section_name).count() == 0:
                my_section = Section()
                # Section name
                my_section.name = section_name
                # Section grade
                if  river['HIGHEST GRADE']:
                    my_section.grade = river['HIGHEST GRADE']
                else:
                    my_section.grade = 'Unknown'

                # Section Description
                if river['Description']:
                    description_text = river['Description']
                else:
                    description_text = ''

                # Add other fields into the description contents
                description_fields = ['Hot tip', 'Gradient', 'Portage?',
                                      'Shuttle Length', 'TRIP DURATION', 'TRIP LENGTH', 'AVERAGE GRADE']
                for field in description_fields:
                    if field in river and river[field]:
                        description_text += '\n\n### {}\n\n{}'.format(
                            field.title(), river[field])

                my_section.description = description_text
                my_section.url_id = river['URL_ID']
                my_section.river = River.objects.get(name=river_name)
                my_section.save()
                print('{} section has been created.'.format(section_name))
            else:
                print('{} section already exists.'.format(section_name))

            # Deal with special case where both points are the same spot
            if put_in_data['Latitude'] == take_out_data['Latitude'] and put_in_data['Longitude'] == take_out_data['Longitude']:
                put_in_data['Latitude'] = float(
                    put_in_data['Latitude']) + 0.00001
            # Create points for section
            current_section = Section.objects.get(name=section_name)

            # put in point
            if Point.objects.filter(section=current_section, point_type=1).count() == 0:
                put_in = Point(name=put_in_data['title'], latitude=put_in_data[
                               'Latitude'], longditude=put_in_data['Longitude'], section=current_section, point_type=1)
                put_in.save()
            # take out point
            if Point.objects.filter(section=current_section, point_type=0).count() == 0:
                take_out = Point(name=take_out_data['title'], latitude=take_out_data[
                                 'Latitude'], longditude=take_out_data['Longitude'], section=current_section, point_type=0)
                take_out.save()

            print('Created put in and take out points.')

    def handle(self, *args, **options):
        self._load_rivers()
