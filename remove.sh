#!/bin/bash

CONTAINER_NAME="lc0_sf_base"

if [ "$(docker ps -a | grep $CONTAINER_NAME)" ]; then
  docker container rm -f "$CONTAINER_NAME"
fi
