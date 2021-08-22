#!/bin/bash

BASE_DIR=$(pwd)
CONTAINER_NAME="lc0_fileio"

if [ "$(docker ps -a | grep $CONTAINER_NAME)" ]; then
  docker container rm -f "$CONTAINER_NAME"
fi

docker container run \
    -d \
    --name "$CONTAINER_NAME" \
    --volume "$BASE_DIR"/settings:/lc0/settings \
    --volume "$BASE_DIR"/weights:/lc0/weights \
    --volume "$BASE_DIR"/analysis:/home/daemon/analysis \
    pafrank/lc0_cpu:fileio