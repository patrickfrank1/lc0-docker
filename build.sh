#!/bin/bash

IMAGE_TAG="pafrank/lc0_cpu:fileio"

sudo docker image build \
    --tag "$IMAGE_TAG" \
    --file=Dockerfile.fileio \
    .

sh ./run.sh
