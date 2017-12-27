# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter

router =DefaultRouter()

from django.conf.urls import url, include

urlpatterns = [
    url('cooking-blog/', include('blog.api_urls', namespace='blog')),

]


urlpatterns += router.urls
