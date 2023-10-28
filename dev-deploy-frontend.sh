#!/bin/zsh

rm -rf ./static/*
cd ./vue/aca-front/ || exit
npm run build
mv dist/* ../../static
cp -r ./src/sounds/*.mp3 ../../static/assets
cp webrtc.html ../../static/webrtc.html
cd ../../
ansible-playbook -i ansible/inventory.yml ansible/dev-deploy-frontend.yml