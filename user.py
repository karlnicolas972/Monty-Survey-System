from server import db, course_user_table, survey_user_table
from flask_login import UserMixin
from exceptions import InvalidParameterError
from course import CourseOffering

class User(db.Model, UserMixin):

	__tablename__ = "user"
	user_id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(512), nullable=False)
	user_type = db.Column(db.String(20), nullable=False)
	courses = db.relationship("CourseOffering", secondary=course_user_table,
		lazy="subquery", backref=db.backref("user", lazy=True))
	surveys = db.relationship("Survey", secondary=survey_user_table,
		lazy=True, backref=db.backref("users", lazy=True))

	'''
	The _remove methods are here to make 
	deleting easier for objects that are linked
	by an association table, i.e. where the 
	objects have a many-to-many relationship
	'''
	def _remove_courses(self):
		self.courses = []

	'''
	See documentation for _remove_courses
	'''
	def _remove_surveys(self):
		self.surveys = []

	def add_to_answered_surveys(self, survey):
		self.surveys.append(survey)

	def enrol_in_course(self, course):
		if type(course) != CourseOffering:
			raise TypeError
		if self.is_student():
			self.courses.append(course)

	def unenrol_in_course(self, course):
		if type(course) != CourseOffering:
			raise TypeError
		if self.is_student():
			self.courses.remove(course)

	def be_staff_for_course(self, course):
		if type(course) != CourseOffering:
			raise TypeError
		if self.is_staff():
			self.courses.append(course)

	def resign_as_staff_for_course(self, course):
		if type(course) != CourseOffering:
			raise TypeError
		if self.is_staff():
			self.courses.remove(course)

	def get_user_type(self):
		return self.user_type

	def is_admin(self):
		return self.user_type == "admin"

	def is_student(self):
		return self.user_type == "student"

	def is_staff(self):
		return self.user_type == "staff"

	def has_answered_survey(self, survey):
		if self.is_student():
			return self.surveys.__contains__(survey)
		else:
			return False

	def is_staff_for_course(self, course):
		if self.is_staff():
			return self.courses.__contains__(course)
		else:
			return False

	def is_enrolled_in_course(self, course):
		if self.is_student():
			return self.courses.__contains__(course)
		else:
			return False

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.user_id)

def new_user(id, password, user_type):
	if type(id) != int or type(password) != str or type(user_type) != str:
		raise TypeError
	if user_type != "student" and user_type != "staff" and user_type != "admin" and user_type != "guest":
		raise InvalidParameterError
	u = User(user_id=id, password=password, user_type=user_type)
	return u

def get_user(id):
	u = User.query.get(id)
	return u

def user_exists(zid, password, user_type):
	return User.query.filter_by(user_id=zid, password=password, user_type=user_type).scalar() is not None