from django.shortcuts import render
from .models import River, Section, Level, Gauge
from django.db.models import Max
from rivers.forms import SectionForm
import sys
sys.path.insert(0, './rivers/lib')
import gauge_download  # this actually runs it lol


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
    gauges = Gauge.objects.all()
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

    def get(self, request, slug):
        # Create new section
        section = Section.objects.get(slug=slug)
        form = SectionForm( instance = section)

        args = {'form': form}

        return render(request, self.template_name, args)

    # def post(self, request, slug):
    #     # Edit existing section
    #     form = SectionForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         # post.user = request.user
    #         post.save()

    #         text = form.cleaned_data['post']
    #         return redirect('home:home')

    #     args = {'form': form, 'text': text}
    #     return render(request, self.template_name, args)
