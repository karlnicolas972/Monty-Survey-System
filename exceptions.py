
class Error(Exception):
	pass

class InvalidParameterError(Error):
	'''
	Raised when parameters defined as strings 
	(for example, Question.question_type or User.user_type)
	is given a theoretically invalid argument but an
	otherwise functionally valid argument.

	For example, when User.user_type is assigned a value of "pen", 
	which is neither "student", "staff" nor "admin".
	'''
	pass