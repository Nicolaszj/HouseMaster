from django.urls import path
from . import views
from .i18n_views import i18n_test

urlpatterns = [
    path('', views.home, name='home'),
    path('i18n-test/', i18n_test, name='i18n_test'),
]