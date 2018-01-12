from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class River(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Gauge(models.Model):
    name = models.CharField(max_length=100)
    download_id = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Level(models.Model):
    READING_TYPES = (
        (0, 'level'),
        (1, 'discharge'),
    )
    gauge = models.ForeignKey(Gauge, on_delete=models.CASCADE)
    value = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    unit = models.CharField(max_length=1, choices=READING_TYPES)


class Section(models.Model):
    # Section related
    name = models.CharField(max_length=100)
    river = models.ForeignKey(River, on_delete=models.CASCADE)
    grade = models.CharField(max_length=100)
    description = MarkdownxField(default='')

    # levels related
    gauge = models.ForeignKey(Gauge, on_delete=models.SET_NULL, null=True)
    minimum = models.FloatField(null=True)

    # Editing
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='author')
    creation_time = models.DateField(null=True)

    recent_editor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='editor')
    last_edit_time = models.DateField(null=True)

    # Linking
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Section, self).save(*args, **kwargs)

    @property
    def description_markdown(self):
        return markdownify(self.description)

# class Points(models.Model):
#     POINT_TYPES = (
#         (0, 'take_out'),
#         (1, 'rapid'),
#         (2, 'put_in'),
#         (3, 'poi'),
#     )
#     name = models.CharField(max_length=100)
#     point_type = models.CharField(max_length=1, choices=POINT_TYPES)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longditude = models.DecimalField(max_digits=9, decimal_places=6)


# class Sectionpoints(models.Model):
#     section = models.ForeignKey(Section)
#     point = models.ForeignKey(Points)


class Interested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gauge = models.ForeignKey(Gauge, on_delete=models.CASCADE)
