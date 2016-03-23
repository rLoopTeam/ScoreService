#!/usr/bin/env bash

echo Starting uWSGI Emperor

UWSGI=/var/www/ScoreService/venv/bin/uwsgi
LOGTO=/var/www/ScoreService/log/uwsgi/emperor.log
BASE=/var/www/ScoreService

nohup $UWSGI --master --emperor $BASE/vassals --die-on-term --uid www-data --gid www-data --logto $LOGTO &>/dev/null &