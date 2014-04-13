$(function() {
	$('.essay-category').change(function(){
		var category_id = $(this).val();
		var url = "/admin120/post/?category_id=" + category_id;
		window.location = url;
	});
});