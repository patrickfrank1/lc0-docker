#!/bin/bash

BASE_DIR=$(pwd)
CONTAINER_NAME="lc0_base"

docker container rm -f "$CONTAINER_NAME"

docker container run \
    -it \
    --name "$CONTAINER_NAME" \
    --volume "$BASE_DIR"/settings:/lc0/settings \
    --volume "$BASE_DIR"/weights:/lc0/weights \
    pafrank/lc0_cpu:base