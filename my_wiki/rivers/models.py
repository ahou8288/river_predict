from django.db import models

# Create your models here.
class River(models.Model):
    name = models.CharField(max_length=100)
    level_url = models.URLField()
    river_id = models.IntegerField()
    description = models.CharField(max_length=1000)
    minimum = models.FloatField()
    def __str__(self):
        return self.name