# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from blog import models
from blog import serializers
from blog.serializers import CategoryDetailedSerializer, CategoryDetailedWithoutChildrenSerializer, \
    CreateUpdateRecipeSerializer, DetailRecipeSerializer, CreateUpdateArticleSerializer, \
    DetailArticleSerializer, ListParentCategoriesSerializer, ListParentArticleSerializer, ListParentRecipeSerializer


class CRUDCategoryApiView(ModelViewSet):
    """
    CRUD a Category objects
    """
    queryset = models.Category.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers.CreateUpdateCategorySerializer
        elif self.action in ['list', 'retrieve']:
            return serializers.CategoryDetailedSerializer
        elif self.action == 'get_category_parent_list':
            return ListParentCategoriesSerializer
        else:
            return serializers.CategoryDetailedSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(CategoryDetailedWithoutChildrenSerializer(serializer.instance).data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(CategoryDetailedSerializer(serializer.instance).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Object {0}: {1} has been deleted successfully.'.format(
            instance.name, instance.id)}, status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['GET'], url_path='parent-list/(?P<pk>[0-9]+)')
    def get_category_parent_list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['GET'], url_path='recipe-list/(?P<category_pk>[0-9]+)')
    def get_recipe_list(self, request, *args, **kwargs):
            queryset = self.filter_queryset(models.Recipe.objects.filter(parent=kwargs.get('category_pk')))

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = DetailRecipeSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = DetailRecipeSerializer(queryset, many=True)
            return Response(serializer.data)

    @list_route(methods=['GET'], url_path='article-list/(?P<category_pk>[0-9]+)')
    def get_article_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(models.Article.objects.filter(category=kwargs.get('category_pk')))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DetailArticleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = DetailArticleSerializer(queryset, many=True)
        return Response(serializer.data)


class CRUDRecipesApiView(ModelViewSet):
    """
    CRUD Recipe objects
    """
    queryset = models.Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateUpdateRecipeSerializer
        elif self.action == ['list', 'retrieve']:
            return DetailRecipeSerializer
        elif self.action == 'get_category_parent_list':
            return ListParentRecipeSerializer
        else:
            return DetailRecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(DetailRecipeSerializer(serializer.instance).data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(DetailRecipeSerializer(serializer.instance). data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(DetailRecipeSerializer(serializer.instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Recipe {0}: {1} has been deleted successfully.'.format(
            instance.name, instance.id)}, status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['GET'], url_path='parent-list/(?P<pk>[0-9]+)')
    def get_category_parent_list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CRUDArticleApiView(ModelViewSet):
    """
    CRUD Article objects
    """
    queryset = models.Article.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateUpdateArticleSerializer
        elif self.action == ['list', 'retrieve']:
            return DetailArticleSerializer
        elif self.action == 'get_category_parent_list':
            return ListParentArticleSerializer
        else:
            return DetailArticleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(DetailArticleSerializer(serializer.instance).data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(DetailArticleSerializer(serializer.instance). data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(DetailArticleSerializer(serializer.instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Article {0}: {1} has been deleted successfully.'.format(
            instance.name, instance.id)}, status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['GET'], url_path='parent-list/(?P<pk>[0-9]+)')
    def get_category_parent_list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
