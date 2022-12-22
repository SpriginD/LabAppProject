import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = False
	TESTING = False

	SECRET_KEY = os.getenv('SECRET_KEY')

	DATABASE = os.path.join(basedir, 'googlesheetsdatas.db')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'feedbackData.db')

	UPLOAD_FOLDER = os.path.join(basedir, 'app/static/images/feedbacks')
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
	MAX_CONTENT_LENGTH = 1024 * 1024 * 4 	# 4MB

	SEND_FILE_MAX_AGE_DEFAULT = 0

	SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	DEBUG = True

	SESSION_COOKIE_SECURE = False
