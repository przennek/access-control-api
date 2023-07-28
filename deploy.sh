#!/bin/zsh

if [ -z $1 ]; then
  echo "Usage ./deploy.sh <version_tag>"
fi

# Define the VERSION_TAG environment variable
export VERSION_TAG=$1

# Use envsubst to replace the placeholder with the actual value
envsubst < ./config/docker-compose-template.yml > ./config/docker-compose.yml

ansible-playbook -i ansible/inventory.yml ansible/access-control-api.yml