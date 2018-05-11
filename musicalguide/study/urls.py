from django.urls import path

from . import views

app_name = 'Study'

urlpatterns = [
	path('', views.index, name='index'),
	path('pre/', views.pre_questionnaire, name='pre'),
	path('post/', views.post_questionnaire, name='post'),
	path('submitted_pre/', views.submitted_pre, name='submitted_pre'),
	path('instructions_one/<int:identifier>/', views.instructions_one, name='instructions_one'),
	path('instructions_one_ok/', views.instructions_one_ok, name='instructions_one_ok'),
	path('condition_one/', views.condition_one, name='condition_one'),
	path('instructions_two/', views.instructions_two, name='instructions_two'),
	path('instructions_two_ok/', views.instructions_two_ok, name='instructions_two_ok'),
	path('condition_two/', views.condition_two, name='condition_two'),
	path('submitted_post/', views.submitted_post, name='submitted_post'),
	path('thank_you/', views.thank_you, name='thank_you'),
	path('debug/', views.debug, name='debug'),
	path('condition_one/gen/', views.cond_one_response),
	path('condition_one/off/', views.cond_one_off),
	path('condition_two/magenta_gen/', views.cond_two_response),
	path('condition_two/off/', views.cond_two_off),
]