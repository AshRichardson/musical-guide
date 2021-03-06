from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import PreQuestionnaireForm, PostQuestionnaireForm, Participant, Note, ComputerNote
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import time
from django.contrib import messages

def index(request):
	return render(request, 'study/index.html')

def pre_questionnaire(request):
	pre = PreQuestionnaireForm()
	return render(request, 'study/pre.html', {'form':pre})

def post_questionnaire(request):
	print(request.session.get('identifier'))
	participant = Participant.objects.all().get(pk=request.session.get('identifier'))
	questionnaire = PostQuestionnaireForm(instance=participant)
	context={'form':questionnaire}
	return render(request, 'study/post.html', context)

def instructions_one(request, identifier):
	return render(request, 'study/instructions_one.html')

def submitted_pre(request):
	identifier = None
	if request.method == 'POST':
		form = PreQuestionnaireForm(request.POST)
		if form.is_valid():
			data = form.save()
			identifier = data.id
			request.session['identifier'] = identifier
			return HttpResponseRedirect(reverse('study:instructions_one', args=(identifier,)))
		return render(request, 'study/pre.html', {'form':form})
	return HttpResponseRedirect(reverse('study:pre'))

def submitted_post(request):
	if request.method == 'POST':
		form = PostQuestionnaireForm(request.POST, instance=Participant.objects.all().get(pk=request.session.get('identifier')))
		if form.is_valid():
			data = form.save()
			return HttpResponseRedirect(reverse('study:thank_you'))
		return render(request, 'study/post.html', {'form':form})
	return HttpResponseRedirect(reverse('study:post'))

def condition_one(request):
	return render(request, 'study/condition_one.html', {'participant_id': request.session.get('identifier')})

def instructions_one_ok(request):
	identifier = request.session.get('identifier')
	if identifier % 2 == 1:
		return HttpResponseRedirect(reverse('study:condition_one'))
	else:
		return HttpResponseRedirect(reverse('study:condition_two'))

def instructions_two(request):
	return render(request, 'study/instructions_two.html')

def instructions_two_ok(request):
	identifier = request.session.get('identifier')
	if identifier % 2 == 1:
		return HttpResponseRedirect(reverse('study:condition_two'))
	else:
		return HttpResponseRedirect(reverse('study:condition_one'))

def condition_two(request):
	return render(request, 'study/condition_two.html', {'participant_id': request.session.get('identifier')})

def cond_two_next(request):
	if request.session.get('identifier') % 2 == 1:
		return HttpResponseRedirect(reverse('study:post'))
	else:
		return HttpResponseRedirect(reverse('study:instructions_two'))

def cond_one_next(request):
	if request.session.get('identifier') % 2 == 1:
		return HttpResponseRedirect(reverse('study:instructions_two'))
	else:
		return HttpResponseRedirect(reverse('study:post'))

def thank_you(request):
	return render(request, 'study/thank_you.html')

def debug(request):
	return render(request, 'study/debug.html')

@csrf_protect
def cond_one_response(request):
	participant = Participant.objects.all().get(pk=request.session.get('identifier'))
	newNote = Note(participant=participant, noteName=request.POST.get('note'), startTime=request.POST.get('startTime'), duration=request.POST.get('duration'), interaction='echo')
	participant.save()
	newNote.save()
	# Hard-coded delay of 2 seconds; TODO
	print(request.POST.get('startTime'))
	aiStartTime = int(request.POST.get('startTime')) + 2000
	print('ai', aiStartTime)
	aiNote = ComputerNote(participant=participant, noteName=request.POST.get('note'), startTime=aiStartTime, duration=request.POST.get('duration'), interaction='echo')
	participant.save()
	aiNote.save()
	return JsonResponse({'notes':[request.POST.get('note'), request.POST.get('duration')]})

@csrf_protect
def cond_two_response(request):
	if request.method != 'POST':
		print('NOT POST METHOD')
		return HttpResponseRedirect(reverse('study:condition_two'))
	if request.POST.get('note') is None:
		print('HARD CODING C3')
		return JsonResponse({'notes':[('C3', request.POST.get('startTime'), request.POST.get('duration'))]})
	response = get_midi_data(request.POST.get('note'), 0, request.POST.get('duration'))
	participant = Participant.objects.all().get(pk=request.session.get('identifier'))
	newNote = Note(participant=participant, noteName=request.POST.get('note'), startTime=request.POST.get('startTime'), duration=request.POST.get('duration'), interaction='magenta')
	participant.save()
	try:
		newNote.save()
	except ValueError:
		return JsonResponse({'notes':[]})
	notes = []
	for i, note in enumerate(response):
		if len(note[0]) == 3:
			note = (note[0][0] + 's' + note[0][2], note[1], note[2])
		aiNote = ComputerNote(participant=participant, noteName=note[0], startTime=int(request.POST.get('startTime')) + note[1], duration=note[2]-note[1], interaction='magenta')
		participant.save()
		aiNote.save()
		notes.append((note[0], note[1], note[2] - note[1]))
	return JsonResponse({'notes':notes})

