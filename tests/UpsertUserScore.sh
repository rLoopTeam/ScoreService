#!/usr/bin/env bash

curl -v -H "Content-Type: application/json" -X POST -d '{"playerName":"foxlet","score":"200"}' http://localhost:8080/api/UpsertUserScore
