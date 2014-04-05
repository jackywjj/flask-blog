$(function() {
	$('.essay-album').change(function(){
		var album_id = $(this).val();
		var url = "/admin/photo/?album_id=" + album_id;
		window.location = url;
	});
});