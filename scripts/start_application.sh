#!/bin/bash
sudo apt install python3 pip3
cd /var/www/myapp
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
pip3 install gunicorn