#!/bin/zsh

rm -rf ./static/*
cd ./vue/aca-front/ || exit
npm run build
mv dist/* ../../static
cd ../../

ansible-playbook -i ansible/inventory.yml ansible/dev-deploy-frontend.yml