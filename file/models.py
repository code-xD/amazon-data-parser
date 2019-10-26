from django.db import models

# Create your models here.


class Dataset(models.Model):
    name = models.CharField(max_length=200)
    scraped_file = models.FileField(upload_to='scraped', blank=True, null=True)
    ml_file = models.FileField(upload_to='machinelearned', blank=True, null=True)
    volume = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
