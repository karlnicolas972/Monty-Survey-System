from server import db, survey_question_table, survey_user_table
from course import CourseOffering
from exceptions import InvalidParameterError

class Survey(db.Model):

	__tablename__ = "survey"
	survey_id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.String(32), nullable=False) # this can either be "to_be_reviewed" or "to_be_answered"
	course_offering = db.relationship("CourseOffering", uselist=False, lazy=True)
	answers = db.relationship("Answer", lazy=True, 
		backref=db.backref("survey", lazy=True))
	questions = db.relationship("Question", 
		secondary=survey_question_table,
		lazy=True, 
		backref=db.backref("survey", lazy=True))


	def get_survey_id(self):
		return self.survey_id

	def get_status(self):
		return self.status

	def update_status(self, status):
		if status != "to_be_reviewed" and status != "to_be_answered" and status != "closed":
			raise InvalidParameterError
		self.status = status

	def add_question(self, question):
		self.questions.append(question)

	def add_answer(self, answer):
		self.answers.append(answer)

	def get_all_questions(self):
		return self.questions

	def get_all_answers(self):
		return self.answers

	def get_course_str(self):
		return self.course_offering.course_name + " " + self.course_offering.semester


# linear search might be slow sometimes
def get_closed_surveys_for_user(user):
	closed_surveys = Survey.query.filter_by(status="closed").all()
	users_surveys = []
	if user.is_student():
		for s in closed_surveys:
			if user.has_answered_survey(s):
				users_surveys.append(s)
	elif user.is_staff():
		for s in closed_surveys:
			if user.is_staff_for_course(s.course_offering):
				users_surveys.append(s)

	return users_surveys

def survey_exists_for_course(course):
	# make sure there is only one survey for each course
	# there is probably a better way of doing this using the database
	current_courses = []
	for temp_survey in Survey.query.all():
		if not current_courses.__contains__(temp_survey.course_offering):
			current_courses.append(temp_survey.course_offering)

	if current_courses.__contains__(course):
		return True
	else:
		return False

def get_survey(id_num):
	s = Survey.query.get(id_num)
	return s

def new_survey(course):
	if type(course) != CourseOffering:
		raise TypeError
	s = Survey(course_offering=course, status="to_be_reviewed")
	return s

def get_surveys_for_user(user):
	surveys = []
	if user.user_type == "staff":
		for c in user.courses:
			s = Survey.query.filter_by(course_offering=c, status="to_be_reviewed").scalar()
			if s != None:
				surveys.append(s)
	elif user.user_type == "student":
		for c in user.courses:
			s = Survey.query.filter_by(course_offering=c, status="to_be_answered").scalar()
			if s != None and not user.surveys.__contains__(s):
				surveys.append(s)
	else:
		surveys = None

	return surveys

def get_all_surveys():
	all_surveys = Survey.query.all()
	return all_surveys