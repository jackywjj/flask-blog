from app import app
from flaskext.markdown import Markdown
from werkzeug.contrib.fixers import ProxyFix

if __name__ == '__main__':
	Markdown(app)
	app.wsgi_app = ProxyFix(app.wsgi_app)
	app.debug = True
	app.run()