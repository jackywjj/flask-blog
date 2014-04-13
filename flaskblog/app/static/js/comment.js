function checkform() {
	if ($('#user_name').val() == "") {
		alert("请填写姓名。")
		$("#user_name").focus();
		return false;
	} else if ($('#message').val() == "") {
		alert("请填写评论内容。")
		$("#message").focus();
		return false;
	}
	return true;
}