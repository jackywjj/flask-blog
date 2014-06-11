# coding=utf8
import os
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from flask.ext.paginate import Pagination
from wtforms import Form
from wtforms.ext.appengine.db import model_form


from config import POSTS_PER_PAGE
from app import db
from app.models.models import *
from app.models.forms import *
from app.helpers.helpers import *

admin = Blueprint('admin', __name__, url_prefix='/admin120')

# globale variables
data = {}
@admin.before_request
def before_request():
	if 'login' in request.url_rule.rule:
		pass
	else:
		if 'user_id' in session:
			pass
		else:
			return redirect(url_for('admin.adminLogin'))

# Set the route and accepted methods
@admin.route('/', methods=['GET', 'POST'])
@admin.route('/login/', methods=['GET', 'POST'])
def adminLogin():
	form = LoginForm(request.form)
	if request.method == "POST" and form.validate():
		return redirect(url_for('admin.categoryIndex'))
	return render_template("admin/login.html",form=form)

@admin.route('/logout/')
def adminLogout():
	session.pop('user_id', None)
	return redirect(url_for('admin.adminLogin'))
	
'''
Comment controllers
'''
@admin.route('/comment/')
@admin.route('/comment/index/')
def commentIndex():
	comments = Comment.query.order_by("-id").all()
	return render_template("admin/comment/index.html", data=data, comments=comments)
	
@admin.route('/comment/<id>/delete/')
def commentDelete(id):
	comment = Comment.query.get(id)
	db.session.delete(comment)
	db.session.commit()
	return redirect(url_for('admin.commentIndex'))
'''
Category controllers
'''
@admin.route('/category/')
@admin.route('/category/index/')
def categoryIndex():
	categories = Category.query.all()
	data['categories'] = categories
	return render_template("admin/category/index.html", data=data)

@admin.route('/category/create/', methods=['GET', 'POST'])
def categoryCreate():
	form = CategoryForm(request.form)
	if request.method == "POST" and form.validate():
		category = Category(form.title.data)
		db.session.add(category)
		db.session.commit()
		return redirect(url_for('admin.categoryIndex'))
	return render_template("admin/category/create.html", data=data, form=form)

@admin.route('/category/<id>/edit/', methods=['GET', 'POST'])
def categoryUpdate(id):
	category = Category.query.get(id)
	form = CategoryForm(request.form, category)
	if request.method == "POST" and form.validate():
		category.title = form.title.data
		db.session.commit()
		return redirect(url_for('admin.categoryIndex'))
	return render_template("admin/category/update.html", form=form, category=category)

@admin.route('/category/<id>/delete/')
def categoryDelete(id):
	category = Category.query.get(id)
	db.session.delete(category)
	db.session.commit()
	return redirect(url_for('admin.categoryIndex'))

@admin.route('/category/<id>/status/')
def categoryStatus(id):
	category = Category.query.get(id)
	if category.status == 1:
		category.status = 0
	elif category.status == 0:
		category.status = 1
	db.session.commit()
	return redirect(url_for('admin.categoryIndex'))

'''
Post controllers
'''
@admin.route('/post/')
@admin.route('/post/index/')
@admin.route('/post/<int:page>/')
@admin.route('/post/index/<int:page>/')
def postIndex(page = 1):
	category_id = request.args.get('category_id') if request.args.get('category_id') else 1
	categories = Category.query.all()
	try:
		posts = Post.query.filter_by(category_id=category_id).paginate(page=page, per_page=POSTS_PER_PAGE)
	except:
		return redirect(url_for('admin.postIndex', category_id=category_id))

	data['categories'] = categories
	data['category_id'] = int(category_id)
	return render_template("admin/post/index.html", data=data, posts=posts, category_id=category_id, page=page)

@admin.route('/post/create/', methods=['GET', 'POST'])
def postCreate():
	category_id = request.args.get('category_id') if request.args.get('category_id') else 1
	form = PostForm(request.form, category_id=category_id)
	if request.method == "POST" and form.validate():
		post = Post(form.title.data, form.category_id.data, form.content.data)
		db.session.add(post)
		db.session.commit()
		file = request.files['post_image']
		if file:
			filename = resizePostImage(file, post.id)
			post.post_image = filename
			db.session.commit()
		return redirect(url_for('admin.postIndex', category_id=category_id))	
	categories = Category.query.all()
	data['categories'] = categories
	data['category_id'] = int(category_id)
	return render_template("admin/post/create.html", data=data, form=form)

@admin.route('/post/<id>/edit/', methods=['GET', 'POST'])
def postUpdate(id):
	post = Post.query.get(id)
	form = PostForm(request.form, post)
	if request.method == "POST" and form.validate():
		post.title = form.title.data
		post.category_id = form.category_id.data
		post.content = form.content.data
		file = request.files['post_image']
		if file:
			filename = resizePostImage(file, post.id)
			post.post_image = filename
		db.session.commit()
		return redirect(url_for('admin.postIndex', category_id=post.category_id))
	return render_template("admin/post/update.html", data=data, form=form, post=post)

@admin.route('/post/<id>/delete/')
def postDelete(id):
	category_id = request.args.get('category_id') if request.args.get('category_id') else 1
	post = Post.query.get(id)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('admin.postIndex', category_id=category_id))
    
@admin.route('/post/<id>/status/')
def postStatus(id):
	category_id = request.args.get('category_id') if request.args.get('category_id') else 1
	page = request.args.get('page') if request.args.get('page') else 1
	post = Post.query.get(id)
	if post.status == 1:
		post.status = 0
	elif post.status == 0:
		post.status = 1
	db.session.commit()
	return redirect(url_for('admin.postIndex', page=page, category_id=category_id))
