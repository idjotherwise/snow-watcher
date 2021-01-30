#!/usr/bin/env bash

apt update
apt upgrade -y

apt install zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"


# Stop the hackers
sudo apt install fail2ban -y

ufw allow 22
ufw allow 80
ufw allow 443
ufw enable

apt install acl -y
useradd -M apiuser
usermod -L apiuser
setfacl -m u:apiuser:rwx /apps/logs/weather_api

# Web app file structure
mkdir /apps
chmod 777 /apps
mkdir /apps/logs
mkdir /apps/logs/weather_api
mkdir /apps/logs/weather_api/app_log
# chmod 777 /apps/logs/weather_api
cd /apps

cd /apps
python3 -m venv venv
source /apps/venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install --upgrade httpie glances
pip install --upgrade gunicorn uvloop httptools

# clone the repo:
cd /apps
git clone https://github.com/