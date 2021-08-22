#!/bin/bash

BASE_DIR=$(pwd)
CONTAINER_NAME="lc0_base"

if [ "$(docker ps -a | grep $CONTAINER_NAME)" ]; then
  docker container rm -f "$CONTAINER_NAME"
fi

docker container run \
    -it \
    --name "$CONTAINER_NAME" \
    --volume "$BASE_DIR"/settings:/lc0/settings \
    --volume "$BASE_DIR"/weights:/lc0/weights \
    pafrank/lc0_cpu:base