#!/bin/bash

if [ -z $1 ]; then
  echo "Usage ./build_armv7.sh <version_tag>"
fi

docker buildx build --platform linux/arm/v7 -t przennek/access-control-api-armv7:$1 --push .
