# coding=utf8
# Import flask dependencies
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import Markup
from flask import request
from werkzeug.contrib.atom import AtomFeed
from config import POSTS_PER_PAGE
from flask.ext.paginate import Pagination
from flaskext.markdown import Markdown
import markdown
from app import db
from app.models.models import *
from app.models.forms import CommentForm
main = Blueprint('main', __name__, url_prefix='/')

@main.route('')
def index():
	page = int(request.args.get('page')) if request.args.get('page') else 1
	categories = Category.query.filter_by(status='1').order_by('title').all()
	try:
		posts = Post.query.filter_by(status='1').order_by("-id").paginate(page=page, per_page=POSTS_PER_PAGE)
	except:
		return redirect(url_for('main.index', page=1))

	dates = db.session.query(Post, "created_month").group_by("created_month").all()
	return render_template("blog/index.html", categories=categories, posts=posts, dates=dates, page=page)

@main.route('blog/category/<id>/')
def category(id):
	page = int(request.args.get('page')) if request.args.get('page') else 1
	categories = Category.query.filter_by(status='1').order_by('title').all()
	try:
		posts = Post.query.filter_by(status='1').order_by("-id").filter_by(category_id=id).paginate(page=page, per_page=POSTS_PER_PAGE)
	except:
		return redirect(url_for('main.index', page=1))
	dates = db.session.query(Post, "created_month").group_by("created_month").all()
	return render_template("blog/index.html", categories=categories, posts=posts, dates=dates, page=page)
	
@main.route('blog/archive/<month>/')
def archive(month):
	page = int(request.args.get('page')) if request.args.get('page') else 1
	categories = Category.query.filter_by(status='1').order_by('title').all()
	try:
		posts = Post.query.filter_by(status='1').order_by("-id").filter_by(created_month=month).paginate(page=page, per_page=POSTS_PER_PAGE)
	except:
		return redirect(url_for('main.index', page=1))
	dates = db.session.query(Post, "created_month").group_by("created_month").all()
	return render_template("blog/index.html", categories=categories, posts=posts, dates=dates, page=page)
	
@main.route('blog/<id>/', methods=['GET', 'POST'])
def detail(id):
	try:
		id = int(id)
		post = Post.query.get(id)
	except ValueError:
		print "nonononono"
		post = Post.query.filter_by(perma_link=id).one()
	
	form = CommentForm(request.form)
	if request.method == "POST" and form.validate():
		comment = Comment(form.user_name.data, form.message.data, post.id)
		db.session.add(comment)
		db.session.commit()
		flash(u'感谢您的留言！')
		return redirect(url_for('main.detail', id=id))

	comments = Comment.query.filter_by(post_id=post.id).order_by("-id").all()
	#update view count
	post.view_count = post.view_count + 1
	db.session.commit()
	
	ip = request.remote_addr
	viewlogModel = Viewlog(ip, post.id)
	db.session.add(viewlogModel)
	db.session.commit()
	
	return render_template("blog/detail.html", post=post, form=form, comments=comments)

@main.route('album/')
@main.route('album/<id>/')
def albumIndex(id=0):
	albums = Album.query.order_by("-id").all()
	if id == 0:
		id = albums[0].id
	photos = Photo.query.filter_by(album_id=id).order_by("-id")
	return render_template("album/index.html", albums=albums, photos=photos)
	
@main.route('aboutme/')
def aboutmeIndex():
	return render_template("aboutme/index.html")

@main.route('rss/')
def rssIndex():
	feed = AtomFeed(u'树妖攻城狮的IT实验室', feed_url=request.url, url=request.url_root)
	posts = Post.query.order_by("-id").limit(15).all()
	for post in posts:
		feed.add(post.title, Markup(markdown.markdown(post.content)),
				content_type='html',
				author='Jacky',
				url=url_for('main.detail', id=post.id),
				updated=post.updated_at,
				published=post.created_at)
	return feed.get_response()
	
	
	
	
	
	
	