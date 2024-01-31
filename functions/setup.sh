#!/bin/bash

# Install Python 3.9
sudo apt-get update
sudo apt-get install -y python3.9 python3.9-distutils

# Upgrade pip
/usr/bin/python3.9 -m pip install --upgrade pip

# Install Cloudant
/usr/bin/python3.9 -m pip install Cloudant

# Install Flask
/usr/bin/python3.9 -m pip install Flask

/usr/bin/python3.9 -m pip install ibm_cloud_sdk_core

/usr/bin/python3.9 -m pip install requests
