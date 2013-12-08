$(document).bind('ajaxSend', function(e, xhr, settings) {
	if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)))
		xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
});

var Roboconf = (function(){
	function defSuccess(d,t,j) { window.location.reload(); }
	return {
		post: function(url, args, options) {
			$.ajax({
				data: args,
				success: (options && options.success) || defSuccess,
				url: url, type: 'POST'
			});
		},
		put: function(url, args, options) {
			$.ajax({
				contentType: 'application/json',
				data: JSON.stringify(args),
				success: (options && options.success) || defSuccess,
				url: url, type: 'PUT'
			});
		},
		delete: function(url, args, options) {
			$.ajax({
				success: (options && options.success) || defSuccess,
				url: url, type: 'DELETE'
			})
		}
	}
})()