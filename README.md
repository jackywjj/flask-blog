Flask blog & gallary
==========

My personal blog base on Python. Using Flask.

This version is already lunched on my blog. So please do not do anything evil. Many thanks.


### 2014-06-09 修改
-删除用户uwsgi的配置文件，改用gunicorn启动应用
-启动脚本如：
	/usr/local/bin/gunicorn -D -p _/path/to/pid/flaskblog.pid_ -u _user_ -g _group_ --access-logfile _/path/to/log/flaskblog-access.log_ --error-logfile _/path/to/log/flaskblog-error.log_ -w 2 run:app
-修复若干Bug，主要是view部分
-增加文章阅读次数功能