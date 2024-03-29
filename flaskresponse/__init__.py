from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flaskresponse.config import Config


db = SQLAlchemy() 
bcrypt = Bcrypt() 
login_manager = LoginManager() 
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info' 



def create_app(config_class = Config):
	app = Flask(__name__) 
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	from flaskresponse.users.routes import users
	from flaskresponse.main.routes import main
	from flaskresponse.filter.routes import filter_blueprint
	app.register_blueprint(users)
	app.register_blueprint(filter_blueprint)
	app.register_blueprint(main)

	app.jinja_env.globals.update(zip=zip)
	return app

