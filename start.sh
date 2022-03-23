#!/bin/sh

# start the virtual environment
. env/bin/activate

# get the flask server/app going in this shell
# debug only
export FLASK_ENV=development
# export FLASK_APP=app
flask run
