from django.shortcuts import render
from django.http import HttpResponse
from .models import PreQuestionnaire

def index(request):
	return render(request, 'study/index.html')

def pre_questionnaire(request):
	questionnaire = PreQuestionnaire()
	context={'questionnaire':questionnaire}
	return render(request, 'study/pre.html', context)
	# pre_question_list = Questionnaire.objects.get(pk=1).question_set.all()
	# context = {'question_list':pre_question_list}
	# return render(request, 'study/pre.html', context)