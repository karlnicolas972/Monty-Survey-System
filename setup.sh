#!/bin/sh

if [ -e app.db ]
then
    echo "Database already exists!"
    echo "Please run the app with python3 run.py"
else
	echo "Creating Database"
    python3 db_create.py

    echo "Uploading courses"
	python3 courses_upload.py

    echo "Uploading users"
	python3 user_upload.py

	echo "Uploading enrolments"
	python3 enrolments_upload.py

	echo "Running app. Welcome to Monty Survey System!"
	python3 run.py
fi