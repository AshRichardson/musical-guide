const whiteKeys = [
	'C3', 'D3', 'E3', 'F3', 'G3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'A6', 'B6'
];

const blackKeys = [
	'Cs3', 'Ds3', 'Fs3', 'Gs3', 'As4', 'Cs4', 'Ds4', 'Fs4', 'Gs4', 'As5', 'Cs5', 'Ds5', 'Fs5', 'Gs5', 'As6'
];

const audioPath = '../../static/study/audio/';

var whiteNoteAudios = [];
for (var i = 0; i < whiteKeys.length; i++) {
	whiteNoteAudios.push(new Audio(audioPath + whiteKeys[i] + '.mp3'));
}

var blackNoteAudios = [];
for (var i = 0; i < blackKeys.length; i++) {
	blackNoteAudios.push(new Audio(audioPath + blackKeys[i] + '.mp3'));
}

const allKeyArray = whiteKeys.concat(blackKeys);

var mouseDown = 0;
var d = new Date();
var originalStartTime = d.getTime();
var thisNoteStart = 0;
var endTime = 0;

function generate_note(path, params) {
	var form = $('<form></form>');
	form.attr("method", "post");
	form.attr("action", path);
	$.each(params, function(key, val) {
		var field = $('<input></input>');
		field.attr('type', 'hidden');
		field.attr('name', key);
		field.attr('value', value);
		form.append(field);
	});
	$(document.body).append(form);
	form.submit();
}

function ai_response(keyColour) {
	const keyArray = keyColour == 'white' ? whiteKeys : blackKeys;
	const audioArray = keyColour == 'white' ? whiteNoteAudios : blackNoteAudios;
	$.ajax({
		url: 'magenta_gen/',
		method: 'POST',
		dataType:'json',
		data: {
			'note': keyArray[i]
		},
		success: function(msg) {
			$.each(msg, function(key, val) {
				for (var noteIndex = 0; noteIndex < val.length; noteIndex++) {
					note = val[noteIndex];
					const noteName = note[0];
					const noteStart = note[1];
					const noteDuration = note[2];
					let keyIndex = 0;
					for (keyIndex = 0; keyIndex < allKeyArray.length; keyIndex++) {
						let thisIndex = keyIndex;
						if(allKeyArray[thisIndex] == noteName) {
							setTimeout(function() {
								if (thisIndex > 20) {
									thisIndex -= 21;
								}
								audioArray[thisIndex].play()
								let element = document.querySelectorAll('div.'.concat(noteName))[0];
								element.style.backgroundColor = 'yellow';
								setTimeout(function() {							
									if ($(element).hasClass('piano-white')) {
										element.style.backgroundColor = 'white';
										whiteNoteAudios[thisIndex].pause();
										whiteNoteAudios[thisIndex].currentTime = 0;	
									} else {
										element.style.backgroundColor = 'black';
										blackNoteAudios[thisIndex].pause();
										blackNoteAudios[thisIndex].currentTime = 0;	
									}
								}, noteDuration);								
							}, noteStart);
						}
					}
				}
			})
		}
	});
}

function note_on(noteDiv) {
	const keyArray = $(noteDiv).hasClass('piano-white') ? whiteKeys : blackKeys;
	const audioArray = $(noteDiv).hasClass('piano-white') ? whiteNoteAudios : blackNoteAudios;
	for (i = 0; i < keyArray.length; i++) {
		if ($(noteDiv).hasClass(keyArray[i])) {
			audioArray[i].play();
			thisNoteStart = d.getTime() - originalStartTime;
		}
		noteDiv.style.backgroundColor = 'cyan';
	}
}

function note_off(noteDiv) {
	const keyArray = $(noteDiv).hasClass('piano-white') ? whiteKeys : blackKeys;
	const audioArray = $(noteDiv).hasClass('piano-white') ? whiteNoteAudios : blackNoteAudios;		
	const colour = $(noteDiv).hasClass('piano-white') ? 'white' : 'black';
	if (noteDiv.style.backgroundColor == 'cyan'){
		for (i = 0; i < keyArray.length; i++) {
			if ($(noteDiv).hasClass(keyArray[i])) {
				audioArray[i].pause();
				audioArray[i].currentTime = 0;
				endTime = d.getTime() - originalStartTime;
				ai_response(colour);
			}
		}
		noteDiv.style.backgroundColor = colour;
	}
}

var main = function() {

	document.body.onmousedown = function() {
		mouseDown = 1;
	}

	document.body.onmouseup = function() {
		mouseDown = 0;
	}

	$('.piano-key').mousedown(function() {
		note_on(this);
	})

	$('.piano-key').mouseenter(function() {
		if (mouseDown == 1) {
			note_on(this);
		}
	})

	$('.piano-key').mouseup(function() {
		note_off(this);
	})

	$('.piano-key').mouseleave(function() {
		if (this.style.backgroundColor == 'cyan') {
			note_off(this);
		}
	})

};







// The below code is from https://github.com/realpython/django-form-fun/blob/master/part1/main.js
// Implements csrf for ajax so that data is more secure
$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

$(document).ready(main);