#--------------------------------------------------------------------------#
# The code below is adapted from the following source:                     #
# Title: aiDuet                                                            #
# Author: Google                                                           #
# Date: 04/05/18                                                           #
# Availability: https://github.com/googlecreativelab/aiexperiments-ai-duet #
#--------------------------------------------------------------------------#

import magenta

from magenta.models.melody_rnn import melody_rnn_config_flags
from magenta.models.melody_rnn import melody_rnn_model
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

import os
import time
import tempfile
import pretty_midi
import numpy as np

BUNDLE_NAME = 'basic_rnn'

noteNameToMidi = {'C3':48, 'C#3':49, 'D3':50, 'D#3':51, 'E3':52, 'F3':53,
				 'F#3':54, 'G3':55, 'G#3':56, 'A4':57, 'A#4':58, 'B4':59,
				 'C4':60, 'C#4':61, 'D4':62, 'D#4':63, 'E4':64, 'F4':65,
				 'F#4':66, 'G4':67, 'G#4':68, 'A5':69, 'A#5':70, 'B5':71,
				 'C5':72, 'C#5':73, 'D5':74, 'D#5':75, 'E5':76, 'F5':77,
				 'F#5':78, 'G5':79, 'G#5':80, 'A6':81, 'A#6':82, 'B6':83}
indexToNoteName = ['C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A4', 'A#4', 'B4',
				 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A5', 'A#5', 'B5',
				 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A6', 'A#6', 'B6']
pianoRollToNoteName = {}
for noteName in noteNameToMidi.keys():
	pianoRollToNoteName[pretty_midi.note_name_to_number(noteName)] = noteName

config = magenta.models.melody_rnn.melody_rnn_model.default_configs[BUNDLE_NAME]
bundle_file = magenta.music.read_bundle_file(os.path.abspath(BUNDLE_NAME+'.mag'))
steps_per_quarter = 4

generator = melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(
      model=melody_rnn_model.MelodyRnnModel(config),
      details=config.details,
      steps_per_quarter=steps_per_quarter,
      bundle=bundle_file)

def generate_midi(midi_data, total_seconds=10):
    primer_sequence = magenta.music.midi_io.midi_to_sequence_proto(midi_data)

    # For now, assume 120 quavers per minute
    qpm = 120
    steps = 1
    primer_sequence.tempos[0].qpm = qpm

    generator_options = generator_pb2.GeneratorOptions()
    last_end_time = (max(n.end_time for n in primer_sequence.notes)
                     if primer_sequence.notes else 0)

    starting_time = last_end_time + 1 * 60.0 / qpm / steps_per_quarter
    generator_options.generate_sections.add(start_time=starting_time, end_time=starting_time + total_seconds)
    generated_sequence = generator.generate(primer_sequence, generator_options)

    output = tempfile.NamedTemporaryFile()
    magenta.music.midi_io.sequence_proto_to_midi_file(generated_sequence, output.name)
    output.seek(0)
    return pretty_midi.PrettyMIDI(output)

def get_midi_data(userNoteName, start, end):
	print('Time for', userNoteName, 'got:', time.time())
	if len(userNoteName) == 3:
		userNoteName = userNoteName[0] + '#' + userNoteName[2]
	primer = pretty_midi.PrettyMIDI()
	instrument = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program('Cello'))
	noteNumber = pretty_midi.note_name_to_number(userNoteName)
	try:
		note = pretty_midi.Note(velocity=100, pitch=noteNumber, start=int(start), end=int(start) + int(end))
	except ValueError:
		return []
	instrument.notes.append(note)
	primer.instruments.append(instrument)
	output = generate_midi(primer, total_seconds=2) # Takes about 4-6 seconds
	aiNotes = []
	try:
		note = output.instruments[0].notes[0]
		notePitch, noteStart, noteEnd = pretty_midi.note_number_to_name(note.pitch), note.start, note.end
		if len(notePitch) == 3:
			notePitch = notePitch[0] + 's' + notePitch[2]
		aiNotes.append((notePitch, noteStart, noteEnd))
		print('AI notes are', aiNotes)
		return aiNotes
	except IndexError:
		return []

