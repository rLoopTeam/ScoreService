#!/usr/bin/env bash

curl -H "Content-Type: application/json" -X POST -d '{"playerName":"foxlet","score":"200"}' http://localhost:8084/api/UpsertUserScore
