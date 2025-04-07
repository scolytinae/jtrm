#!/usr/bin/bash

curl --header "Content-Type: application/json" \
     --request POST \
     --data "{
        \"template\": \"test-template.html.j2\",
        \"data\": {
            \"username\": \"VVasya\"
        }
    }" \
http://localhost:8000/immediate_report/