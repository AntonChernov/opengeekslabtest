# -*- coding: utf-8 -*-

from django.db import models

from django.utils.translation import ugettext as _

from mptt.models import TreeForeignKey, MPTTModel


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True, help_text=_('Category name.'), verbose_name=_('Category name'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recipe_category'
        verbose_name = 'Recipe categories'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    parent = models.ForeignKey(Category, related_name='recipe')
    name = models.CharField(max_length=255, help_text=_('Recipe name.'), verbose_name=_('Recipe name'))
    description = models.TextField()

    class Meta:
        db_table = 'recipe'
        verbose_name = 'Recipes'

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(Category, related_name='article')
    name = models.CharField(max_length=150, help_text=_('Article name.'), verbose_name=_('Article name'))
    short_description = models.CharField(max_length=255, help_text=_('Short description of article'),
                                         verbose_name=_('Short description of article'))
    article = models.TextField(help_text=_('Article text.'), verbose_name=_('Article text'))

    class Meta:
        db_table = 'article'
        verbose_name = 'Articles'






