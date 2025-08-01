jQuery(function($) {$(document).ready(function() {
						$('#rotator').crossSlide(
							{sleep: 2, fade: 1, debug: true},
							[
							{src: '1.jpeg'},
							{src: '2.jpg'},
							{src: '3.jpg'},
							{src: '4.jpg'},
							]
						);
					});});