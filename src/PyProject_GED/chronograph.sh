#!/bin/bash
#   If you aren't using a virtual environment, you might
#   try sourcing whichever file it is that you define your
#   PYTHONPATH in (~/.basrc, ~/.bash_profile, etc)
#
#   Pass this script one argument: the path to your project.
#   (The directory in which your manage.py is)

PROJECT_PATH=/home/webapps/GED/PyProject_GED
source $PROJECT_PATH"/../bin/activate" && cd $PROJECT_PATH && python manage.py cron
