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

        self.create_article_url = api_reverse('blog:article:article-create')
        self.get_article_parent_list_url = api_reverse('blog:article:article-get-category-parent-list', args=(self.article.id,))
        self.delete_article_url = api_reverse('blog:article:article-delete', args=(self.article.id,))
        self.get_article_url = api_reverse('blog:article:article-read', args=(self.article.id,))
        self.update_article_url = api_reverse('blog:article:article-partial-update', args=(self.article.id,))

        self.valid_data = {
            'name': 'some name',
            'short_description': 'some description',
            'category': self.category,
            'article': 'some article'
        }

        self.empty_name_data = {
            'name': '',
            'short_description': 'some description',
            'category': self.category,
            'article': 'some article'
        }

        self.change_name_data = {
            'name': 'some other name'
        }

    def test_create_article(self):
        resp = self.client.post(self.create_article_url, data=self.valid_data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.assertEqual(resp.data['name'], self.valid_data['name'])

    def test_create_article_fail(self):
        resp = self.client.post(self.create_article_url, data=self.empty_name_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(resp.data['name'], ['This field may not be blank.'])

    def test_change_article_name(self):
        resp = self.client.post(self.update_article_url, data=self.change_name_data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['name'], self.change_name_data['name'])

    def test_article_list(self):
        resp = self.client.post(self.get_article_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['name'], self.recipe.name)

    def test_delete_article(self):
        resp = self.client.post(self.delete_article_url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)