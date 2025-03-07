#!/usr/bin/env bash
# Script sets up web servers for te dedployment of Airbnb web_static

sudo apt-get upgrade
sudo apt-get -y install nginx
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "This is some test text" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/html;
	index index.html;

	server_name _;

	location / {
		try_files \$uri \$uri/ =404;
	}

	location /redirect_me {
		return 301 https://www.google.com/;
	}
	
	location /hbnb_static {
		alias /data/web_static/current/
	}
}
EOF

sudo nginx -t
sudo service nginx restart
