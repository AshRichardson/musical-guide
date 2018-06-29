from django.db import models
from django import forms
from django.forms.widgets import RadioSelect
import json
# from django.forms.extras.widgets import SelectDateWidget

# Choice options
RATING_CHOICES = [('1', '1 (not enjoyable at all)'), ('2', '2'), ('3', '3'), ('4', '4'),
	('5', '5 (very enjoyable)')]
GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
AGE = [(0, 18), (1, 19), (2, 20), (3, 21), (4, 22)] # Needs more ages; TODO
YES_NO = [('y', 'Yes'), ('n', 'No')]
EXPERTISE_CHOICES = [(None, 'Not applicable'), ('0', 'Beginner'), ('1', 'Intermediate'),
	('2', 'Advanced'), ('3', 'Professional')]
HOURS_OPTIONS = [(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
	(6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
	(13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'),
	(19, '19'), (20, '20'), (21, '21+')]
SYSTEMS_CHOICES = [('0', 'First system'), ('1', 'Second system')]
COMPARISON_CHOICES = [('1', '1 (much worse)'), ('2', '2 (a bit worse)'), ('3', '3 (about the same'), ('4', '4 (a bit better)'), ('5', '5 (much better)')]
NUMBER_CHOICES = [('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four')]
OPTION_CHOICES = [('1', '1 (option 1)'), ('2', '2 (option 2)'), ('3', '3 (option 3)'), ('4', '4 (option 4)'), ('5', '5 (option 5)')]

# Pre-survey questionnaire questions
AGE_QUESTION = 'What is your age (in years)?'
GENDER_QUESTION = 'What is your gender?'
PLAYS_QUESTION = 'Do you play any musical instruments? If you answer no to' + \
	' this question, please skip to Question 7.'
LIST_INSTRUMENTS_QUESTION = 'Please list all musical instruments that you ' + \
	'play, with associated number of years of experience.'
ABILITY_QUESTION = 'How would you rank your ability to read music?'
HOURS_PRACTICED = 'How many hours per week would you say you spend ' + \
	'practicing playing musical instruments?'
HOURS_LISTENED = 'How many hours per week would you say you spend ' + \
	'listening to music?'
SELECT_THREE = 'Please select the option with the English word for the number 3 below.'
GENRES_QUESTION = 'What genre/s of music do you generally like to listen to?'
PREDICTED_PLAYING_TIME = 'If you could play music with a computer, how long do ' + \
	'you think this would entertain you for (i.e. how long do you think ' + \
	'you would continue playing before getting bored)? Please specify units.'

# Questions for the post-study questionnaire
ESTIMATED_TIME = 'How long do you think you spent playing music with this system?'
SYSTEM_RATING = "How enjoyable would you rate your experience playing music with this system to be?"
PLAY_AGAIN = "If given the chance, would you play music with this system again?"
SYSTEM_IMPRESSION = "What did you think about this system’s responses to your music?"
SYSTEM_GOOD = "What (if anything) did you like about playing music with this system?"
SYSTEM_BAD = "What (if anything) did you not like about playing music with this system?"
SYSTEM_SUGGESTIONS = "What sorts of things would you like to see an interactive music AI doing, that you did not in this system?"
SYSTEM_PREFERRED = "Which system did you prefer playing with (the first or the second)?"
WHY_SYSTEM_PREFERRED = "Why did you prefer playing with this system?"
COMPARED_TO_SELF = "How would you rate playing music with this system, compared to playing music by yourself? If you do not play music by yourself, please leave this question blank."
COMPARED_TO_FRIENDS = "How would you rate playing music with this system, compared to playing music with a friend or family member? If you do not play music with a friend or family member, please leave this question blank."
FILTER_Q_1 = "Please write the word 'music' in the space below."
FILTER_Q_2 = "Please select option 4 for this question."

class Participant(models.Model):
	# Use auto-incremented id as participant id
	# participant_id = models.AutoField(primary_key=True)

	# Data collected from pre-study questionnaire
	age = models.IntegerField(default=0)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='o')
	plays_instruments=models.CharField(choices=YES_NO, max_length=3, default='')
	instrument_list=models.CharField(max_length=500, default='', blank=True)
	ability = models.CharField(choices=EXPERTISE_CHOICES, max_length=1, null=True, blank=True)
	hours_practiced_per_week = models.IntegerField(null=True, blank=True)
	hours_listening_per_week = models.IntegerField(default=0)
	select_three = models.CharField(max_length=6, choices=NUMBER_CHOICES, default='o')
	preferred_genres = models.CharField(max_length=500, default='')
	predicted_playing_time = models.CharField(max_length=100, default='')

	# Data collected from post-study questionnaire
	first_system_estimated_time = models.CharField(max_length=100, default='')
	first_system_rating = models.CharField(max_length=2, choices=RATING_CHOICES, default='')
	first_system_play_again = models.CharField(max_length=3, choices=YES_NO, default='')
	first_system_impression = models.CharField(max_length=500, default='')
	first_system_good = models.CharField(max_length=500, default='')
	first_system_bad = models.CharField(max_length=500, default='')
	filter_q_1 = models.CharField(max_length=20, default='')
	first_system_suggestions = models.CharField(max_length=500, default='')
	first_compared_to_self = models.CharField(max_length=2, choices=COMPARISON_CHOICES, default='')
	first_compared_to_friends = models.CharField(max_length=2, choices=COMPARISON_CHOICES, default='')

	second_system_estimated_time = models.CharField(max_length=100, default='')
	second_system_rating = models.CharField(max_length=2, choices=RATING_CHOICES, default='')
	second_system_play_again = models.CharField(max_length=3, choices=YES_NO, default='')
	second_system_impression = models.CharField(max_length=500, default='')
	second_system_good = models.CharField(max_length=500, default='')
	second_system_bad = models.CharField(max_length=500, default='')
	second_system_suggestions = models.CharField(max_length=500, default='')
	second_compared_to_self = models.CharField(max_length=2, choices=COMPARISON_CHOICES, default='')
	filter_q_2 = models.CharField(max_length=20, choices=OPTION_CHOICES, default='o')
	second_compared_to_friends = models.CharField(max_length=2, choices=COMPARISON_CHOICES, default='')

	system_preferred = models.CharField(max_length=2, default='', choices=SYSTEMS_CHOICES)
	why_system_preferred = models.CharField(max_length=500, default='')

class PreQuestionnaireForm(forms.ModelForm):
	class Meta:
		model = Participant
		fields = ['age', 'gender', 'plays_instruments', 'instrument_list', 
			'ability', 'hours_practiced_per_week', 'hours_listening_per_week',
			'select_three', 'preferred_genres', 'predicted_playing_time']
		labels = {'age':AGE_QUESTION, 'gender':GENDER_QUESTION,
			'plays_instruments':PLAYS_QUESTION,
			'instrument_list':LIST_INSTRUMENTS_QUESTION,
			'ability':ABILITY_QUESTION,
			'hours_practiced_per_week':HOURS_PRACTICED,
			'hours_listening_per_week':HOURS_LISTENED,
			'select_three':SELECT_THREE,
			'preferred_genres':GENRES_QUESTION,
			'predicted_playing_time':PREDICTED_PLAYING_TIME}
		widgets = {'plays_instruments': forms.RadioSelect,
			'instrument_list': forms.Textarea(attrs={'width':"100%"}),
			'ability': forms.RadioSelect,
			'select_three': forms.RadioSelect,
			'preferred_genres': forms.Textarea(attrs={'width':"100%"}),
			'predicted_playing_time': forms.Textarea(attrs={'width':"100%"})}

class PostQuestionnaireForm(forms.ModelForm):
	class Meta:
		model = Participant
		fields = ['first_system_estimated_time', 
			'first_system_rating',
			'first_system_play_again',
			'first_system_impression',
			'first_system_good', 'first_system_bad',
			'filter_q_1', 'first_system_suggestions',
			'first_compared_to_self',
			'first_compared_to_friends',
			'second_system_estimated_time', 
			'second_system_rating',
			'second_system_play_again',
			'second_system_impression',
			'second_system_good', 'second_system_bad',
			'second_system_suggestions',
			'second_compared_to_self',
			'filter_q_2',
			'second_compared_to_friends',
			'system_preferred',
			'why_system_preferred',
		]
		labels = {'first_system_estimated_time':ESTIMATED_TIME,
			'first_system_rating':SYSTEM_RATING,
			'first_system_play_again':PLAY_AGAIN,
			'first_system_impression':SYSTEM_IMPRESSION,
			'first_system_good':SYSTEM_GOOD,
			'first_system_bad':SYSTEM_BAD,
			'filter_q_1':FILTER_Q_1,
			'first_system_suggestions':SYSTEM_SUGGESTIONS,
			'first_compared_to_self':COMPARED_TO_SELF,
			'first_compared_to_friends':COMPARED_TO_FRIENDS,
			'second_system_estimated_time':ESTIMATED_TIME,
			'second_system_rating':SYSTEM_RATING,
			'second_system_play_again':PLAY_AGAIN,
			'second_system_impression':SYSTEM_IMPRESSION,
			'second_system_good':SYSTEM_GOOD,
			'second_system_bad':SYSTEM_BAD,
			'second_compared_to_self':COMPARED_TO_SELF,
			'filter_q_2':FILTER_Q_2,
			'second_compared_to_friends':COMPARED_TO_FRIENDS,
			'second_system_suggestions':SYSTEM_SUGGESTIONS,
			'system_preferred':SYSTEM_PREFERRED,
			'why_system_preferred':WHY_SYSTEM_PREFERRED,
		}
		widgets = {'first_system_estimated_time': forms.Textarea(attrs={'width':"100%"}),
			'first_system_rating': RadioSelect,
			'first_system_play_again': RadioSelect,
			'first_system_impression': forms.Textarea(attrs={'width':"100%"}),
			'first_system_good':forms.Textarea(attrs={'width':"100%"}),
			'first_system_bad':forms.Textarea(attrs={'width':"100%"}),
			'filter_q_1':forms.Textarea(attrs={'width':'100%'}),
			'first_system_suggestions':forms.Textarea(attrs={'width':"100%"}),
			'first_compared_to_self': RadioSelect,
			'first_compared_to_friends': RadioSelect,
			'second_system_estimated_time': forms.Textarea(attrs={'width':"100%"}),
			'second_system_rating': RadioSelect,
			'second_system_play_again': RadioSelect,
			'second_system_impression': forms.Textarea(attrs={'width':"100%"}),
			'second_system_good':forms.Textarea(attrs={'width':"100%"}),
			'second_system_bad':forms.Textarea(attrs={'width':"100%"}),
			'second_system_suggestions':forms.Textarea(attrs={'width':"100%"}),
			'second_compared_to_self': RadioSelect,
			'filter_q_2': RadioSelect,
			'second_compared_to_friends': RadioSelect,
			'system_preferred': RadioSelect,
			'why_system_preferred': forms.Textarea(attrs={'width':'100%'})
		}


class Note(models.Model):
	participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=1)
	noteName = models.CharField(max_length=3, default='000')
	startTime = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	interaction = models.CharField(max_length=10, default='echo')

class ComputerNote(models.Model):
	participant = models.ForeignKey(Participant, on_delete=models.CASCADE, default=1)
	noteName = models.CharField(max_length=3, default='000')
	startTime = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	interaction = models.CharField(max_length=10, default='echo')
