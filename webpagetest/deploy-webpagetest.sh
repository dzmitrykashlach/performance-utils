#!/bin/bash
# Guide:
# https://medium.com/@francis.john/local-webpagetest-using-docker-90441d7c2513
# https://docs.docker.com/engine/install/ubuntu/
# Enhance docker security with AppArmor:
# https://docs.docker.com/engine/security/
# https://docs.docker.com/engine/security/apparmor/
# https://appfleet.com/blog/advanced-docker-security-with-apparmor/
pull_webpagetest()
{
        # pull webpage/server;
        sudo docker pull webpagetest/server

        # pull webpage/agent;

        sudo docker pull webpagetest/agent

}

rebuild_webpagetest()
{
       #re-build server;
        cd performance-utils*/webpagetest/server
        # re-build server
        sudo docker build -t local-wptserver .
        cd ../agent
        # re-build agent;
        chmod u+x script.sh
        sudo docker build -t local-wptagent .
        cd ../server
}
run_webpagetest()
{
        # run server;
        sudo docker run -d -p 4000:80 local-wptserver
        # run agent;
        sudo docker run -d -p 4001:80 --network="host"  -e "SERVER_URL=http://localhost:4000/work/" -e "LOCATION=Test"  local-wptagent

}

which docker

if [ $? -eq 0 ]
then
    docker --version | grep "Docker version"
    if [ $? -gt 0 ]
    then
        echo "Docker will be installed..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
    else
        echo "Found docker installation...."
              if [[ "$(docker image inspect webpagetest/server:latest 2> /dev/null)" == "" ]]; then
                 pull_webpagetest
              fi
        rebuild_webpagetest
        run_webpagetest
    fi
else
    echo "Failed to check docker version" >&2
fi
