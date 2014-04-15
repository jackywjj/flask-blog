import time
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import event
from app.helpers.helpers import *

class Base(db.Model):
	__abstract__	= True
	id				= db.Column(db.Integer, primary_key=True)
	created_at		= db.Column(db.DateTime,  default=db.func.current_timestamp())
	updated_at		= db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class User(Base):
	__tablename__ = 'users'
	user_name    = db.Column(db.String(255),  nullable=False)
	user_pass = db.Column(db.String(255),  nullable=False)
	def __init__(self, user_name, user_pass):
		self.user_name	= user_name
		self.user_pass	= user_pass
	def __repr__(self):
		return '<User %r>' % (self.name)
	def check_password(self, userPass):
		if self.user_pass == userPass:
			return True
		else:
			return False

class Album(Base):
	__tablename__ = 'albums'
	title = db.Column(db.String(255),  nullable=False)
	status = db.Column(db.Boolean(),  nullable=False)
	def __init__(self, title):
		self.title      = title
		self.status     = 0

class Photo(Base):
	__tablename__ = 'photos'
	title = db.Column(db.String(255),  nullable=False)
	album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
	photo_image = db.Column(db.String(255))
	photo_image_ext = db.Column(db.String(5))
	album = relationship("Album", order_by="Album.id", backref="photo")
	def __init__(self, title, album_id):
		self.title          = title
		self.album_id    	= album_id
		self.photo_image		= ''
	def renderImage(self, type):
		dir = renderPhotoImageUrl(self.id)
		if self.photo_image != "":
			if self.photo_image_ext:
				ext = self.photo_image_ext
			else:
				ext = ''
			return dir + self.photo_image + '-' + type + ext
		else:
			return False

class Category(Base):
	__tablename__ = 'categories'
	title = db.Column(db.String(255),  nullable=False)
	status = db.Column(db.Boolean(),  nullable=False)
	def __init__(self, title):
		self.title      = title
		self.status     = 0


class Post(Base):
	__tablename__ = 'posts'
	title = db.Column(db.String(255),  nullable=False)
	content = db.Column(db.Text(),  nullable=False)
	summary = db.Column(db.Text(), nullable=False)
	status = db.Column(db.Boolean(),  nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	category = relationship("Category", order_by="Category.id", backref="post")
	post_image = db.Column(db.String(255))
	created_month = db.Column(db.String(7), default='')
	def __init__(self, title, category_id, content):
		self.title          = title
		self.category_id    = category_id
		self.content    	= content
		self.summary		= self.getSummary()
		self.status         = 0
		self.created_month  = time.strftime('%Y-%m',time.localtime(time.time()))
		self.post_image		= ''
	def getSummary(self):
		tmpSumm = self.content.split("<!--more-->")
		return tmpSumm[0]
	def renderImage(self):
		dir = renderPostImageUrl(self.id)
		if self.post_image != "":
			return dir + self.post_image
		else:
			return False
	def renderCommentCount(self):
		return Comment.query.filter_by(post_id=self.id).count()

class Comment(Base):
	__tablename__ = 'comments'
	user_name = db.Column(db.String(255),  nullable=False)
	message = db.Column(db.Text(),  nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	post = relationship("Post", order_by="Post.id", backref="comment")
	def __init__(self, user_name, message, post_id):
		self.user_name      = user_name
		self.message    	= message
		self.post_id    	= post_id
			
@event.listens_for(Post, 'before_update')
def receive_before_update(mapper, connection, target):
	target.summary		= target.getSummary()



