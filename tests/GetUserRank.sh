#!/usr/bin/env bash

curl -v -H "Content-Type: application/json" -X POST -d '{"player":"foxlet"}' http://localhost:8080/api/GetUserRank
