# only to be used once, since after the initial execution everything is in the database

from survey import *
from course import *
from question import *
from user import *
from server import *
from answer import *
import csv
import sys

def enrolments_upload():
	with open("csv_files/enrolments.csv", "r") as csv_in:
		reader = csv.reader(csv_in)

		counter = 0;
		for row in reader:

			#Let user know the progress of the upload
			counter = counter+1;
			sys.stdout.write(str(counter) + "/2534")
			sys.stdout.flush()
			restart_line()

			zid = row[0]
			course = row[1]
			sem = row[2]
			u = get_user(zid)
			c = get_course_offering(course, sem)
			if u.is_student() and not u.is_enrolled_in_course(c):
				u.enrol_in_course(c)
			elif u.is_staff() and not u.is_staff_for_course(c):
				u.be_staff_for_course(c)

	commit_db()

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

if __name__ == "__main__":
	enrolments_upload()