#!/usr/bin/env bash
# Script sets up web servers for te dedployment of Airbnb web_static

sudo apt-get upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "This is some test text" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
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
                alias /data/web_static/current/;
        }
}
EOF

sudo nginx -t
sudo service nginx restart
