
var whiteKeys = [
	'C3', 'D3', 'E3', 'F3', 'G3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4',
	'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'A6', 'B6'
];

var blackKeys = [
	'Csharp3', 'Dsharp3', 'Fsharp3', 'Gsharp3', 'Asharp4', 'Csharp4', 'Dsharp4', 'Fsharp4', 'Gsharp4', 'Asharp5',
	'Csharp5', 'Dsharp5', 'Fsharp5', 'Gsharp5', 'Asharp6'
];

var audioPath = '../../static/study/audio/';
var c3Audio = new Audio(audioPath + 'C3.mp3');
var c4Audio = new Audio(audioPath + 'C4.mp3');
var c5Audio = new Audio(audioPath + 'C5.mp3');
var a4Audio = new Audio(audioPath + 'A4.mp3');
var a5Audio = new Audio(audioPath + 'A5.mp3');
var a6Audio = new Audio(audioPath + 'A6.mp3');
var dSharp3Audio = new Audio(audioPath + 'Ds3.mp3');
var dSharp4Audio = new Audio(audioPath + 'Ds4.mp3');
var dSharp5Audio = new Audio(audioPath + 'Ds5.mp3');
var fSharp4Audio = new Audio(audioPath + 'Fs4.mp3');
var fSharp5Audio = new Audio(audioPath + 'Fs5.mp3');
var fSharp6Audio = new Audio(audioPath + 'Fs6.mp3');

var main = function() {
	$('.piano-white').click(function() {
		for (i = 0; i < whiteKeys.length; i++) {
			if ($(this).hasClass(whiteKeys[i])) {
				if ($(this).hasClass('C3')) {
					c3Audio.play();
				}
				else if ($(this).hasClass('C4')) {
					c4Audio.play();
				} else if ($(this).hasClass('C5')) {
					c5Audio.play();
				} else if ($(this).hasClass('A4')) {
					a4Audio.play();
				} else if ($(this).hasClass('A5')) {
					a5Audio.play();
				} else if ($(this).hasClass('A6')) {
					a6Audio.play();
				} else {
					alert(whiteKeys[i]);
				}
			}
		}
	})

	$('.piano-black').click(function() {
		for (i=0; i < blackKeys.length; i++) {
			if ($(this).hasClass(blackKeys[i])) {
				if ($(this).hasClass('Dsharp3')) {
					dSharp3Audio.play();
				} else if ($(this).hasClass('Dsharp4')) {
					dSharp4Audio.play();
				} else if ($(this).hasClass('Dsharp5')) {
					dSharp5Audio.play();
				} else if ($(this).hasClass('Fsharp4')) {
					fSharp4Audio.play();
				} else if ($(this).hasClass('Fsharp5')) {
					fSharp5Audio.play();
				} else if ($(this).hasClass('Fsharp6')) {
					fSharp6Audio.play();
				} else {
					alert(blackKeys[i]);
				}
			}
		}
	})
};



$(document).ready(main);