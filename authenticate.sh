#!/usr/bin/env bash
token=$(curl -H "Host:milobella.com" -H "Content-Type:application/json" https://milobella.com:10443/users/authenticate -d "{\"username\": \"$MILOBELLA_USERNAME\", \"password\":\"$MILOBELLA_PASSWORD\"}" | jq -r '.token')
export MILOBELLA_AUTHORIZATION_TOKEN=$token
