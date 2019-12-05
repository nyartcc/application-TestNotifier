# NYARTCC Test Notifier
A simple Python script that scans the database for pending tests that have been submitted, but not graded yet. If the test has been pending for more than 12 hours, notify either training staff or senior staff if is a visitor.

## Configuration
This script uses Slack webhooks to post messages to a channel when required. The webhooks are defined in a .env file and needs to be customized by the user prior to use.
Additionally, the .env file also contains database information that the user must customize.
