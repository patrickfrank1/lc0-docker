#!/bin/bash

IMAGE_TAG="pafrank/lc0_cpu:base"

sudo docker image build \
    --tag "$IMAGE_TAG" \
    --file=Dockerfile.base \
    .

sh ./run.sh
