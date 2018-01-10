from survey import *
from server import *
from question import *
from course import *
from user import *
from answer import *
import unittest
from auth_manager import *
from survey_system import *
from exceptions import *

# use this table for the self.assert...... stuff
# Method                        Checks that	
# assertEqual(a, b)             a == b	 
# assertNotEqual(a, b)          a != b	 
# assertTrue(x)                 bool(x) is True	 
# assertFalse(x)                bool(x) is False	 
# assertIs(a, b)                a is b	
# assertIsNot(a, b)             a is not b	
# assertIsNone(x)               x is None	
# assertIsNotNone(x)            x is not None	
# assertIn(a, b)                a in b	
# assertNotIn(a, b)             a not in b	
# assertIsInstance(a, b)        isinstance(a, b)	
# assertNotIsInstance(a, b)     not isinstance(a, b)	

class TestLogin(unittest.TestCase):
	'''
	Tests for user story ID Z12 - Authentication Module
	'''

	def test_invalid_login(self):
		user_id = "InvalidUSER"
		password = "password"
		result = auth.check_password(user_id, password)
		self.assertIs(result, False) 
		
	def test_student_login(self):
		user_id = "100"
		password = "student228"
		result = auth.check_password(user_id, password)
		self.assertIs(result, True)
		user = auth.get_user(user_id)
		self.assertTrue(user.is_student())

	
	def test_admin_login(self):
		user_id = "0"
		password = "admin_password"
		result = auth.check_password(user_id, password)
		self.assertIs(result, True)
		user = auth.get_user(user_id)
		self.assertTrue(user.is_admin())

	def test_staff_login(self):
		user_id = "50"
		password = "staff670"
		result = auth.check_password(user_id, password)
		self.assertIs(result, True)
		user = auth.get_user(user_id)
		self.assertTrue(user.is_staff())


class TestSurveys(unittest.TestCase):
	'''
	Tests for user story ID Z3 - Create Surveys
	'''

	def test_create_survey(self):
		course = new_course_offering("TEST0100", "18s1")
		add_to_db(course)
		self.assertTrue(course_exists("TEST0100", "18s1"))
		s = new_survey(course)
		add_to_db(s)
		commit_db()
		self.assertTrue(survey_exists_for_course(course))
		remove_from_db(s)
		remove_from_db(course)
		commit_db()

	def test_create_invalid_survey(self):
		self.assertRaises(TypeError, new_survey)
		self.assertRaises(TypeError, new_survey, 1)
		self.assertRaises(TypeError, new_survey, "hi")
		self.assertRaises(TypeError, new_survey, ["lol", 1, False])
		self.assertRaises(TypeError, new_survey, {'1': 4})
		self.assertRaises(TypeError, new_survey, True)

	def test_add_question_to_survey(self):
		q = new_question("How dead is Fred?", "mandatory", "open_ended", 5)
		add_to_db(q)
		course = new_course_offering("TEST9999", "18s1")
		add_to_db(course)
		commit_db()
		self.assertTrue(course_exists("TEST9999", "18s1"))
		s = new_survey(course)
		add_to_db(s)
		commit_db()
		self.assertTrue(survey_exists_for_course(course))
		s.add_question(q)
		commit_db()
		self.assertIn(q, s.get_all_questions())
		remove_from_db(s)
		remove_from_db(q)
		remove_from_db(course)
		commit_db()

	def test_answer_question(self):
		q = new_question("How many octopi in a pie?", "optional", "open_ended", None)
		add_to_db(q)
		course = new_course_offering("TEST0400", "18s1")
		s = new_survey(course)
		add_to_db(s)
		s.add_question(q)
		commit_db()
		a = new_answer("8", q.get_question_id(), s.get_survey_id())
		s.add_answer(a)
		add_to_db(a)
		commit_db()
		self.assertIn(a, s.get_all_answers())
		remove_from_db(q)
		remove_from_db(s)
		remove_from_db(a)
		remove_from_db(course)
		commit_db()

	def test_delete_survey(self):
		course = new_course_offering("TEST3001", "18s1")
		add_to_db(course)
		self.assertTrue(course_exists("TEST3001", "18s1"))
		s = new_survey(course)
		add_to_db(s)
		commit_db()
		remove_from_db(s)
		self.assertIsNot(s, get_all_surveys())
		remove_from_db(course)
		commit_db()

