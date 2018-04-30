from django.db import models
from django import forms
from django.forms.widgets import RadioSelect
# from django.forms.extras.widgets import SelectDateWidget

RATING_SCALE = ((1, 'Very bad.'), (2, 'Bad.'), (3, 'Average.'), (4, 'Good.'),
	(5, 'Great.'))
SCALE_TYPES = {'rating':RATING_SCALE}
GENDER_CHOICES = (('m', 'Male'), ('f', 'Female'), ('o', 'Other'))
AGE = ((0, 18), (1, 19), (2, 20), (3, 21), (4, 22))
YES_NO = (('y', 'yes'), ('n', 'no'))
EXPERTISE_CHOICES = (('0', 'Beginner'), ('1', 'Intermediate'), ('2', 'Advanced'), ('3', 'Professional'))
HOURS_OPTIONS = ((0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'),
		(11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '20+'))
class PreQuestionnaireForm(forms.Form):
	age = forms.ChoiceField(label="What is your age (in years)?", choices=AGE,
		widget = forms.Select(attrs={'class':'selector'}))
	gender = forms.ChoiceField(label="What is your gender?", choices=GENDER_CHOICES,
		widget=RadioSelect())
	playMusicalInstruments = forms.ChoiceField(label="Do you play any musical instruments? If you answer no to this question, please skip to Question 7.", choices=YES_NO,
		widget=RadioSelect())
	musicalInstrumentsPlayed = forms.CharField(label="Please list all musical instruments that you play, with associated number of years of experience.", widget=forms.Textarea(), required=False, max_length=500)
	musicLiteracyLevel = forms.ChoiceField(label="How would you rank your ability to read music?", choices=EXPERTISE_CHOICES, widget=RadioSelect(), required=False)
	hoursAWeekPracticing = forms.ChoiceField(label="How many hours per week would you say you spend practicing playing musical instruments?", required=False, choices=HOURS_OPTIONS, widget = forms.Select(attrs={'class':'selector'}))
	hoursAWeekListening = forms.ChoiceField(label="How many hours per week would you say you spend listening to music?", choices=HOURS_OPTIONS, widget = forms.Select(attrs={'class':'selector'}))
	preferredGenres = forms.CharField(label="What genre/s of music do you generally like to listen to?", widget=forms.Textarea(), max_length=500)
	hoursPredictedToPlay = forms.CharField(label="If you could play music with a computer, how long do you think this would entertain you for (i.e. how long do you think you would continue playing before getting bored)?", widget=forms.Textarea(), max_length=500)

class PreQuestionnaire(models.Model):
	form = PreQuestionnaireForm