from django.db import models

RATING_SCALE = ((1, 'Very bad.'), (2, 'Bad.'), (3, 'Average.'), (4, 'Good.'),
	(5, 'Great.'))

# Create your models here.
class Questionnaire(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return self.title

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)

	def __str__(self):
		return self.question_text

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	
class TextAnswer(Answer):
	answer = models.CharField(max_length=300)

class ScaleAnswer(Answer):
	answer = models.SmallIntegerField(choices=RATING_SCALE)

class NumberAnswer(Answer):
	answer = models.PositiveSmallIntegerField()