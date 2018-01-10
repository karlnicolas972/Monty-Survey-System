from server import db, course_user_table
from exceptions import InvalidParameterError

class CourseOffering(db.Model):

	__tablename__ = "course_offering"
	course_id = db.Column(db.Integer, primary_key=True)
	course_name = db.Column(db.String(10), nullable=False)
	semester = db.Column(db.String(5), nullable=False)
	survey_id = db.Column(db.Integer, db.ForeignKey("survey.survey_id"), unique=True)
	users = db.relationship("User", secondary=course_user_table,
		lazy="subquery", backref=db.backref("course_offering", lazy=True))


	def get_course_id(self):
		return self.course_id

	def get_course_name_and_sem(self):
		return self.course_name + " " + self.semester

	def get_users(self):
		return self.users

def new_course_offering(name, semester):
	# check that the arguments are valid
	if type(name) != str or type(semester) != str:
		raise TypeError
	if len(name) != 8 or len(semester) != 4:
		raise InvalidParameterError
	for i in range(4):
		if not name[i].isupper() or not name[i+4].isdigit():
			raise InvalidParameterError
	if not semester[0].isdigit() or not semester[1].isdigit() or semester[2] != 's' or not semester[3].isdigit():
		raise InvalidParameterError

	# create object once proven that arguments are valid
	c = CourseOffering(course_name=name, semester=semester)
	return c

def course_exists(name, sem):
	return CourseOffering.query.filter_by(course_name=name, semester=sem).scalar() is not None

def get_course_offering(name, semester):
	c = CourseOffering.query.filter_by(course_name=name, semester=semester).first()
	return c

def get_all_courses():
	all_courses = CourseOffering.query.all()
	return all_courses