'''
Album controllers
'''
@admin.route('/album/')
@admin.route('/album/index/')
def albumIndex():
	albums = Album.query.all()
	data['albums'] = albums
	return render_template("admin/album/index.html", data=data)

@admin.route('/album/create/', methods=['GET', 'POST'])
def albumCreate():
	form = AlbumForm(request.form)
	if request.method == "POST" and form.validate():
		album = Album(form.title.data)
		db.session.add(album)
		db.session.commit()
		return redirect(url_for('admin.albumIndex'))
	return render_template("admin/album/create.html", form=form)

@admin.route('/album/<id>/edit/', methods=['GET', 'POST'])
def albumUpdate(id):
	album = Album.query.get(id)
	form = CategoryForm(request.form, album)
	if request.method == "POST" and form.validate():
		album.title = form.title.data
		db.session.commit()
		return redirect(url_for('admin.albumIndex'))
	return render_template("admin/album/update.html", form=form, album=album)

@admin.route('/album/<id>/delete/')
def albumDelete(id):
	album = Album.query.get(id)
	db.session.delete(album)
	db.session.commit()
	return redirect(url_for('admin.albumIndex'))

@admin.route('/album/<id>/status/')
def albumStatus(id):
	album = Album.query.get(id)
	if album.status == 1:
		album.status = 0
	elif album.status == 0:
		album.status = 1
	db.session.commit()
	return redirect(url_for('admin.albumIndex'))
'''
Photo controllers
'''
@admin.route('/photo/')
@admin.route('/photo/index/')
@admin.route('/photo/<int:page>/')
@admin.route('/photo/index/<int:page>/')
def photoIndex(page = 1):
	album_id = request.args.get('album_id') if request.args.get('album_id') else 1
	albums = Album.query.all()
	try:
		photos = Photo.query.filter_by(album_id=album_id).order_by("-id").paginate(page=page, per_page=POSTS_PER_PAGE)
	except:
		return redirect(url_for('admin.photoIndex', album_id=album_id))

	data['albums'] = albums
	data['album_id'] = int(album_id)
	return render_template("admin/photo/index.html", data=data, photos=photos, album_id=album_id, page=page)

@admin.route('/photo/create/', methods=['GET', 'POST'])
def photoCreate():
	album_id = request.args.get('album_id') if request.args.get('album_id') else 1
	form = PhotoForm(request.form, album_id=album_id)
	if request.method == "POST" and form.validate():
		photo = Photo(form.title.data, form.album_id.data)
		db.session.add(photo)
		db.session.commit()
		file = request.files['photo_image']
		if file:
			file_infor = resizePhotoImage(file, photo.id)
			photo.photo_image = file_infor['filename']
			photo.photo_image_ext = file_infor['fileext']
			db.session.commit()
		return redirect(url_for('admin.photoIndex', album_id=album_id))
	albums = Album.query.all()
	data['albums'] = albums
	data['album_id'] = int(album_id)
	return render_template("admin/photo/create.html", data=data, form=form)

@admin.route('/photo/<id>/edit/', methods=['GET', 'POST'])
def photoUpdate(id):
	#album_id = request.args.get('album_id') if request.args.get('album_id') else 1
	page = request.args.get('page') if request.args.get('page') else 1
	photo = Photo.query.get(id)
	form = PhotoForm(request.form, photo)
	if request.method == "POST" and form.validate():
		photo.title = form.title.data
		photo.album_id = form.album_id.data
		file = request.files['photo_image']
		if file:
			file_infor = resizePhotoImage(file, id)
			photo.photo_image = file_infor['filename']
			photo.photo_image_ext = file_infor['fileext']
		db.session.commit()
		return redirect(url_for('admin.photoIndex', album_id=photo.album_id, page=page))
	return render_template("admin/photo/update.html", data=data, form=form, photo=photo)

@admin.route('/photo/<id>/delete/')
def photoDelete(id):
	album_id = request.args.get('album_id') if request.args.get('album_id') else 1
	page = request.args.get('page') if request.args.get('page') else 1
	photo = Photo.query.get(id)
	db.session.delete(photo)
	db.session.commit()
	return redirect(url_for('admin.photoIndex', album_id=album_id, page=page))
'''
User controller
'''
@admin.route('/user/')
@admin.route('/user/index/')
def userIndex():
	users = User.query.all()
	data['users'] = users
	return render_template("admin/user/index.html", data=data)

@admin.route('/user/create/', methods=['GET', 'POST'])
def userCreate():
	form = UserForm(request.form)
	if request.method == "POST" and form.validate():
		user = User(form.user_name.data, form.user_pass.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('admin.userIndex'))
	return render_template("admin/user/create.html", form=form)

@admin.route('/user/<id>/edit/', methods=['GET', 'POST'])
def userUpdate(id):
	user = User.query.get(id)
	form = UserForm(request.form, user)
	if request.method == "POST" and form.validate():
		user.user_name = form.user_name.data
		user.user_pass = form.user_pass.data
		db.session.commit()
		return redirect(url_for('admin.userIndex'))
	return render_template("admin/user/update.html", form=form, user=user)

@admin.route('/user/<id>/delete/')
def userDelete(id):
	user = User.query.get(id)
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('admin.userIndex'))

'''
View log controller
'''
@admin.route('/viewlog/')
@admin.route('/viewlog/index/')
@admin.route('/viewlog/<int:page>/')
@admin.route('/viewlog/index/<int:page>/')
def viewlogIndex(page=1):
	try:
		models = Viewlog.query.order_by("-id").paginate(page=page, per_page=POSTS_PER_PAGE)
	except:
		return redirect(url_for('admin.viewlogIndex'))
	return render_template("admin/viewlog/index.html", models=models)






