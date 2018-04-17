from django.db import models

from actors import models as actor_models


class MovieCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Movie category'
        verbose_name_plural = 'Movie categories'

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    min_age = models.IntegerField()
    poster = models.ImageField()
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, editable=False,
    )
    categories = models.ManyToManyField(MovieCategory, related_name='movies')

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title

    def get_calculated_rating(self):
        return self.ratings.aggregate(
            avg_rate=models.Avg('value'),
        )['avg_rate'] or 0


class CastMember(models.Model):
    movie = models.ForeignKey(
        Movie, related_name='cast', on_delete=models.CASCADE,
    )
    actor = models.ForeignKey(
        actor_models.Actor, related_name='movies', on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Cast member'
        verbose_name_plural = 'Cast members'

    def __str__(self):
        return self.name


class MovieRating(models.Model):
    movie = models.ForeignKey(
        Movie, related_name='ratings', on_delete=models.CASCADE,
    )
    value = models.IntegerField()

    class Meta:
        verbose_name = 'Movie rating'
        verbose_name_plural = 'Movie ratings'

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        is_adding = not self.pk

        instance = super().save(*args, **kwargs)
        if is_adding:
            self.movie.rating = self.movie.get_calculated_rating()
            self.movie.save()

        return instance
