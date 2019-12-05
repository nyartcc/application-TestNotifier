from dotenv import load_dotenv
import requests
import datetime
import calendar
import json
import operator
import functools
import os
import mysql.connector
from tools import convertTuple
import tools

# Load the database variables from the .env file.
load_dotenv()
db_host = os.getenv('DATABASE_HOST')
db_user = os.getenv('DATABASE_USER')
db_pass = os.getenv('DATABASE_PASSWORD')
db_name = os.getenv('DATABASE_NAME')
webhook_url = os.getenv('SLACK_WEBHOOK_GENERAL')

# Establish a connection to the MySQL Database using the .env variables.
mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd=db_pass,
    database=db_name
)

# Get some date information that will be needed later.
today = datetime.datetime.today()

# Get info about last weeks hours.
query = "SELECT tc_results.*, controllers.fname, controllers.lname, tc_tests.testname, tc_tests.passingscore, tc_tests.maxscore FROM tc_results INNER JOIN controllers USING (cid) INNER JOIN tc_tests ON tc_results.testid = tc_tests.id WHERE checkedby < 2 AND start >0 AND end>0 AND certed=0 AND reassigned=0 AND assignedby>0 ORDER BY id DESC;"
run = mydb.cursor()
run.execute(query)
run_records = run.fetchall()

x = 0   # Debugging Purposes

for row in run_records:
    for i in row:
        # print("row[{}]: {}".format(x, i))  # Debugging Purposes
        x += 1  # Debugging Purposes

    cur_timestamp = datetime.datetime.now().timestamp()
    print(cur_timestamp)  # Debugging Purposes
    diff = cur_timestamp - row[5]
    if diff > 43200:
        # print("Let's go boys!")  # Debugging Purposes
        # pass
        tools.slackPendingExam('training-staff', row[0], row[19],
                               row[3], row[20], row[21], row[5], row[17], row[18])

    # print("\n")  # Debugging Purposes

    x = 0   # Debuting Purposes
