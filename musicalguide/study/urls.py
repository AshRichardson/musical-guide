from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('pre/', views.pre_questionnaire, name='pre'),
]