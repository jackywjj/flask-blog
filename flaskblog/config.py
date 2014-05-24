# Debug enviroment
DEBUG = False
# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
# Define the database
#SQLALCHEMY_DATABASE_URI = 'mysql://name:password@127.0.0.1/dbname'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "mkoiujnbhyt"

# Secret key for signing cookies
SECRET_KEY = "0912ikxmjs7283746"

POSTS_PER_PAGE = 12

#UPLOAD_PATH_BLOG = BASE_DIR + "\\app\\static\\uploads\\b\\"
#UPLOAD_PATH_ALBUM = BASE_DIR + "\\app\\static\\uploads\\a\\"
UPLOAD_PATH_BLOG = "/workdisk/www/flaskblog/app/static/uploads/b/"
UPLOAD_PATH_ALBUM = "/workdisk/www/flaskblog/app/static/uploads/a/"
UPLOAD_URL_BLOG = "/static/uploads/b/"
UPLOAD_URL_ALBUM = "/static/uploads/a/"