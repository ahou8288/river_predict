from django.db import models
from django.template.defaultfilters import slugify

class River(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.name


# class Levels(models.Model):
#     READING_TYPES = (
#         (0, 'level'),
#         (1, 'discharge'),
#     )
#     river = models.ForeignKey(River)
#     reading = models.FloatField()
#     time = models.DateTimeField()
#     unit = models.CharField(max_length=1, choices=READING_TYPES)


class Section(models.Model):
    name = models.CharField(max_length=100)
    river = models.ForeignKey(River, on_delete=models.CASCADE)
    minimum = models.FloatField()
    def __str__(self):
        return self.name
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Section, self).save(*args, **kwargs)


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


# class Interested(models.Model):
#     user = models.ForeignKey(User)
#     river = models.ForeignKey(River)