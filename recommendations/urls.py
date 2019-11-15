"""recommendations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from rest import views

schema_view = get_swagger_view(title='Recommendations')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'v1/recommendations', views.RecommendationsView.as_view()),
    url(r'v1/docs$', schema_view),
    url('', schema_view),
]
handler500 = 'rest_framework.exceptions.server_error'
