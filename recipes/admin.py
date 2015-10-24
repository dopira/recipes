from django.contrib import admin

from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Recipe, RecipeAdmin)
