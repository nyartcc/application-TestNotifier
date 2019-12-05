import functools
import operator
import os
from dotenv import load_dotenv
import requests
import json
import datetime
from datetime import datetime

load_dotenv()
slack_general = os.getenv('SLACK_WEBHOOK_GENERAL')
slack_web_dev = os.getenv('SLACK_WEBHOOK_WEB_DEV')
slack_training_staff = os.getenv('SLACK_WEBHOOK_TRAINING_STAFF')
slack_senior_staff = os.getenv('SLACK_WEBHOOK_SENIOR_STAFF')


def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str


def slackPendingExam(channel, test_id, test_name, total_score, passing_score, max_score, end_time, fname, lname):

    formatted_time = datetime.utcfromtimestamp(
        end_time).strftime('%Y-%m-%d %H:%M:%S')

    if total_score >= passing_score:
        test_result = "PASS"
    else:
        test_result = "FAIL"

    message_data = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Warning! A test has been pending for more than 12 hours:\n_(Please note that the buttons below do not work yet. They might in the future.)_\n*<https://www.nyartcc.org/tc/admin/view/{} | {} {} - {}>*".format(test_id, fname, lname, test_name)
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Exam:*\n{}".format(test_name)
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Submitted:*\n{}".format(formatted_time)
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Total Score:*\n{}/{}".format(total_score, max_score)
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Result:*\n {}".format(test_result)
                    }

                ], "accessory": {
                    "type": "image",
                    "image_url": "https://image.prntscr.com/image/y9FuNIUOQBacBfIJgA0Sgg.png",
                    "alt_text": "Warning"
                }
            },

            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Pass Exam"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Fail Exam"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    }

    if channel == 'web-dev':
        print(slack_web_dev)
        webhook_url = slack_web_dev
        print(webhook_url)
    elif channel == 'training-staff':
        webhook_url = slack_training_staff
    elif channel == 'senior-staff':
        webhook_url = slack_senior_staff
    else:
        webhook_url = slack_general

    response = requests.post(
        webhook_url, data=json.dumps(message_data),
        headers={'Content-type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to Slack returned an error %s, the response is:\n%s'
            % (reponse.status_code, response.text)
        )
