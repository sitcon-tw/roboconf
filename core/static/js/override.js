$(document).ready(function() {
	$("textarea").keyup(function(e) {
		var $t = $(this);
		var from = $t.outerHeight();
		var dest = this.scrollHeight + 
			parseFloat($t.css("border-top-width") || 0) + parseFloat($t.css("border-bottom-width") || 0) +
			parseInt(parseFloat($t.css("font-size"))*1.15);
		if (from < dest) $t.height(from + (dest - from));
	});
});
