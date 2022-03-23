#!/bin/sh

# start the virtual environment
. env/bin/activate

# get the flask server/app going in this shell
export FLASK_ENV=development
# production server would look like this:
# export FLASK_APP=app
flask run
