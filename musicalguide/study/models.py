from django.db import models
from django import forms

RATING_SCALE = ((1, 'Very bad.'), (2, 'Bad.'), (3, 'Average.'), (4, 'Good.'),
	(5, 'Great.'))
SCALE_TYPES = {'rating':RATING_SCALE}

# Create your models here.
class Questionnaire(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return self.title

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
	questionType = models.CharField(max_length=200) # This is either text, scale, or integer

	if questionType == 'text':
		answer = forms.TextInput()
	elif questionType == 'scale':
		# At the moment, hardcoding a RATING_SCALE
		# scale = model.CharField
		answer = forms.ChoiceField(RATING_SCALE)
	elif questionType == 'integer':
		answer = forms.IntegerField()
	elif questionType == 'gender':
		answer = forms.ChoiceField(choices=((1, 'Female'), (2, 'Male'), (3, 'Other')))

	def __str__(self):
		return self.question_text
