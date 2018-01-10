from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# table is for the "many to many" relationship between course and user
course_user_table = db.Table("course_user_table",
	db.Column("user_id", db.Integer, db.ForeignKey("user.user_id"), primary_key=True),
	db.Column("course_id", db.Integer, db.ForeignKey("course_offering.course_id"), primary_key=True)
)

# table is for the "many to many" relationship between survey and question
survey_question_table = db.Table("survey_question_table", 
	db.Column("question_id", db.Integer, db.ForeignKey("question.question_id"), primary_key=True),
	db.Column("survey_id", db.Integer, db.ForeignKey("survey.survey_id"), primary_key=True)
)


survey_user_table = db.Table("survey_user_table",
	db.Column("survey_id", db.Integer, db.ForeignKey("survey.survey_id"), primary_key=True),
	db.Column("user_id", db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
)

def add_to_db(item):
	db.session.add(item)

def commit_db():
	db.session.commit()

def remove_from_db(item):
	db.session.delete(item) 