class TestQuestions(unittest.TestCase):
	'''
	Tests for user story ID Z2 - Create Questions
	'''

	def test_create_invalid_question(self):
		self.assertRaises(TypeError, new_question, 1)
		self.assertRaises(TypeError, new_question, 1, 2, 3)
		self.assertRaises(TypeError, new_question, 1, False, ["True"])
		self.assertRaises(InvalidParameterError, new_question, "This is the question", "wrong_param", "open_ended", None)
		self.assertRaises(InvalidParameterError, new_question, "This is the question", "optional", "wrong_param", None)
		self.assertRaises(InvalidParameterError, new_question, "This is the question", "wrong_param", "wrong_param", None)
		self.assertIs(new_question("This is the question", "optional", "multiple_choice", {"some", "set"}), None)

	def test_create_optional__MC_question(self):
		answers = ["answer 1", "answer 2", "answer 3", "answer 4"]
		q = new_question("How many chickens in a house?", "optional", "multiple_choice", answers)
		add_to_db(q)
		commit_db()
		g = get_question(q.get_question_id())
		self.assertEqual(q, g)
		self.assertEqual(q.get_question_type(), "optional")
		remove_from_db(q)
		commit_db()

	def test_create_mandatory__MC_question(self):
		answers = ["answer 1", "answer 2", "answer 3", "answer 4"]
		q = new_question("How many chickens in a house?", "mandatory", "multiple_choice", answers)
		add_to_db(q)
		commit_db()
		g = get_question(q.get_question_id())
		self.assertEqual(q, g)
		self.assertEqual(q.get_question_type(), "mandatory")
		remove_from_db(q)
		commit_db()

	def test_create_optional_open_question(self):
		q = new_question("How many chickens in a house?", "optional", "open_ended", None)
		add_to_db(q)
		commit_db()
		g = get_question(q.get_question_id())
		self.assertEqual(q, g)
		remove_from_db(q)

	def test_create_mandatory_open_question(self):
		q = new_question("How many chickens in a house?", "mandatory", "open_ended", None)
		add_to_db(q)
		commit_db()
		g = get_question(q.get_question_id())
		self.assertEqual(q, g)
		remove_from_db(q)

	def test_delete_question(self):
		q = new_question("Do you like cats?", "mandatory", "open_ended", None)
		add_to_db(q)
		commit_db()
		remove_from_db(q)
		self.assertNotIn(q, get_all_open_questions())


