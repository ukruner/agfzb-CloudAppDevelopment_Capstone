#!/bin/bash

# Install Python 3.9
sudo apt-get update
sudo apt-get install -y python3.9 python3.9-distutils

# Upgrade pip
pip install --upgrade pip

# Install Cloudant
pip install Cloudant

# Install Flask
pip install Flask

pip install ibm_cloud_sdk_core

pip install requests
