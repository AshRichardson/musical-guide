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
				$.ajax({
					url: 'gen/',
					method: 'POST',
					dataType:'json',
					data: {
						'note': whiteKeys[i]
					},
					success: function(msg) {
						$.each(msg, function(key, val) {
							for (i = 0; i < whiteKeys.length; i++) {
								if(whiteKeys[i] == val) {
									whiteNoteAudios[i].play();
								}
							}
							var elements = document.querySelectorAll('div.'.concat(val));
							console.log(elements);
							for (var i = 0; i < elements.length; i++) {
								elements[i].style.backgroundColor = 'yellow';
							}
						})
					}
				});
			}
			this.style.backgroundColor = 'cyan';
		}
	})

	$('.piano-white').mouseup(function() {
		if (this.style.backgroundColor == 'cyan'){
			for (i = 0; i < whiteKeys.length; i++) {
				if ($(this).hasClass(whiteKeys[i])) {
					whiteNoteAudios[i].pause();
					whiteNoteAudios[i].currentTime = 0;
					$.ajax({
						url: 'off/',
						method: 'POST',
						dataType:'json',
						data: {
							'note': whiteKeys[i]
						},
						success: function(msg) {
							$.each(msg, function(key, val) {
								for (i = 0; i < whiteKeys.length; i++) {
									if(whiteKeys[i] == val) {
										whiteNoteAudios[i].pause();
										whiteNoteAudios[i].currentTime = 0;
									}
								}
								var elements = document.querySelectorAll('div.'.concat(val));
								console.log(elements);
								for (var i = 0; i < elements.length; i++) {
									elements[i].style.backgroundColor = 'white';
								}
							})
						}
					});
				}
			}
			this.style.backgroundColor = 'white';
		}
	})

	$('.piano-white').mouseleave(function() {
		if (this.style.backgroundColor == 'cyan'){
			for (i = 0; i < whiteKeys.length; i++) {
				if ($(this).hasClass(whiteKeys[i])) {
					whiteNoteAudios[i].pause();
					whiteNoteAudios[i].currentTime = 0;
					$.ajax({
						url: 'off/',
						method: 'POST',
						dataType:'json',
						data: {
							'note': whiteKeys[i]
						},
						success: function(msg) {
							$.each(msg, function(key, val) {
								for (i = 0; i < whiteKeys.length; i++) {
									if(whiteKeys[i] == val) {
										whiteNoteAudios[i].pause();
										whiteNoteAudios[i].currentTime = 0;
									}
								}
								var elements = document.querySelectorAll('div.'.concat(val));
								console.log(elements);
								for (var i = 0; i < elements.length; i++) {
									elements[i].style.backgroundColor = 'white';
								}
							})
						}
					});
				}
			}
			this.style.backgroundColor = 'white';
		}
	})

	$('.piano-white').mouseenter(function() {
		if (mouseDown == 1) {
			for (i = 0; i < whiteKeys.length; i++) {
				if ($(this).hasClass(whiteKeys[i])) {
					whiteNoteAudios[i].play();
					$.ajax({
						url: 'gen/',
						method: 'POST',
						dataType:'json',
						data: {
							'note': whiteKeys[i]
						},
						success: function(msg) {
							$.each(msg, function(key, val) {
								for (i = 0; i < whiteKeys.length; i++) {
									if(whiteKeys[i] == val) {
										whiteNoteAudios[i].play();
									}
								}
								var elements = document.querySelectorAll('div.'.concat(val));
								console.log(elements);
								for (var i = 0; i < elements.length; i++) {
									elements[i].style.backgroundColor = 'yellow';
								}
							})
						}
					});
				}
				this.style.backgroundColor = 'cyan';
			}
		}
	})

	$('.piano-black').mousedown(function() {
		for (i=0; i < blackKeys.length; i++) {
			if ($(this).hasClass(blackKeys[i])) {
				blackNoteAudios[i].play();
				$.ajax({
					url: 'gen/',
					method: 'POST',
					dataType:'json',
					data: {
						'note': blackKeys[i]
					},
					success: function(msg) {
						$.each(msg, function(key, val) {
							for (i = 0; i < blackKeys.length; i++) {
								if(blackKeys[i] == val) {
									blackNoteAudios[i].play();
								}
							}
							var elements = document.querySelectorAll('div.'.concat(val));
							console.log(elements);
							for (var i = 0; i < elements.length; i++) {
								elements[i].style.backgroundColor = 'yellow';
							}
						})
					}
				});
			}
		}
		this.style.backgroundColor = 'cyan';
	})

	$('.piano-black').mouseenter(function() {
		if (mouseDown == 1) {
			for (i=0; i < blackKeys.length; i++) {
				if ($(this).hasClass(blackKeys[i])) {
					blackNoteAudios[i].play();
					$.ajax({
						url: 'gen/',
						method: 'POST',
						dataType:'json',
						data: {
							'note': blackKeys[i]
						},
						success: function(msg) {
							$.each(msg, function(key, val) {
								for (i = 0; i < blackKeys.length; i++) {
									if(blackKeys[i] == val) {
										blackNoteAudios[i].play();
									}
								}
								var elements = document.querySelectorAll('div.'.concat(val));
								console.log(elements);
								for (var i = 0; i < elements.length; i++) {
									elements[i].style.backgroundColor = 'yellow';
								}
							})
						}
					});
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
				$.ajax({
					url: 'off/',
					method: 'POST',
					dataType:'json',
					data: {
						'note': blackKeys[i]
					},
					success: function(msg) {
						$.each(msg, function(key, val) {
							for (i = 0; i < blackKeys.length; i++) {
								if(blackKeys[i] == val) {
									blackNoteAudios[i].pause();
									blackNoteAudios[i].currentTime = 0;
								}
							}
							var elements = document.querySelectorAll('div.'.concat(val));
							console.log(elements);
							for (var i = 0; i < elements.length; i++) {
								elements[i].style.backgroundColor = 'black';
							}
						})
					}
				});
			}
		}
		this.style.backgroundColor = 'black';
	})

	$('.piano-black').mouseleave(function() {
		for (i=0; i < blackKeys.length; i++) {
			if ($(this).hasClass(blackKeys[i])) {
				blackNoteAudios[i].pause();
				blackNoteAudios[i].currentTime = 0;
				$.ajax({
					url: 'off/',
					method: 'POST',
					dataType:'json',
					data: {
						'note': blackKeys[i]
					},
					success: function(msg) {
						$.each(msg, function(key, val) {
							for (i = 0; i < blackKeys.length; i++) {
								if(blackKeys[i] == val) {
									blackNoteAudios[i].pause();
									blackNoteAudios[i].currentTime = 0;
								}
							}
							var elements = document.querySelectorAll('div.'.concat(val));
							console.log(elements);
							for (var i = 0; i < elements.length; i++) {
								elements[i].style.backgroundColor = 'black';
							}
						})
					}
				});
			}
		}
		this.style.backgroundColor = 'black';
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