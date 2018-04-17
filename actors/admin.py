from django.contrib import admin

from actors import models


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
    pass
