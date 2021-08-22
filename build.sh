#!/bin/bash

IMAGE_TAG="pafrank/lc0_cpu:lc0_sf_base"

sudo docker image build \
    --tag "$IMAGE_TAG" \
    --file=Dockerfile.lc0_sf_base \
    .

sh ./run.sh
