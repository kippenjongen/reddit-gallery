import os

from flask import Flask


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'reddit-gallery.sqlite'),
		USER_AGENT='linux:slideshow_web:v3.0.0 (by /u/IndependentAmount)',
		STANDARD_SORT='hot',
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import post
	app.register_blueprint(post.bp)

	from . import subreddit
	app.register_blueprint(subreddit.bp)

	from . import index
	app.register_blueprint(index.bp)
	app.add_url_rule('/', endpoint='index')

	from . import error
	app.register_error_handler(400, error.bad_request)
	app.register_error_handler(404, error.page_not_found)
	app.register_error_handler(418, error.teapot)
	app.register_error_handler(500, error.serverErr)

	return app


