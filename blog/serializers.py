# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from rest_framework import serializers

from blog.models import Category, Recipe, Article


# Categories serializers
# ---------------------------------------------------------------------------


class CategoryDetailedSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'children')

    def get_children(self, obj):
        return CategoryDetailedSerializer(obj.get_children(), many=True).data


class CategoryDetailedWithoutChildrenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')


class CreateUpdateCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'parent')


class ListParentCategoriesSerializer(serializers.ModelSerializer):
    categories_list = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('categories_list',)

    def get_categories_list(self, obj):
        return CategoryDetailedWithoutChildrenSerializer(obj.get_ancestors(include_self=True), many=True).data


# Recipe serializers
# ---------------------------------------------------------------------------


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'parent')
        extra_fields = {'parent': {'required': True}}


class DetailRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'parent')


class ListParentRecipeSerializer(serializers.ModelSerializer):
    categories_list = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('categories_list',)

    def get_categories_list(self, obj):
        return CategoryDetailedWithoutChildrenSerializer(obj.parent.get_ancestors(include_self=True), many=True).data

# Article serializers
# ---------------------------------------------------------------------------


class CreateUpdateArticleSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Article
        fields = ('name', 'short_description', 'article', 'category')


class DetailArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('name', 'short_description', 'article', 'category')


class ListParentArticleSerializer(serializers.ModelSerializer):
    categories_list = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('categories_list',)

    def get_categories_list(self, obj):
        return CategoryDetailedWithoutChildrenSerializer(obj.category.get_ancestors(include_self=True), many=True).data
