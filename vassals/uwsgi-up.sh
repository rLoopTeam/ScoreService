#!/usr/bin/env bash

pip3.4 install virtualenv
virtualenv venv
. venv/bin/activate
venv/bin/pip3.4 install flask
venv/bin/pip3.4 install requests
venv/bin/pip3.4 install json
deactivate