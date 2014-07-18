# Import flask and libs
from flask import Flask, render_template
from flaskext.markdown import Markdown
# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('config')
# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
# HTTP 404
# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
# Import modules by blueprint
# Import a module / component using its blueprint handler variable (mod_auth)
from app.main.controllers import main as main_module
from app.admin.controllers import admin as admin_module
# Register blueprint(s)
app.register_blueprint(admin_module)
app.register_blueprint(main_module)
# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()
Markdown(app)