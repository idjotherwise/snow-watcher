#!/usr/bin/env bash

apt update
apt upgrade -y

apt install zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install some OS dependencies:
sudo apt-get install -y -q build-essential git zip unload tree
sudo apt-get install -y -q python3-pip python3-dev python3-venv

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
git clone https://github.com/idjotherwise/snow-watcher app_repo

# setup the webapp
cp /apps/app_repo/server/units/weather.service /etc/systemd/system/

systemctl start weather
systemctl status weather
systemctl enable weather
### to restart use:
# systemctl restart weather

# setup public facing server
apt install nginx

# rm /etc/nginx/sites-enabled/default

cp /apps/app_repo/server/nginx/weather.nginx /etc/nginx/sites-enabled
update-rc.d nginx enable
service nginx restart

add-apt-repository ppa:certbot/certbot
apt install python3-certbox-nginx
certbot --nginx -d weatherotherwise.xyz
