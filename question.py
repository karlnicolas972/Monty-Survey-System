from server import db, survey_question_table
from exceptions import InvalidParameterError

class Question(db.Model):

	__tablename__ = "question"
	__table_args__ = { 'extend_existing': True } 
	question_id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String(100), nullable=False)
	question_type = db.Column(db.String(20), nullable=False)
	response_type = db.Column(db.String(20), nullable=False)
	answers = db.relationship("Answer", lazy=True, 
		backref=db.backref("question", lazy=True))
	discriminator = db.Column(db.String(50))

	__mapper_args__ = {
		"polymorphic_identity":"questions",
		"polymorphic_on":discriminator
	}

	def get_question_id(self):
		return self.question_id

	def get_question(self):
		return self.question

	def get_answers(self):
		return self.answers

	def get_question_type(self):
		return self.question_type

	def is_mandatory(self):
		return self.question_type == "mandatory"

	def is_optional(self):
		return self.question_type == "optional"

	def is_multiple_choice(self):
		return self.response_type == "multiple_choice"

	def is_open_ended(self):
		return self.response_type == "open_ended"


class MultipleChoiceQuestion(Question):

	__tablename__ = "mc_question"
	mc_question_id = db.Column(db.Integer, 
		db.ForeignKey("question.question_id"), primary_key=True)

	__mapper_args__ = { "polymorphic_identity":"mc_questions" }

	answer_1 = db.Column(db.String(100))
	answer_2 = db.Column(db.String(100))
	answer_3 = db.Column(db.String(100))
	answer_4 = db.Column(db.String(100))

	def get_answer_1(self):
		return self.answer_1

	def get_answer_2(self):
		return self.answer_2
		
	def get_answer_3(self):
		return self.answer_3

	def get_answer_4(self):
		return self.answer_4	


def new_question(question, question_type, response_type, answers):
	if type(question) != str:
		raise TypeError

	if question_type != "optional" and question_type != "mandatory":
		raise InvalidParameterError

	if response_type == "multiple_choice":
		q = MultipleChoiceQuestion(question=question, 
			question_type=question_type, response_type=response_type)
			
		# if it is a multiple choice question with no answers, return None
		# None will be flag for the controller that there is an error
		# controller will then redirect back to the add questions page
		some_list = []
		if answers != None and type(answers) == type(some_list):
			q.answer_1 = answers[0]
			q.answer_2 = answers[1]
			q.answer_3 = answers[2]
			q.answer_4 = answers[3]
		else:
			return None
	elif response_type == "open_ended":
		q = Question(question=question, 
			question_type=question_type, response_type=response_type)
	else:
		raise InvalidParameterError
	return q


def get_question(question_id):
	q = Question.query.get(question_id)
	return q

def get_all_mc_questions():
	all_mc_questions = MultipleChoiceQuestion.query.all()
	return all_mc_questions

def get_all_open_questions():
	all_open_questions = Question.query.filter_by(response_type="open_ended").all()
	return all_open_questions

def get_num_all_questions():
	n = Question.query.count()
	return n