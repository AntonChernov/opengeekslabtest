# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()

router.register(r'category', api.CRUDCategoryApiView, base_name='categories')
router.register(r'recipe', api.CRUDRecipesApiView, base_name='recipes')
router.register(r'article', api.CRUDArticleApiView, base_name='articles')

urlpatterns = []


urlpatterns += router.urls