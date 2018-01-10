# This is the "controller"
# It's like a dictionary or hash, there is a list of urls mapping to functions

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from survey import *
from server import *
from question import *
from course import *
from user import *
from answer import *
import csv

from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from auth_manager import auth

#----Login----

@login_manager.user_loader
def load_user(user_id):
	user = auth.get_user(user_id)
	return user


@app.route('/', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user_id = request.form["user_name"]
		password = request.form["password"]

		if auth.check_password(user_id, password):
			auth.user = user_id
			user = load_user(user_id)
			login_user(user)
			return redirect(url_for('index'))
		else:
			flash("Your login details are incorrect. Please try again.")

	return render_template("basic_login.html")


@app.route('/index')
@login_required
def index():
	user = load_user(auth.user)
	surveys = get_surveys_for_user(user)
	closed_surveys = get_closed_surveys_for_user(user)
	return render_template("index.html", title="Home", user=user, 
		surveys=surveys, closed_surveys=closed_surveys)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

#----Login^----

@app.route("/add_question", methods=["POST", "GET"])
@login_required
def add_question():
	user = load_user(auth.user)
	if not user.is_admin():
		return render_template("no_permission.html", user=user)

	if request.method == "POST":
		st = request.form["question"]

		if st == "":
			flash("You haven't entered a question!")
			return redirect(url_for("add_question"))

		question_type = request.form["question_type"]
		response_type = request.form["response_type"]

		answers = None

		if response_type == "multiple_choice":
			answers = []
			for i in range(1, 5):
				ans = "ans_%d" % i
				a = request.form[ans]
				if a != "":
					answers.append(a)
				else:
					flash("You haven't added all the possible answers for a multiple choice question!")
					return redirect(url_for("add_question"))

		q = new_question(st, question_type, response_type, answers)

		if q == None and response_type == "multiple_choice":
			flash("You haven't written any answers for a multiple choice question!")
			return redirect(url_for("add_question"))

		add_to_db(q)
		commit_db()

		flash("Question successfully added!")

	return render_template("add_question.html", 
		title="Add a Question", user=user)

@app.route("/view_surveys", methods=["POST", "GET"])
@login_required
def view_surveys():
	survey_list = get_all_surveys()
	user = load_user(auth.user)
	if not user.is_admin():
		return render_template("no_permission.html", user=user)
	return render_template("view_surveys.html", 
		title="View Surveys", survey_list=survey_list, user=user)


#CHARTS LIST
@app.route("/view_charts", methods=["POST", "GET"])
@login_required
def view_charts():
	survey_list = get_all_surveys()
	user = load_user(auth.user)
	if not user.is_admin():
		return render_template("no_permission.html", user=user)
	return render_template("charts.html", 
		title="View survey charts", survey_list=survey_list, user=user)


@app.route('/close', methods=['POST'])
def close_entry():
	id_num = request.form['entry_id']
	s = get_survey(id_num)
	s.update_status("closed")
	commit_db()
	return redirect(url_for("view_surveys"))

#CHART FOR SINGLE SURVEY
@app.route("/survey_chart/<int:id_num>", methods=["POST", "GET"])
@login_required
def survey_chart(id_num):
	survey_list = get_all_surveys()
	s = get_survey(id_num)
	if s == None:
		flash("This survey doesn't exist!")
		return redirect(url_for("index"))

	user = load_user(auth.user)

	mc_question_list = get_all_mc_questions()
	for q in mc_question_list:
		if not s.questions.__contains__(q): ### should change s.questions
			mc_question_list.remove(q)

	#dictionary of dictionaries
	all_answers_dict = {}
	for q in mc_question_list:

		#stores options for mc_question and # of responses as key:value pairs
		answers_dict = {}
		#initialise dictionary
		answers_dict[q.answer_1] = 0
		answers_dict[q.answer_2] = 0
		answers_dict[q.answer_3] = 0
		answers_dict[q.answer_4] = 0

		#iterate through answer objects and add them to value
		for a in q.answers:
			if a.survey_id == s.survey_id:
				answers_dict[a.answer] = answers_dict[a.answer]+1
		for k in answers_dict.keys():
			print(k + ":" + str(answers_dict[k]))
		print("----")
		all_answers_dict[q.question_id] = answers_dict

	open_question_list = []
	survey_question_ids = []
	for q in s.questions:
		survey_question_ids.append(q.question_id)
		if q.response_type == "open_ended":
			open_question_list.append(q)

	course = s.get_course_str()
	return render_template("survey_chart.html", title=("Results of survey for %s" % course), 
		mc_question_list=mc_question_list, open_question_list=open_question_list, 
		survey_list=survey_list, user=user, all_answers_dict=all_answers_dict, survey_id=s.survey_id)


@app.route("/survey/<int:id_num>", methods=["POST", "GET"])
@login_required
def survey(id_num):
	s = get_survey(id_num)
	if s == None:
		flash("This survey doesn't exist!")
		return redirect(url_for("index"))

	user = load_user(auth.user)

	course = s.get_course_str()

	if not user.is_admin():
		if s.users.__contains__(user):
			flash("You have already filled out this survey!")
			return redirect(url_for("index"))

		if not user.courses.__contains__(s.course_offering):
			flash("You are not taking this course!")
			return redirect(url_for("index"))

	# here the strategy is to get all the multiple choice questions
	# and then remove it if it isn't in the survey's own list of questions
	# this is because for some reason inheritance doesn't hold
	# when retrieving from s.questions so you have to directly
	# query from the multiple choice question so that the results
	# are of type "MultipleChoiceQuestion" instead of "Question"
	mc_question_list = get_all_mc_questions()
	for q in mc_question_list:
		if not s.questions.__contains__(q):
			mc_question_list.remove(q)

	open_question_list = []
	survey_question_ids = []
	for q in s.questions:
		survey_question_ids.append(q.question_id)
		if q.response_type == "open_ended":
			open_question_list.append(q)

	if request.method == "POST":
		
		answered_questions = request.form["answered_questions"]
		answered_questions_list = [int(x) for x in answered_questions.split()]

		answered_questions_list = list(set(answered_questions_list))
		answered_questions_list.sort()

		for q in s.questions:

			if not answered_questions_list.__contains__(q.question_id):
				if q.question_type == "optional":
					continue
				else:
					flash("You haven't answered a mandatory question!")
					return redirect(url_for("survey", id_num=id_num))

			answer_index = "answer_%d" % q.question_id
			print("submitting answer_%d" % q.question_id) ###
			answer = request.form[answer_index]
			a = new_answer(answer, q.question_id, s.survey_id)
			s.add_answer(a)
			add_to_db(a)

		if not user.is_admin():
			user.add_to_answered_surveys(s)

		commit_db()

		flash("Survey successfully submitted!")

		return redirect(url_for("index"))

	return render_template("survey.html", title=("Survey for %s" % course), 
		survey=s, open_question_list=open_question_list, 
		mc_question_list=mc_question_list, user=user)

@app.route("/review_survey/<int:id_num>", methods=["POST", "GET"])
@login_required
def review_survey(id_num):
	s = get_survey(id_num)
	if s == None:
		flash("This survey doesn't exist!")
		return redirect(url_for("index"))

	user = load_user(auth.user)

	if user.is_student():
		return render_template("no_permission.html", user=user)

	course = s.get_course_str()

	# separate the optional questions depending if they're in the survey or not
	all_mc_question_list = get_all_mc_questions()
	all_open_question_list = get_all_open_questions()

	survey_mc_question_list = []
	survey_open_question_list = []

	remaining_mc_question_list = []
	remaining_open_question_list = []

	for q in all_mc_question_list:
		if s.questions.__contains__(q):
			survey_mc_question_list.append(q)
		elif q.question_type == "optional":
			remaining_mc_question_list.append(q)

	for q in all_open_question_list:
		if s.questions.__contains__(q):
			survey_open_question_list.append(q)
		elif q.question_type == "optional":
			remaining_open_question_list.append(q)

	if request.method == "POST":

		# parsing a string that determines which checkboxes were ticked by the user
		selected_questions = request.form["selected_questions"]

		# remove duplicates in the selected_questions string
		num_questions = get_num_all_questions()
		for i in range(num_questions):
			tmp = " %d " % (i + 1)
			if selected_questions.__contains__(tmp):
				if selected_questions.count(tmp) % 2 == 0:
					selected_questions = selected_questions.replace(tmp, "")
				else:
					selected_questions = selected_questions.replace(tmp, "")
					selected_questions += tmp

		selected_questions_list = [int(x) for x in selected_questions.split()]

		selected_questions_list.sort()

		# after we have the list of question numbers selected by the user
		# we add them to the survey object
		for i in selected_questions_list:
			q = get_question(i)
			s.add_question(q)

		s.update_status("to_be_answered")

		commit_db()

		flash("Survey for %s is now approved!" % course)
		return redirect(url_for("index"))

	return render_template("review_survey.html", 
		title=("Reviewing survey for %s" % course), 
		survey_mc_question_list=survey_mc_question_list, 
		survey_open_question_list=survey_open_question_list, 
		remaining_mc_question_list=remaining_mc_question_list,
		remaining_open_question_list=remaining_open_question_list,
		user=user)

@app.route("/view_questions", methods=["POST", "GET"])
@login_required
def view_questions():
	user = load_user(auth.user)
	if not user.is_admin():
		return render_template("no_permission.html", user=user)

	if request.method == "POST":
		course_str = request.form["course"]
		course_details = course_str.split()

		if len(course_details) == 0:
			flash("You haven't selected a course!")
			return redirect(url_for("view_questions"))

		course_name = course_details[0]
		course_sem = course_details[1]
		course = get_course_offering(course_name, course_sem)
		
		if survey_exists_for_course(course):
			flash("There is already a survey for %s!" % course_str)
			return redirect(url_for("view_questions"))

		s = new_survey(course)

		# parsing a string that determines which checkboxes were ticked by the user
		selected_questions = request.form["selected_questions"]

		# remove duplicates in the selected_questions string
		num_questions = get_num_all_questions()
		for i in range(num_questions):
			tmp = " %d " % (i + 1)
			if selected_questions.__contains__(tmp):
				if selected_questions.count(tmp) % 2 == 0:
					selected_questions = selected_questions.replace(tmp, "")
				else:
					selected_questions = selected_questions.replace(tmp, "")
					selected_questions += tmp

		selected_questions_list = [int(x) for x in selected_questions.split()]

		# if the user hasn't selected any questions
		if not selected_questions_list:
			flash("You haven't selected any questions!")
			return redirect(url_for("view_questions"))

		selected_questions_list.sort()

		# after we have the list of question numbers selected by the user
		# we add them to the survey object
		for i in selected_questions_list:
			q = get_question(i)
			s.add_question(q)

		add_to_db(s)
		commit_db()

		flash("Survey successfully created")

	mc_question_list = get_all_mc_questions()
	open_question_list = get_all_open_questions()
	courses_list = get_all_courses()
	return render_template("view_questions.html", 
		title="View Questions", user=user, mc_question_list=mc_question_list,
		open_question_list=open_question_list, courses_list=courses_list)

# error pages
@app.errorhandler(401)
def page_not_found(e):
 	return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

