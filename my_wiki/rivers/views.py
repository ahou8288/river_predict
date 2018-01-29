from django.shortcuts import render, redirect
from .models import River, Section, Level, Gauge, Interested, Point
from django.db.models import Max
from rivers.forms import SectionForm, RiverForm
from django.forms import modelformset_factory
import sys
sys.path.insert(0, './rivers/lib')
# import gauge_download  # this actually runs it lol
from django.utils import timezone
from django.contrib import messages 


from django.views.generic import TemplateView

# Create your views here.


def index(request):
    return render(request, 'home.html', {'PAGE_TITLE': 'Homepage'})


def rivers(request):
    output = []
    rivers = River.objects.all()
    for river in rivers:
        sections = Section.objects.filter(river=river)
        output.append({
            'name': river.name,
            'sections': sections
        })
    return render(request, 'rivers.html', {'rivers': output, 'PAGE_TITLE': 'Rivers'})


def levels(request):
    if request.user.is_anonymous:
        gauges = Gauge.objects.all()
    else:
        user_gauges = Interested.objects.filter(user=request.user)
        print(user_gauges)
        gauges = [i.gauge for i in user_gauges]

    data = []
    for gauge in gauges:
        latest_time = Level.objects.filter(
            gauge=gauge).aggregate(time=Max('time'))['time']
        try:
            level = Level.objects.get(gauge=gauge, time=latest_time)
            data.append({
                'name': gauge.name,
                'type': level.unit,
                'value': level.value,
                'time': level.time
            })
        except:
            pass
    return render(request, 'levels.html', {'PAGE_TITLE': 'Levels', 'data': data})


def sections(request, slug):
    section = Section.objects.get(slug=slug)
    river = section.river

    return render(request, 'section.html', {'PAGE_TITLE': section.name, 'section': section, 'river': river})


class SectionView(TemplateView):
    template_name = 'form.html'

    def get(self, request, slug=None):

        # Create formset
        PointFormSet = modelformset_factory(Point, fields=(
            'latitude', 'longditude', 'point_type'), min_num=2, max_num=2)

        # Deal with whether there is a section specified
        if slug:
            section = Section.objects.get(slug=slug)
            point_query = Point.objects.filter(section=section)
            river_form = None
        else:
            section = Section()
            section.description = "### Placeholder title\n"
            point_query = Point.objects.none()
            river_form = RiverForm()

        # Create the forms
        form = SectionForm(instance=section)
        point_formset = PointFormSet(queryset=point_query)

        # Render the view
        args = {'form': form, 'formset': point_formset, 'river_form':river_form}
        return render(request, 'create_section.html', args)

    def post(self, request, slug=None):

        if not slug:
            form = SectionForm(request.POST)
        else:
            # Save edit section
            slug_section = Section.objects.get(slug=slug)
            form = SectionForm(request.POST, instance=slug_section)


        if form.is_valid():
            changed_section = form.save(commit=False)
            if not request.user.is_anonymous:
                changed_section.recent_editor = request.user
            changed_section.last_edit_time = timezone.now()
            changed_section.save()

            PointFormSet = modelformset_factory(Point, fields=(
                'latitude', 'longditude', 'point_type'), min_num=2, max_num=2)
            point_formset = PointFormSet(request.POST)
            if point_formset.is_valid():
                points = point_formset.save(commit=False)
                for point in points:
                    print('Point is valid. Saving.')
                    point.section=changed_section
                    point.save()
            else:
                print('Invalid formset')
                messages.error(request, "Error")
                print(point_formset.errors)

            return redirect('view section', slug=changed_section.slug)
        else:
            # Form is not valid
            text = 'Form is invalid'
            args = {'form': form, 'text': text}
            return render(request, self.template_name, args)


class RiverView(TemplateView):
    template_name = 'form.html'

    def get(self, request):
        form = RiverForm()
        args = {'form': form}

        return render(request, self.template_name, args)

    def post(self, request):
        form = RiverForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('invalid form')
        return redirect('home')
