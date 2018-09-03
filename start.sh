#!/usr/bin/env sh

IMAGE_NAME="task_list"
CONTAINER_NAME="task-list"
MAX_LOG_SIZE="8m"
MEMORY="256M"

echo "Stopping container..."
sudo docker stop $CONTAINER_NAME

echo "Deleting container..."
sudo docker rm $CONTAINER_NAME

set -e

echo "Re-building image..."
sudo docker build -t $IMAGE_NAME .

echo "Creating and starting container..."
sudo docker run -d --name $CONTAINER_NAME \
    -m $MEMORY \
    --log-opt max-size=$MAX_LOG_SIZE \
    -v $(realpath src):/home/tester/task_list/ \
    -p 127.0.0.1:48080:8000 \
    $IMAGE_NAME
    # -it $IMAGE_NAME bash

echo "Tailing logs..."
sudo docker logs -f $CONTAINER_NAME
