# only to be used once, since after the initial execution everything is in the database

import sys
from survey import *
from course import *
from question import *
from user import *
from server import *
from answer import *
from werkzeug.security import generate_password_hash, check_password_hash 
import csv

def user_upload():
	with open("csv_files/passwords.csv", "r") as csv_in:
		reader = csv.reader(csv_in)
		counter = 0
		for row in reader:

			#Let user know the progress of the upload
			counter = counter+1;
			sys.stdout.write(str(counter) + "/2534")
			sys.stdout.flush()
			restart_line()

			zid = int(row[0])
			password = row[1]
			user_type = row[2]
			hashed_password = generate_password_hash(password)
			if not user_exists(zid, hashed_password, user_type):
				u = new_user(zid, hashed_password, user_type)
				add_to_db(u)
		# create admin user
		hashed_admin_pass = generate_password_hash("admin_password")
		admin = new_user(0, hashed_admin_pass, "admin")
		add_to_db(admin)


	commit_db()

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

#user_upload()

if __name__ == "__main__":
	user_upload()



