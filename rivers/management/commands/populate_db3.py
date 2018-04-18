from django.core.management.base import BaseCommand
from rivers.models import River, Section


class Command(BaseCommand):
    args = ''
    help = 'Loads data'

    def _load_rivers(self):
        with open('section_list.csv', 'w') as handle:
            handle.write('River,Section,Class,Link,Keep,Grade')
            for section in Section.objects.all():
                if  section.url_id and section.url_id.isdigit():
                    base_url = "http://www.waterwaysguide.org.au/section-detail/" + section.url_id
                elif section.url_id:
                    base_url = "https://www.adventurepro.com.au/paddleaustralia/pa.cgi?action=details&id=" + section.url_id
                else:
                    base_url = ''

                handle.write('"{}", "{}", "{}","{}"\n'.format(
                    section.river.name, section.name, section.grade, base_url))

    def handle(self, *args, **options):
        self._load_rivers()
