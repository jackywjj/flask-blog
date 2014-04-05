# Import flask and libs
from flask import Flask, render_template
from flaskext.markdown import Markdown
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
# Configurations
app.config.from_object('config')
db = SQLAlchemy(app)
# HTTP 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
# Import modules by blueprint
from app.main.controllers import main as main_module
from app.admin.controllers import admin as admin_module
# Register blueprint
app.register_blueprint(admin_module)
app.register_blueprint(main_module)
Markdown(app)