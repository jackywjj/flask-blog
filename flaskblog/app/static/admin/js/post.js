$(function() {
	$('.essay-category').change(function(){
		var category_id = $(this).val();
		var url = "/admin/post/?category_id=" + category_id;
		window.location = url;
	});
});