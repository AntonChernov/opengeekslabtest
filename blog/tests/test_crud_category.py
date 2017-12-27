# -*- coding: utf-8 -*-

from django.apps import apps
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

from blog.tests.factories import CategoryFactory, RecipeFactory, ArticleFactory
from blog.models import Article, Recipe


class CategoryApiTestCase(APITestCase):

    def setUp(self):
        self.category = CategoryFactory()

        self.recipe = RecipeFactory()
        self.recipe.parent = self.category
        self.recipe.save()

        self.article = ArticleFactory()
        self.article.category = self.category
        self.article.save()

        self.create_category_url = api_reverse('blog:categories:category-list')
        self.get_article_list_url = api_reverse('blog:categories:category-get-article-list', args=(self.category.id,))
        self.get_category_parent_list_url = api_reverse('blog:categories:category-get-category-parent-list', args=(self.category.id,))
        self.get_recipe_list_url = api_reverse('blog:categories:category-get-recipe-list', args=(self.category.id,))
        self.delete_category_url = api_reverse('blog:categories:category-delete', args=(self.category.id,))
        self.get_category_url = api_reverse('blog:categories:category-read', args=(self.category.id,))
        self.update_category_url = api_reverse('blog:categories:category-partial-update', args=(self.category.id,))

        self.valid_data = {
            'name': 'some name',
            'parent': self.category
        }

        self.empty_name_data = {
            'name': '',
            'parent': self.category
        }

        self.change_name_data = {
            'name': 'some other name'
        }

    def test_create_category(self):
        resp = self.client.post(self.create_category_url, data=self.valid_data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.assertEqual(resp.data['name'], self.valid_data['name'])

    def test_create_category_fail(self):
        resp = self.client.post(self.create_category_url, data=self.empty_name_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(resp.data['name'], ['This field may not be blank.'])

    def test_change_category_name(self):
        resp = self.client.post(self.update_category_url, data=self.change_name_data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['name'], self.change_name_data['name'])

    def test_article_list(self):
        resp = self.client.post(self.get_article_list_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(len(resp.data['results']), Article.objects.filter(category=self.category).count())

    def test_recipe_list(self):
        resp = self.client.post(self.get_recipe_list_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(len(resp.data['results']), Recipe.objects.filter(parent=self.category).count())

    def test_categories_list(self):
        resp = self.client.post(self.get_category_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['name'], self.category.name)

    def test_delete_category(self):
        resp = self.client.post(self.delete_category_url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)