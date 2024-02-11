#!/bin/bash

# Install Python 3.9
sudo apt-get update

# Install Cloudant
/usr/bin/python3.9 pip install Cloudant

/usr/bin/python3.9 pip install ibm_cloud_sdk_core

/usr/bin/python3.9 pip install requests

/usr/bin/python3.9 pip install ibm_watson
