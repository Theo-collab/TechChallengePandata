#!/bin/bash

cd /root/TechChall/obsfs_Ubuntu14.04_amd64

sudo apt install curl -y
sudo apt install inkscape -y

sudo apt-get remove --auto-remove libcurl4-openssl-dev
sudo apt-get install libcurl3 -y
./obsfs mountpoint /root/TechChall/data/ -o url=obs.ap-southeast-1.myhuaweicloud.com -o passwd_file=/etc/passwd-obsfs -o use_ino

# image recognition
sudo apt-get install tesseract-ocr tesseract-ocr-deu -y