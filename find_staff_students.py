# only to be used once, since after the initial execution everything is in the database

import sys
from survey import *
from course import *
from question import *
from user import *
from server import *
from answer import *
import csv

def main():
	for course in get_all_courses():
		print(course.get_course_name_and_sem())
		print("Staff: ")
		for user in User.query.all():
			if user.is_staff_for_course(course):
				print("    zID:  " + str(user.user_id))
				password = find_password(user.user_id)
				print("    Pass: " + password)
		print("Student: ")
		for user in User.query.all():
			if user.is_enrolled_in_course(course):
				print("    zID:  " + str(user.user_id))
				password = find_password(user.user_id)
				print("    Pass: " + password)

		print("=========================")


def find_password(user_id):
	with open("csv_files/passwords.csv", "r") as csv_in:
		reader = csv.reader(csv_in)
		for row in reader:
			zid = int(row[0])
			if user_id == zid:
				return row[1]
			

if __name__ == "__main__":
	main()



