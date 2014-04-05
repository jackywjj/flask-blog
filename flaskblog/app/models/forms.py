# coding=utf8
from flask import session
from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators, SelectField, FileField
from app.models.models import *

class LoginForm(Form):
	user_name = TextField(u'用户名', [ validators.Required(message=u"用户名不能为空。") ])
	user_pass = PasswordField(u'密码', [ validators.Required(message=u"密码不能为空。") ])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False
		user = User.query.filter_by(user_name=self.user_name.data).first()
		if user is None:
			self.user_name.errors.append('Unknown username')
			return False
		if not user.check_password(self.user_pass.data):
			self.user_pass.errors.append(u'密码错误。')
			return False
		self.user = user
		session['user_id'] = user.id
		return True

class UserForm(Form):
	user_name = TextField(u'用户名', [ validators.Required(message=u"用户名不能为空。") ])
	user_pass = TextField(u'密码', [ validators.Required(message=u"密码不能为空。") ])

class CategoryForm(Form):
	title = TextField(u'标题', [ validators.Required(message=u"标题不能为空")])

class PostForm(Form):
	title = TextField(u'标题', [ validators.Required(message=u"标题不能为空")])
	content = TextAreaField(u'文章内容', [ validators.Required(message=u"内容不能为空")])
	category_id = SelectField(u'文章分类', choices=[(c.id, c.title) for c in Category.query.order_by('id')], coerce=int)
	post_image = FileField(u'文章图片')

class AlbumForm(Form):
	title = TextField(u'标题', [ validators.Required(message=u"标题不能为空")])
	
class PhotoForm(Form):
	title = TextField(u'标题')
	album_id = SelectField(u'相册', choices=[(c.id, c.title) for c in Album.query.order_by('id')], coerce=int)
	photo_image = FileField(u'图片')