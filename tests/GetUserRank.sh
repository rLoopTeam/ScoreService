#!/usr/bin/env bash

curl -v -H "Content-Type: application/json" -X POST -d '{"playerName":"foxlet"}' http://localhost:8080/api/GetUserRank
