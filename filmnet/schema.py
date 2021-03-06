from graphene_django import DjangoObjectType
import graphene
from django.conf import settings

from actors import models as actor_models
from movies import models as movie_models


class Actor(DjangoObjectType):
    class Meta:
        model = actor_models.Actor


class MovieCategory(DjangoObjectType):
    class Meta:
        model = movie_models.MovieCategory
        only_fields = ('id', 'name')


class CastMember(DjangoObjectType):
    class Meta:
        model = movie_models.CastMember


class Movie(DjangoObjectType):
    categories = graphene.List(MovieCategory)
    cast = graphene.List(CastMember)
    poster = graphene.String(
        width=graphene.Int(),
        height=graphene.Int(),
    )

    class Meta:
        model = movie_models.Movie

    def resolve_cast(self, info):
        return self.cast.all()

    def resolve_categories(self, info):
        return self.categories.all()

    def resolve_poster(self, info, width=None, height=None):
        if self.poster and self.poster.file:
            image_url = '{}/{}{}'.format(
                settings.BASE_DOMAIN,
                settings.MEDIA_URL,
                self.poster,
            )

            if width and height:
                image_parts = image_url.split('.')

                image_url = '{}_{}x{}.{}'.format(
                    '.'.join(image_parts[:-1]),
                    width,
                    height,
                    image_parts[-1],
                )

            return image_url

        return None


class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    movie = graphene.Field(Movie, movie_id=graphene.Int())

    def resolve_movies(self, info):
        return movie_models.Movie.objects.all()

    def resolve_movie(self, info, movie_id):
        return movie_models.Movie.objects.get(pk=movie_id)


class RateMovie(graphene.Mutation):
    class Arguments:
        movie_id = graphene.Int()
        rate = graphene.Int()

    new_rate = graphene.Float()
    movie = graphene.Field(Movie)

    def mutate(self, info, movie_id, rate):
        movie = movie_models.Movie.objects.get(pk=movie_id)

        rating = movie_models.MovieRating.objects.create(
            movie=movie, value=rate,
        )

        new_rate = format(rating.movie.rating, '.1f')

        return RateMovie(new_rate=new_rate, movie=movie)


class Mutation(graphene.ObjectType):
    rate_movie = RateMovie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
