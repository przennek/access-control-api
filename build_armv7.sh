#!/bin/bash

if [ -z $1 ]; then
  echo "Usage ./build_armv7.sh <version_tag>"
fi

rm -rf ./static/*
cd ./vue/aca-front/ || exit
npm run build
mv dist/* ../../static
cp -r ./src/sounds/*.mp3 ../../static/assets
cd ../../

docker buildx build --platform linux/arm/v7 -t przennek/access-control-api-armv7:$1 --push .
