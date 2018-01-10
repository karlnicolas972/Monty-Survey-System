# only to be used once, since after the initial execution everything is in the database

from survey import *
from course import *
from question import *
from user import *
from server import *
from answer import *
import csv

def courses_upload():
	with open("csv_files/courses.csv", "r") as csv_in:
		reader = csv.reader(csv_in)
		for row in reader:
			name = row[0]
			sem = row[1]
			if not course_exists(name, sem):	
				c = new_course_offering(name, sem)
				add_to_db(c)

	commit_db()

if __name__ == "__main__":
	courses_upload()