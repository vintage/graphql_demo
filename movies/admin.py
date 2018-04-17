from django.contrib import admin

from movies import models


@admin.register(models.MovieCategory)
class MovieCategoryAdmin(admin.ModelAdmin):
    pass


class CastMemberInline(admin.StackedInline):
    model = models.CastMember


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [CastMemberInline]
    readonly_fields = ('rating',)
