$(function() {
	$('.delete').click(function(){
		var url = $(this).attr('href');
		if (confirm("Are you sure?")) {
			window.location = url;
		}
		return false;
	});
});