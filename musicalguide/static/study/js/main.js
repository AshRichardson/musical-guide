
// var whiteKeys = [
// 	'C3', 'D3', 'E3', 'F3', 'G3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4',
// 	'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'A6', 'B6'
// ];

// var blackKeys = [
// 	'Cs3', 'Ds3', 'Fs3', 'Gs3', 'As4', 'Cs4', 'Ds4', 'Fs4', 'Gs4', 'As5',
// 	'Cs5', 'Ds5', 'Fs5', 'Gs5', 'As6'
// ];

var whiteKeys = [
	'C3'
];

var blackKeys = [
	'Cs3'
];

var audioPath = '../../static/study/audio/';

var c3Audio = new Audio(audioPath + 'C3.mp3');

var whiteNoteAudios = [c3Audio];


// var cs3Audio = new Audio(audioPath + 'Cs3.mp3');
var cs3Audio = new Audio(audioPath + 'Cs3.mp3');
var blackNoteAudios = [cs3Audio];

var main = function() {
	$('.piano-white').mousedown(function() {
		for (i = 0; i < whiteKeys.length; i++) {
			if ($(this).hasClass(whiteKeys[i])) {
				whiteNoteAudios[i].play();
			}
		}
	})
	$('.piano-white').mouseup(function() {
		for (i = 0; i < whiteKeys.length; i++) {
			if ($(this).hasClass(whiteKeys[i])) {
				whiteNoteAudios[i].pause();
				whiteNoteAudios[i].currentTime = 0;
			}
		}
	})

	$('.piano-black').mousedown(function() {
		for (i=0; i < blackKeys.length; i++) {
			if ($(this).hasClass(blackKeys[i])) {
				blackNoteAudios[i].play();
			}
		}
	})

	$('.piano-black').mouseup(function() {
		for (i=0; i < blackKeys.length; i++) {
			if ($(this).hasClass(blackKeys[i])) {
				blackNoteAudios[i].pause();
				blackNoteAudios[i].currentTime = 0;
			}
		}
	})


};



$(document).ready(main);