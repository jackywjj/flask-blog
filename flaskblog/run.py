from app import app
from flaskext.markdown import Markdown

if __name__ == '__main__':
	Markdown(app)
	app.debug = True
	app.run()