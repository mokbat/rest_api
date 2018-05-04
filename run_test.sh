#!/bin/bash
################################################################################
# Docker Helper Script                                                         #
# -------------------------                                                    #
# This is an all purpose script which would allow you to do the following -    #
# 1) Create a clone of REST API repo                                           #
# 2) Build a Docker Image                                                      #
# 3) Spin a Docker Container                                                   #
# 4) Execute Test inside Container                                             #
################################################################################

echo "-----------------------------------"
echo "| Welcome to Docker Helper Script |"
echo "-----------------------------------"

# Check if user has docker and git
echo "This script assumes you have Git and Docker installed on your system!"
echo "If you wish to install Git and Docker, use these commands - "
echo ""
echo "-------------------------------------------------------------------------"
echo "For Git (Ubuntu) - sudo apt-get install git"
echo "For Git (RHEL and Flavors) - sudo yum install git"
echo "-------------------------------------------------------------------------"
echo ""
echo "-------------------------------------------------------------------------"
echo "For Docker (Ubuntu) - sudo apt-get install docker-ce"
echo "For Docker (RHEL and Flavors) - sudo yum install docker-ce"
echo "-------------------------------------------------------------------------"

# Should you proceed with the script
while true; do
    echo "Do you wish to proceed?"
    read -p "Enter (y/n) - " yn
    case "$yn" in
        [Yy]* )
            break ;;
        [Nn]* )
            return ;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Local Repo Directory
repodir=/tmp/rest_api

# Find current directory
cwd="$pwd"

# User wants to create a local repo clone
while true; do
    echo "Do you wish to create a local repository?"
    read -p "Enter (y/n) - " yn
    case "$yn" in
        [Yy]* )
            echo "Where do you wish to create a local repository? [Example - /tmp/rest_api]"
            echo "Ensure you have permissions rightfully set as the script will NOT change permissions!"
            read -p "Repository : " repodir
            mkdir -p "$repodir"
            git clone https://github.com/mokbat/rest_api.git "$repodir"
            repodir="$repodir"
            break;;
        [Nn]* )
            echo "Assuming you already have a local repo. [Example /tmp/rest_api]"
            echo "If you wish to manually clone - "
            echo "git clone https://github.com/mokbat/rest_api.git <base_directory>"
            echo "Please provide your local repository path?"
            read -p "Repo Path : " repodir
            break;;
        * ) echo "Please answer yes or no.";;
    esac
done
echo "-----------------------------------------------------------------------------------------"
echo "Your local repository can be accessed at - $repodir"
echo "-----------------------------------------------------------------------------------------"

# Docker Image Details
while true; do    

    # Get to the right  directory
    echo "Getting into $repodir"
    cd "$repodir" || echo "Unable to change directory to $repodir"
    
    # Tag for the name of the image
    TAG="$(date +%m_%d_%Y):$(git log -n 1 origin/master --format="%h")"
    echo "TAG has been set with value $TAG"

    # Check if the user wishes to build the container
    echo "Do you wish to build a docker image for rest api testing?"
    read -p "Enter (y/n) - " yn
    case "$yn" in
        [Yy]* )
            # Build the image
            echo "-----------------------------------------------------------------------------------------"
            echo "Building Docker Container with Tag Name - $TAG"
            echo "-----------------------------------------------------------------------------------------"
            docker build -t "$TAG" .
            break ;;
        [Nn]* )
            echo "Please build your docker image manually!"
            echo "-----------------------------------------------------------------------------------------"
            echo "Example command - docker build -t $TAG ."
            echo "-----------------------------------------------------------------------------------------"
            break ;;
        * ) echo "Please answer yes or no.";;
    esac
done

# User wants to access the container
while true; do
    echo "Do you wish to access the container?"
    read -p "Enter (y/n) - " access
    case "$access" in
        [Yy]* )
            echo "Using the current image built!"
            echo "-----------------------------------------------------------------------------------------"
            echo "Redirecting output to your container"
            echo "-----------------------------------------------------------------------------------------"
            echo ""
            docker run -t "$TAG" python3 test_rest_api.py
            echo ""
            break ;;
        [Nn]* )
            break ;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Back to the same directory
cd "$cwd" || echo "Unable to bring you back to the working directory $cwd"

echo "========================================================================================"
echo "                                   Summary                                              "
echo "========================================================================================"
echo "                                                                                        "
echo "----------------------------------------------------------------------------------------"
echo "Your local clone is located at - $repodir                                               "
echo "----------------------------------------------------------------------------------------"
echo "Docker Tag - $TAG                                                                       "
echo "----------------------------------------------------------------------------------------"
echo "                                                                                        "
echo "For manual access to the test in the future, use this command below                     "
echo "----------------------------------------------------------------------------------------"
echo "docker run -t $TAG python3 test_rest_api.py                                             "
echo "----------------------------------------------------------------------------------------"
echo "                                                                                        "
echo "Thank you for using  Helper Function!                                                   "
echo "========================================================================================"
