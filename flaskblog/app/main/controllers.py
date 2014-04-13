# coding=utf8
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import Markup

from app import db
from app.models.models import *
from app.models.forms import CommentForm
main = Blueprint('main', __name__, url_prefix='/')

@main.route('')
def index():
	categories = Category.query.filter_by(status='1').order_by('title').all()
	posts = Post.query.filter_by(status='1').order_by("-id").all()
	dates = db.session.query(Post, "created_month").group_by("created_month").all()
	return render_template("blog/index.html", categories=categories, posts=posts, dates=dates)

@main.route('blog/category/<id>/')
def category(id):
	categories = Category.query.filter_by(status='1').order_by('title').all()
	posts = Post.query.filter_by(status='1').order_by("-id").filter_by(category_id=id).all()
	dates = db.session.query(Post, "created_month").group_by("created_month").all()
	return render_template("blog/index.html", categories=categories, posts=posts, dates=dates)
	
@main.route('blog/archive/<month>/')
def archive(month):
	categories = Category.query.filter_by(status='1').order_by('title').all()
	posts = Post.query.filter_by(status='1').order_by("-id").filter_by(created_month=month).all()
	dates = db.session.query(Post, "created_month").group_by("created_month").all()
	return render_template("blog/index.html", categories=categories, posts=posts, dates=dates)
	
@main.route('blog/<id>/', methods=['GET', 'POST'])
def detail(id):
	form = CommentForm(request.form)
	if request.method == "POST" and form.validate():
		comment = Comment(form.user_name.data, form.message.data, id)
		db.session.add(comment)
		db.session.commit()
		flash(u'感谢您的留言！')
		return redirect(url_for('main.detail', id=id))
	post = Post.query.get(id)
	comments = Comment.query.filter_by(post_id=id).order_by("-id").all()
	return render_template("blog/detail.html", post=post, form=form, comments=comments)

@main.route('album/')
@main.route('album/<id>/')
def albumIndex(id=1):
	albums = Album.query.order_by("-id").all()
	photos = Photo.query.filter_by(album_id=id).order_by("-id")
	return render_template("album/index.html", albums=albums, photos=photos)
	
@main.route('aboutme/')
def aboutmeIndex():
	return render_template("aboutme/index.html")