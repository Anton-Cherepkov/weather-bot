#!/usr/bin/env bash

# Names to identify images and containers of this app
APP_NAME=weather-bot
CONTAINER_NAME=weather-bot
PROJECT_NAME=/weather-bot

# Output colors
NORMAL="\\033[0;39m"
RED="\\033[1;31m"
BLUE="\\033[1;34m"


log() {
  echo -e "$BLUE > $1 $NORMAL"
}

error() {
  echo ""
  echo -e "$RED >>> ERROR - $1$NORMAL"
}

build() {
    log "Building Docker image"
    docker build -t ${APP_NAME} .
    [ $? != 0 ] && error "Docker image build failed !" && exit 100
}

run() {
    log "Running the container"
	  docker run \
		  -e DISPLAY=unix${DISPLAY} \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      --privileged \
      --rm \
      --name=${CONTAINER_NAME} \
      -v ${PWD}:${PROJECT_NAME} ${APP_NAME}
}

stop() {
    log "Stopping and removing the container ${CONTAINER_NAME}"
    docker stop ${CONTAINER_NAME}; docker rm ${CONTAINER_NAME}
}

$*