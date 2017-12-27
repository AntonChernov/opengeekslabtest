# -*- coding: utf-8 -*-

from django.apps import apps
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

from blog.tests.factories import CategoryFactory, RecipeFactory, ArticleFactory


class RecipeApiTestCase(APITestCase):

    def setUp(self):
        self.category = CategoryFactory()

        self.recipe = RecipeFactory()
        self.recipe.parent = self.category
        self.recipe.save()

        self.article = ArticleFactory()
        self.article.category = self.category
        self.article.save()

        self.create_recipe_url = api_reverse('blog:recipes:recipes-create')
        self.get_recipe_parent_list_url = api_reverse('blog:recipes:recipes-get-category-parent-list', args=(self.recipe.id,))
        self.delete_recipe_url = api_reverse('blog:recipes:recipes-delete', args=(self.recipe.id,))
        self.get_recipe_url = api_reverse('blog:recipes:recipes-read', args=(self.recipe.id,))
        self.update_recipe_url = api_reverse('blog:recipes:recipes-partial-update', args=(self.recipe.id,))

        self.valid_data = {
            'name': 'some name',
            'description': 'some description',
            'parent': self.category
        }

        self.empty_name_data = {
            'name': '',
            'description': 'some description',
            'parent': self.category
        }

        self.change_name_data = {
            'name': 'some other name'
        }

    def test_create_recipe(self):
        resp = self.client.post(self.create_recipe_url, data=self.valid_data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.assertEqual(resp.data['name'], self.valid_data['name'])

    def test_create_recipe_fail(self):
        resp = self.client.post(self.create_recipe_url, data=self.empty_name_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(resp.data['name'], ['This field may not be blank.'])

    def test_change_recipe_name(self):
        resp = self.client.post(self.update_recipe_url, data=self.change_name_data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['name'], self.change_name_data['name'])

    def test_recipe_list(self):
        resp = self.client.post(self.get_recipe_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['name'], self.recipe.name)

    def test_delete_category(self):
        resp = self.client.post(self.delete_recipe_url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
