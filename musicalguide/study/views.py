from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import PreQuestionnaireForm, PostQuestionnaireForm, Participant
from django.urls import reverse

def index(request):
	return render(request, 'study/index.html')

def pre_questionnaire(request):
	pre = PreQuestionnaireForm()
	return render(request, 'study/pre.html', {'form':pre})

def post_questionnaire(request):
	participant = Participant.objects.all().get(pk=request.session.get('identifier'))
	print(participant)
	questionnaire = PostQuestionnaireForm(instance=participant)

	context={'form':questionnaire}
	return render(request, 'study/post.html', context)

def instructions_one(request, identifier):
	return render(request, 'study/instructions_one.html')

def submitted_pre(request):
	identifier = None
	if request.method == 'POST':
		form = PreQuestionnaireForm(request.POST)
		print(form.is_valid())
		if form.is_valid():
			data = form.save()
			identifier = data.id
			request.session['identifier'] = identifier
			return HttpResponseRedirect(reverse('study:instructions_one', args=(identifier,)))
	return HttpResponseRedirect(reverse('study:pre'))

def condition_one(request):
	return render(request, 'study/condition_one.html', {'participant_id': request.session.get('identifier')})

def instructions_one_ok(request):
	identifier = request.session.get('identifier')
	return HttpResponseRedirect(reverse('study:condition_one'))

def instructions_two(request):
	return render(request, 'study/instructions_two.html')

def instructions_two_ok(request):
	identifier = request.session.get('identifier')
	return HttpResponseRedirect(reverse('study:condition_two'))

def condition_two(request):
	return render(request, 'study/condition_two.html', {'participant_id': request.session.get('identifier')})

def submitted_post(request):
	if request.method == 'POST':
		form = PostQuestionnaireForm(request.POST)
		print(form.is_valid())
		if form.is_valid():
			data = form.save()
			return HttpResponseRedirect(reverse('study:thank_you'))
	return HttpResponseRedirect(reverse('study:post'))

def thank_you(request):
	return render(request, 'study/thank_you.html')

def debug(request):
	return render(request, 'study/debug.html')