# Debug or not
DEBUG = False
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
#SQLALCHEMY_DATABASE_URI = 'mysql://root:jacky@mysql9981@127.0.0.1/flaskblogdb'
#SQLALCHEMY_DATABASE_URI = 'mysql://root:admin123456@127.0.0.1/flaskblogdb'
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@host/dbname'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2
# Enable CSRF
CSRF_ENABLED     = True
# secure key
CSRF_SESSION_KEY = "abcdefg"
# Secret key for signing cookies
SECRET_KEY = "abcdefg123456"
# page size
POSTS_PER_PAGE = 12
# upload dir and url
UPLOAD_PATH_BLOG = BASE_DIR + "/app/static/uploads/b/"
UPLOAD_PATH_ALBUM = BASE_DIR + "/app/static/uploads/a/"
UPLOAD_URL_BLOG = "/static/uploads/b/"
UPLOAD_URL_ALBUM = "/static/uploads/a/"