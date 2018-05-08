
// var whiteKeys = [
// 	'C3', 'D3', 'E3', 'F3', 'G3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4',
// 	'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'A6', 'B6'
// ];

// var blackKeys = [
// 	'Cs3', 'Ds3', 'Fs3', 'Gs3', 'As4', 'Cs4', 'Ds4', 'Fs4', 'Gs4', 'As5',
// 	'Cs5', 'Ds5', 'Fs5', 'Gs5', 'As6'
// ];

var whiteKeys = [
	'C3', 'D3', 'E3', 'F3', 'G3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'A6', 'B6'
];

var blackKeys = [
	'Cs3', 'Ds3', 'Fs3', 'Gs3', 'As4', 'Cs4', 'Ds4', 'Fs4', 'Gs4', 'As5', 'Cs5', 'Ds5', 'Fs5', 'Gs5', 'As6'
];

var audioPath = '../../static/study/audio/';

var c3Audio = new Audio(audioPath + 'C3.mp3');
var d3Audio = new Audio(audioPath + 'D3.mp3');
var e3Audio = new Audio(audioPath + 'E3.mp3');
var f3Audio = new Audio(audioPath + 'F3.mp3');
var g3Audio = new Audio(audioPath + 'G3.mp3');
var a4Audio = new Audio(audioPath + 'A4.mp3');
var b4Audio = new Audio(audioPath + 'B4.mp3');
var c4Audio = new Audio(audioPath + 'C4.mp3');
var d4Audio = new Audio(audioPath + 'D4.mp3');
var e4Audio = new Audio(audioPath + 'E4.mp3');
var f4Audio = new Audio(audioPath + 'F4.mp3');
var g4Audio = new Audio(audioPath + 'G4.mp3');
var a5Audio = new Audio(audioPath + 'A5.mp3');
var b5Audio = new Audio(audioPath + 'B5.mp3');
var c5Audio = new Audio(audioPath + 'C5.mp3');
var d5Audio = new Audio(audioPath + 'D5.mp3');
var e5Audio = new Audio(audioPath + 'E5.mp3');
var f5Audio = new Audio(audioPath + 'F5.mp3');
var g5Audio = new Audio(audioPath + 'G5.mp3');
var a6Audio = new Audio(audioPath + 'A6.mp3');
var b6Audio = new Audio(audioPath + 'B6.mp3');

var whiteNoteAudios = [c3Audio, d3Audio, e3Audio, f3Audio, g3Audio, a4Audio, b4Audio, c4Audio, d4Audio, e4Audio, f4Audio, g4Audio, a5Audio, b5Audio, c5Audio, d5Audio, e5Audio, f5Audio, g5Audio, a6Audio, b6Audio];

var cs3Audio = new Audio(audioPath + 'Cs3.mp3');
var ds3Audio = new Audio(audioPath + 'Ds3.mp3');
var fs3Audio = new Audio(audioPath + 'Fs3.mp3');
var gs3Audio = new Audio(audioPath + 'Gs3.mp3');
var as4Audio = new Audio(audioPath + 'As4.mp3');
var cs4Audio = new Audio(audioPath + 'Cs4.mp3');
var ds4Audio = new Audio(audioPath + 'Ds4.mp3');
var fs4Audio = new Audio(audioPath + 'Fs4.mp3');
var gs4Audio = new Audio(audioPath + 'Gs4.mp3');
var as5Audio = new Audio(audioPath + 'As5.mp3');
var cs5Audio = new Audio(audioPath + 'Cs5.mp3');
var ds5Audio = new Audio(audioPath + 'Ds5.mp3');
var fs5Audio = new Audio(audioPath + 'Fs5.mp3');
var gs5Audio = new Audio(audioPath + 'Gs5.mp3');
var as6Audio = new Audio(audioPath + 'As6.mp3');

var blackNoteAudios = [cs3Audio, ds3Audio, fs3Audio, gs3Audio, as4Audio, cs4Audio, ds4Audio, fs4Audio, gs4Audio, as5Audio, cs5Audio, ds5Audio, fs5Audio, gs5Audio, as6Audio];

var mouseDown = 0;

var main = function() {

	document.body.onmousedown = function() {
		mouseDown = 1;
	}

	document.body.onmouseup = function() {
		mouseDown = 0;
	}

	$('.piano-white').mousedown(function() {
		for (i = 0; i < whiteKeys.length; i++) {
			if ($(this).hasClass(whiteKeys[i])) {
				whiteNoteAudios[i].play();
			}
			this.style.backgroundColor = 'cyan';
		}
	})

	$('.piano-white').mouseup(function() {
		for (i = 0; i < whiteKeys.length; i++) {
			if ($(this).hasClass(whiteKeys[i])) {
				whiteNoteAudios[i].pause();
				whiteNoteAudios[i].currentTime = 0;
			}
		}
		this.style.backgroundColor = 'white';
	})

	$('.piano-white').mouseleave(function() {
		for (i = 0; i < whiteKeys.length; i++) {
			if ($(this).hasClass(whiteKeys[i])) {
				whiteNoteAudios[i].pause();
				whiteNoteAudios[i].currentTime = 0;
			}
		}
		this.style.backgroundColor = 'white';
	})

	$('.piano-white').mouseenter(function() {
		if (mouseDown == 1) {
			for (i = 0; i < whiteKeys.length; i++) {
				if ($(this).hasClass(whiteKeys[i])) {
					whiteNoteAudios[i].play();
				}
				this.style.backgroundColor = 'cyan';
			}
		}
	})

	$('.piano-black').mousedown(function() {
		for (i=0; i < blackKeys.length; i++) {
			if ($(this).hasClass(blackKeys[i])) {
				blackNoteAudios[i].play();
			}
		}
		this.style.backgroundColor = 'cyan';
	})

	$('.piano-black').mouseenter(function() {
		if (mouseDown == 1) {
			for (i=0; i < blackKeys.length; i++) {
				if ($(this).hasClass(blackKeys[i])) {
					blackNoteAudios[i].play();
				}
			}
			this.style.backgroundColor = 'cyan';
		}
	})

	$('.piano-black').mouseup(function() {
		for (i=0; i < blackKeys.length; i++) {
			if ($(this).hasClass(blackKeys[i])) {
				blackNoteAudios[i].pause();
				blackNoteAudios[i].currentTime = 0;
			}
		}
		this.style.backgroundColor = 'black';
	})

	$('.piano-black').mouseleave(function() {
		for (i=0; i < blackKeys.length; i++) {
			if ($(this).hasClass(blackKeys[i])) {
				blackNoteAudios[i].pause();
				blackNoteAudios[i].currentTime = 0;
			}
		}
		this.style.backgroundColor = 'black';
	})

};



$(document).ready(main);