#!/bin/bash

dead_container=$(docker ps -aq -f status=exited)
if [ "${dead_container}x" != "x" ]; then
docker rm -v $(docker ps -aq -f status=exited)
fi

dead_image=$(docker images | grep "^<none>" | awk '{print $3}')
if [ "${dead_image}x" != "x" ]; then
docker rmi $(docker images | grep "^<none>" | awk '{print $3}')
fi
