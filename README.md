# Monty Survey System

This is a survey system developed to gauge effectiveness and engagement within UNSW courses. 

This is also the Final Project for COMP1531, in which it achieved 96%.

To use the system, first log-in as a System Admin to create surveys for courses and add questions to those surveys. Then a staff user account can review and approve created surveys before they are released to students to fill out. Student user accounts can then answer both open ended and multiple choice questions within those surveys. A chart detailing current responses to the questions in a survey is available for the System Admin to view at any time. Once the System Admin closes the survey, the a chart detailing the results of the survey becomes available to all staff and students are involved in the survey.

**External Python libraries used**

`flask`, `flask_login`, `flask_sqlalchemy`, `werkzeug.security`, `csv`

**Running the project**

To run the project from scratch (if there is no app.db database), run: `./setup.sh`

This will run 

`python3 db_create.py`

`python3 user_upload.py`

`python3 courses_upload.py`

`python3 run.py`

WARNING: This process can take ~3 minutes, depending on your computer

If the database has been created, run: `python3 run.py`

**Example Users**

System Admin: 

    UserID   : `0`
    Password : `admin_password`

Course: `SENG2011 18s1`

Course Staff:
 
    zID      : `1086`
    Password : `staff1086`

Course Students:
 
    zID      : `127`
    Password : `student237`
    zID      : `130`
    Password : `student886`
    zID      : `134`
    Password : `student434`
    zID      : `538`
    Pass     : `student639`

Other course, staff and student information can be found the in the file: `all_users.txt`

**Homepage** 

Once the server is active, the URL of the home page is `http://127.0.0.1:2001`

**Tests**

To run the tests:

`python3 tests.py`

*All tests contained in tests.zip:*

class TestLogin(unittest.TestCase):

	def test_invalid_login(self):
	def test_student_login(self):
	def test_admin_login(self):
	def test_staff_login(self):
	
class TestSurveys(unittest.TestCase):

	def test_create_survey(self):
	def test_create_invalid_survey(self):
	def test_add_question_to_survey(self):
	def test_answer_question(self):
	def test_delete_survey(self):
	
class TestQuestions(unittest.TestCase):

	def test_create_invalid_question(self):
	def test_create_optional__MC_question(self):
	def test_create_mandatory__MC_question(self):
	def test_create_optional_open_question(self):
	def test_create_mandatory_open_question(self):
	def test_delete_question(self):
	
class TestUsers(unittest.TestCase):

	def test_create_invalid_user(self):
	def test_create_student_user(self):
	def test_create_staff_user(self):
	def test_create_admin_user(self):
	def test_student_enrol(self):
	def test_staff_for_course(self):
	def test_invalid_student_enrol(self):
	def test_invalid_staff_for_course(self):
	def test_nonstaff_nonstudent_for_courses(self):
	
class TestCourseOffering(unittest.TestCase):

	def test_create_invalid_course_offering(self):
	def test_create_course_offering(self):
	def test_course_enrolment_data(self):
