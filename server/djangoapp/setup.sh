#!/bin/bash

# Install Python 3.9
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-distutils

# Upgrade pip
pip install --upgrade pip

# Install Cloudant
pip install Cloudant

pip install ibm_cloud_sdk_core

pip install requests
