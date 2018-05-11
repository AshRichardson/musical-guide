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


BUNDLE_NAME = 'basic_rnn'

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
    return output

def get_midi_data(userNoteName, start, end):
	# Just generate one for now
	primer = pretty_midi.PrettyMIDI()
	instrument = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program('Cello'))
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

