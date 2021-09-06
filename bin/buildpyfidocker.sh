#!/bin/bash

cd docker
docker build - < Dockerfile.pyfi --tag pyfi:latest
cd ..
