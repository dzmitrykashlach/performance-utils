#!/bin/bash
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images --format="{{.Repository}} {{.ID}}" | grep "^local" | cut -d' ' -f2)
