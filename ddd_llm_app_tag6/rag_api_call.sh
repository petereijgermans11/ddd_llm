#!/usr/bin/env bash

curl -X 'POST' 'http://127.0.0.1:8000/query' \
-H 'Content-Type: application/json' \
-d '{"question": "Leg uit hoe de organisatie van ProRail is onderverdeeld."}'
