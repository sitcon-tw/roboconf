$(document).ready(function() {
	$("textarea").keyup(function(e) {
		var $t = $(this);
		var lines = parseInt($t.val().length / 56) + $t.val().match(/\n/g).length;
		var em = parseFloat($t.css("font-size"));
		var dest = parseInt((lines + 2) * em * 1.15) + 
			parseFloat($t.css("border-top-width") || 0) + parseFloat($t.css("border-bottom-width") || 0);
		$t.height(dest);
	});
});
$(document).bind('ajaxSend', function(e, xhr, settings) {
	if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)))
		xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
});

