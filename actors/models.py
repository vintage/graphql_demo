from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField()

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
