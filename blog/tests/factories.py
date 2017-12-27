# -*- coding: utf-8 -*-

import datetime

import factory
import time
from django.utils import lorem_ipsum

from blog.models import Category, Recipe, Article


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    # parent = factory.SubFactory('blog.tests/factories.CategoryFactory')

    @factory.lazy_attribute_sequence
    def name(self, n):

        return '{0}_{1}_{2}'.format(lorem_ipsum.words(1, False), n,
                                    time.mktime(datetime.datetime.now().timetuple()))


class RecipeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Recipe

    parent = factory.SubFactory('blog.tests/factories.CategoryFactory')

    @factory.lazy_attribute_sequence
    def name(self, n):

        return '{0}_{1}_{2}'.format(lorem_ipsum.words(1, False), n,
                                    time.mktime(datetime.datetime.now().timetuple()))

    @factory.lazy_attribute_sequence
    def description(self, n):
        return '{0}_{1}_{2}'.format(lorem_ipsum.paragraphs(2, False), n,
                                    time.mktime(datetime.datetime.now().timetuple()))


class ArticleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Article

    category = factory.SubFactory('blog.tests/factories.CategoryFactory')

    @factory.lazy_attribute_sequence
    def name(self, n):

        return '{0}_{1}_{2}'.format(lorem_ipsum.words(1, False), n,
                                    time.mktime(datetime.datetime.now().timetuple()))

    @factory.lazy_attribute_sequence
    def short_description(self, n):
        return '{0}_{1}_{2}'.format(lorem_ipsum.words(1, False), n,
                                    time.mktime(datetime.datetime.now().timetuple()))

    @factory.lazy_attribute_sequence
    def article(self, n):
        return '{0}_{1}_{2}'.format(lorem_ipsum.paragraphs(2, False), n,
                                    time.mktime(datetime.datetime.now().timetuple()))