class TestUsers(unittest.TestCase):

	'''
	All the tests for the user class
	'''

	def test_create_invalid_user(self):
		self.assertRaises(TypeError, new_user, "hi", "some_password", "student")
		self.assertRaises(TypeError, new_user, 2000, 2001, "staff")
		self.assertRaises(TypeError, new_user, 2000, "some_password", [True, False])
		self.assertRaises(InvalidParameterError, new_user, 2000, "some_password", "cool_kid")
		self.assertRaises(TypeError, new_user)

	def test_create_student_user(self):
		u = new_user(2000, "some_password", "student")
		add_to_db(u)
		commit_db()
		self.assertTrue(user_exists(2000, "some_password", "student"))
		self.assertTrue(u.is_student())
		remove_from_db(u)
		commit_db()

	def test_create_staff_user(self):
		u = new_user(2000, "some_password", "staff")
		add_to_db(u)
		commit_db()
		self.assertTrue(user_exists(2000, "some_password", "staff"))
		self.assertTrue(u.is_staff())
		remove_from_db(u)
		commit_db()

	def test_create_admin_user(self):
		u = new_user(2000, "some_password", "admin")
		add_to_db(u)
		commit_db()
		self.assertTrue(user_exists(2000, "some_password", "admin"))
		self.assertTrue(u.is_admin())
		remove_from_db(u)
		commit_db()


	'''
	Tests for user (student) rolment into a course
	'''
	def test_student_enrol(self):
		u = new_user(1337, "super_secure", "student")
		c = new_course_offering("TEST0400", "18s1")
		add_to_db(u)
		add_to_db(c)
		commit_db()
		self.assertFalse(u.is_enrolled_in_course(c))
		u.enrol_in_course(c)
		commit_db()
		self.assertTrue(u.is_enrolled_in_course(c))
		u._remove_courses()
		commit_db()
		remove_from_db(c)
		remove_from_db(u)
		commit_db()

	def test_staff_for_course(self):
		u = new_user(1337, "super_secure", "staff")
		c = new_course_offering("TEST0400", "18s1")
		add_to_db(u)
		add_to_db(c)
		commit_db()
		self.assertFalse(u.is_staff_for_course(c))
		u.be_staff_for_course(c)
		commit_db()
		self.assertTrue(u.is_staff_for_course(c))
		u._remove_courses()
		commit_db()
		remove_from_db(c)
		remove_from_db(u)
		commit_db()

	def test_invalid_student_enrol(self):
		u = new_user(1337, "super_secure", "student")
		add_to_db(u)
		commit_db()
		self.assertRaises(TypeError, u.enrol_in_course, 1)
		self.assertRaises(TypeError, u.enrol_in_course, "Hi")
		self.assertRaises(TypeError, u.enrol_in_course, False)
		self.assertRaises(TypeError, u.enrol_in_course, ["some", "list"])
		self.assertRaises(TypeError, u.enrol_in_course)
		u._remove_courses()
		commit_db()
		remove_from_db(u)
		commit_db()

	def test_invalid_staff_for_course(self):
		u = new_user(1337, "super_secure", "staff")
		add_to_db(u)
		commit_db()
		self.assertRaises(TypeError, u.be_staff_for_course, 1)
		self.assertRaises(TypeError, u.be_staff_for_course, "Hi")
		self.assertRaises(TypeError, u.be_staff_for_course, False)
		self.assertRaises(TypeError, u.be_staff_for_course, ["some", "list"])
		self.assertRaises(TypeError, u.be_staff_for_course)
		u._remove_courses()
		commit_db()
		remove_from_db(u)
		commit_db()

	def test_nonstaff_nonstudent_for_courses(self):
		# for admin user
		u = new_user(1337, "super_secure", "admin")
		c = new_course_offering("TEST0400", "18s1")
		add_to_db(u)
		add_to_db(c)
		commit_db()
		self.assertFalse(u.is_enrolled_in_course(c))
		self.assertFalse(u.is_staff_for_course(c))
		u.enrol_in_course(c)
		commit_db()
		self.assertFalse(u.is_enrolled_in_course(c))
		u.be_staff_for_course(c)
		commit_db()
		self.assertFalse(u.is_staff_for_course(c))
		u._remove_courses()
		commit_db()
		remove_from_db(c)
		remove_from_db(u)
		commit_db()
		# for guest user
		v = new_user(1337, "super_secure", "guest")
		c = new_course_offering("TEST0991", "18s1")
		add_to_db(v)
		add_to_db(c)
		commit_db()
		self.assertFalse(v.is_enrolled_in_course(c))
		self.assertFalse(v.is_staff_for_course(c))
		v.enrol_in_course(c)
		commit_db()
		self.assertFalse(v.is_enrolled_in_course(c))
		v.be_staff_for_course(c)
		commit_db()
		self.assertFalse(v.is_staff_for_course(c))
		v._remove_courses()
		commit_db()
		remove_from_db(c)
		remove_from_db(v)
		commit_db()

class TestCourseOffering(unittest.TestCase):
	'''
	Tests for the user story z14 - Store course info
	'''
	def test_create_invalid_course_offering(self):
		self.assertRaises(TypeError, new_course_offering, 1, "18s2")
		self.assertRaises(TypeError, new_course_offering, True, "18s2")
		self.assertRaises(TypeError, new_course_offering, [1, 2, "some_stuff"], "18s2")
		self.assertRaises(TypeError, new_course_offering, "TEST1111", 18.2)
		self.assertRaises(TypeError, new_course_offering, "TEST1111", [18, 2])
		self.assertRaises(TypeError, new_course_offering, "TEST1111", {"18":"2"})
		self.assertRaises(TypeError, new_course_offering, "TEST1111", True)
		self.assertRaises(InvalidParameterError, new_course_offering, "test1111", "18s2")
		self.assertRaises(InvalidParameterError, new_course_offering, "TESTabcd", "18s2")
		self.assertRaises(InvalidParameterError, new_course_offering, "TEST1111", "1852")
		self.assertRaises(InvalidParameterError, new_course_offering, "TEST1111", "qbs2")

	def test_create_course_offering(self):
		c = new_course_offering("TEST1111", "18s2")
		add_to_db(c)
		commit_db()
		self.assertTrue(course_exists("TEST1111", "18s2"))
		self.assertEqual(c.get_course_name_and_sem(), "TEST1111 18s2")
		remove_from_db(c)
		commit_db()
		
	def test_course_enrolment_data(self):
		u = new_user(1337, "super_secure", "student")
		c = new_course_offering("TEST0400", "18s1")
		add_to_db(u)
		add_to_db(c)
		commit_db()
		self.assertNotIn(u, c.get_users())
		u.enrol_in_course(c)
		commit_db()
		self.assertIn(u, c.get_users())
		u._remove_courses()
		commit_db()
		remove_from_db(c)
		remove_from_db(u)
		commit_db()

if __name__ == '__main__':
	unittest.main()

