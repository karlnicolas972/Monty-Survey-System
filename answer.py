from server import db
from exceptions import InvalidParameterError

class Answer(db.Model):

	__tablename__ = "answer"
	id = db.Column(db.Integer, primary_key=True)
	answer = db.Column(db.String(100), nullable=False)
	question_id = db.Column(db.Integer, db.ForeignKey("question.question_id"))
	survey_id = db.Column(db.Integer, db.ForeignKey("survey.survey_id"))

	def get_answer(self):
		return self.answer

	def get_survey_id(self):
		return self.survey_id

	def get_answer_id(self):
		return self.id

def new_answer(answer, question_id, survey_id):
	if type(answer) != str:
		raise TypeError
	if type(question_id) != int or type(survey_id) != int:
		raise TypeError
	a = Answer(answer=answer, question_id=question_id, survey_id=survey_id)
	return a