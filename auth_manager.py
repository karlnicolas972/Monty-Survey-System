
#auth things
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from user import User
from server import app,login_manager

class AuthManager():

	def __init__(self):
		self._user = ""

	def check_password(self, user_id, password):
		user = self.get_user(user_id)
		if user == None:
			return False
		if check_password_hash(user.password, password):
			return True
		return False

	def get_user(self, user_id):
		user = User.query.filter_by(user_id=user_id).first()
		return user

	@property
	def user(self):
		return self._user

	@user.setter
	def user(self, usr):
		self._user = usr

auth = AuthManager()




