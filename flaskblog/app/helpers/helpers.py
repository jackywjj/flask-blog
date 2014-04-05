# coding=utf8
import time, os
from werkzeug.utils import secure_filename
from PIL import Image

from config import UPLOAD_PATH_BLOG, UPLOAD_PATH_ALBUM, UPLOAD_URL_BLOG, UPLOAD_URL_ALBUM

########################################################################################################################
def renderPostImageFileName(ext):
	name = str(int(time.time())) + "." + ext
	return name

def renderPostImageDir(id):
	dir = UPLOAD_PATH_BLOG + str(id)[-1] + "/"
	if os.path.isdir(dir):
		pass
	else:
		os.mkdir(dir)
	return dir
def renderPostImageUrl(id):
	dir = UPLOAD_URL_BLOG + str(id)[-1] + "/"
	return dir
	
def resizePostImage(file, id):
	filename = secure_filename(file.filename)
	extension = filename.rsplit('.', 1)[1].lower()
	new_filename = renderPostImageFileName(extension)
	new_filepath = renderPostImageDir(id)
	file.save(os.path.join(new_filepath, new_filename))
	im = Image.open(new_filepath + new_filename)
	im.thumbnail((320, 240), Image.ANTIALIAS)
	im.save(new_filepath + new_filename)
	return new_filename

########################################################################################################################	
def renderPhotoImageDir(id):
	dir = UPLOAD_PATH_ALBUM + str(id)[-1] + "/"
	if os.path.isdir(dir):
		pass
	else:
		os.mkdir(dir)
	return dir
	
def renderPhotoImageUrl(id):
	dir = UPLOAD_URL_ALBUM + str(id)[-1] + "/"
	return dir
	
def resizePhotoImage(file, id):
	filename = secure_filename(file.filename)
	extension = filename.rsplit('.', 1)[1].lower()
	new_filepath = renderPhotoImageDir(id)
	name = str(int(time.time()))
	filename_o = name + '-o' + '.' + extension
	file.save(os.path.join(new_filepath, filename_o))
	params = renderPhotoImageParams(name, extension)
	for key in params.keys():
		values = params[key]
		im = Image.open(new_filepath + filename_o)
		im.thumbnail(( values['width'],  values['height']), Image.ANTIALIAS)
		im.save(new_filepath + values['filename'])
	file_infor = {'filename' : name, 'fileext' : '.' + extension}
	return file_infor

def renderPhotoImageParams(name, ext):
	dic = {
			't' : {'filename' : name + '-t'+ "." + ext, 'width' : 120, 'height': 90 },
			'm' : {'filename' : name + '-m'+ "." + ext, 'width' : 400, 'height': 300 },
			'l' : {'filename' : name + '-l'+ "." + ext, 'width' : 800, 'height': 600 },
			'xl' : {'filename' : name + '-xl'+ "." + ext, 'width' : 1000, 'height': 750 }
			}
	return dic
	
def debugPrint(msg):
	print "\n##########################################################################################################"
	print msg
	print "\n##########################################################################################################"