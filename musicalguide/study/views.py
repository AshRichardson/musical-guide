from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import PreQuestionnaireForm, PostQuestionnaireForm, Participant
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
#from resources.magenta_predict import *
import time

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
		form = PostQuestionnaireForm(request.POST, instance=Participant.objects.all().get(pk=request.session.get('identifier')))
		print(form.is_valid())
		if form.is_valid():
			data = form.save()
			return HttpResponseRedirect(reverse('study:thank_you'))
	return HttpResponseRedirect(reverse('study:post'))

def thank_you(request):
	return render(request, 'study/thank_you.html')

def debug(request):
	return render(request, 'study/debug.html')

@csrf_protect
def cond_one_response(request):
	return JsonResponse({'notes':request.POST.get('note')})

# @csrf_protect
# def cond_one_off(request):
# 	time.sleep(3)
# 	return JsonResponse({'off_note':request.POST.get('note')})

@csrf_protect
def cond_two_response(request):
	# time.sleep(2)
	response = get_midi_data(request.POST.get('note'), request.POST.get('startTime'), request.POST.get('endTime'))
	notes = []
	for i, note in enumerate(response):
		if len(note[0]) == 3:
			note = (note[0][0] + 's' + note[0][2], note[1], note[2])
		notes.append((note[0], note[1], note[2] - note[1]))
		#notes.append((note[0], note[2] - note[1]))
	return JsonResponse({'notes':notes})
	# return JsonResponse({'next_note':request.POST.get('note')})

# @csrf_protect
# def cond_two_off(request):
# 	response = get_midi_data(request.POST.get('note'), request.POST.get('startTime'), request.POST.get('endTime'))
# 	time.sleep(2)
# 	return JsonResponse({'off_note':request.POST.get('note')}) # TODO

#----------- REFACTOR BELOW PART INTO MAGENTA_PREDICT.PY EVENTUALLY; TODO -----------#

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

def _steps_to_seconds(steps, qpm):
    return steps * 60.0 / qpm / steps_per_quarter

def generate_midi(midi_data, total_seconds=10):
    primer_sequence = magenta.music.midi_io.midi_to_sequence_proto(midi_data)

    # predict the tempo
    if len(primer_sequence.notes) > 4:
        estimated_tempo = midi_data.estimate_tempo()
        if estimated_tempo > 240:
            qpm = estimated_tempo / 2
        else:
            qpm = estimated_tempo
    else:
        qpm = 120
    primer_sequence.tempos[0].qpm = qpm

    generator_options = generator_pb2.GeneratorOptions()
    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in primer_sequence.notes)
                     if primer_sequence.notes else 0)
    generator_options.generate_sections.add(
        start_time=last_end_time + _steps_to_seconds(1, qpm),
        end_time=total_seconds)

    # generate the output sequence
    generated_sequence = generator.generate(primer_sequence, generator_options)

    output = tempfile.NamedTemporaryFile()
    magenta.music.midi_io.sequence_proto_to_midi_file(generated_sequence, output.name)
    output.seek(0)
    return pretty_midi.PrettyMIDI(output)

def get_midi_data(userNoteName, start, end):
	# Just generate one for now
	if len(userNoteName) == 3:
		userNoteName = userNoteName[0] + '#' + userNoteName[2]
	primer = pretty_midi.PrettyMIDI()
	instrument = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program('Cello'))
	for _ in range(3):
		noteNumber = pretty_midi.note_name_to_number(userNoteName)
		note = pretty_midi.Note(velocity=100, pitch=noteNumber, start=start, end=end)
		instrument.notes.append(note)
	output = generate_midi(primer, total_seconds=2)
	pianoRoll = output.get_piano_roll()
	
	subArrays = np.split(pianoRoll, [48, 81])
	first = subArrays[1]
	second = np.split(subArrays[2], [12, 15])[1]
	ofInterest = np.concatenate((first, second))
	listOfInterest = ofInterest.tolist()
	# for subList in listOfInterest:
	numZeros = 0
	others = 0
	aiNotes = []
	for noteIndex, timeList in enumerate(pianoRoll.tolist()):
		startTime = None
		endTime = None
		lastVal = 0
		for timeIndex, value in enumerate(timeList):
			timeIndex = timeIndex * 10
			if value != 0:
				# This note is on at timeIndex
				if lastVal == 0:
					# First timeIndex for this note
					startTime = timeIndex
			elif lastVal != 0:
				# Note was on and is now off. Add to list of notes
				endTime = timeIndex
				noteName = pianoRollToNoteName.get(noteIndex)
				if noteName is None:
					pass
					#print('Ignoring note at midi value', noteIndex)
				else:
					aiNotes.append((noteName, startTime, endTime))
					#print('added note', noteName, 'with start and end', startTime, endTime)
					startTime = None
					endTime = None

			# if item != 0 and item != 0.0:
			# 	print('in sublist', noteIndex, 'at index', index, 'means note is', pianoRollToNoteName.get(noteIndex))
			lastVal = value
	if lastVal != 0:
		endTime = timeIndex
		noteName = pianoRollToNoteName.get(noteIndex)
		if noteName is None:
			pass
			#print('Ignoring note at midi value', noteIndex)
		else:
			aiNotes.append((noteName, startTime, endTime))
			#print('added note', noteName, 'with start and end', startTime, endTime)
			startTime = None
			endTime = None				
	return sorted(aiNotes, key=lambda x:x[1])


