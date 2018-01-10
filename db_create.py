from server import *
from course import *
from survey import *
from question import *
from user import *
from answer import *

def create_db():
	db.create_all()

if __name__ == "__main__":
	create_db()