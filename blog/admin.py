from django.contrib import admin

# Register your models here.
from blog.models import Category, Recipe, Article

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Article)