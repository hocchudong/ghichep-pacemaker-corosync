mkdir /opt/downloads
cd /opt/downloads
echo "proxy=http://123.30.178.220:3142" >> /etc/yum.conf
yum install git -y
git clone https://github.com/vozlt/nginx-module-vts.git

git clone https://github.com/vozlt/nginx-module-sts.git
git clone https://github.com/vozlt/nginx-module-stream-sts.git

yum -y install gcc gcc-c++ make zlib-devel pcre-devel \
openssl-devel git wget geoip-devel epel-release

yum autoremove nginx -y
wget http://nginx.org/download/nginx-1.13.0.tar.gz
tar -zxf nginx-1.13.0.tar.gz
cd nginx-1.13.0

./configure --user=nginx --group=nginx \
--add-module=/opt/downloads/nginx-module-sts/ \
--add-module=/opt/downloads/nginx-module-vts/ \
--add-module=/opt/downloads/nginx-module-stream-sts/ \
--prefix=/etc/nginx \
--sbin-path=/usr/sbin/nginx \
--conf-path=/etc/nginx/nginx.conf \
--error-log-path=/var/log/nginx/error.log \
--http-log-path=/var/log/nginx/access.log \
--pid-path=/var/run/nginx.pid \
--lock-path=/var/run/nginx.lock \
--http-client-body-temp-path=/var/cache/nginx/client_temp \
--http-proxy-temp-path=/var/cache/nginx/proxy_temp \
--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
--http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
--http-scgi-temp-path=/var/cache/nginx/scgi_temp \
--with-http_ssl_module \
--with-http_realip_module \
--with-http_addition_module \
--with-http_sub_module \
--with-http_dav_module \
--with-http_gunzip_module \
--with-http_gzip_static_module \
--with-http_random_index_module \
--with-http_secure_link_module \
--with-http_stub_status_module \
--with-mail \
--with-mail_ssl_module \
--with-file-aio \
--with-stream \
--with-http_geoip_module

make
make install

useradd -r nginx
mkdir -p /var/cache/nginx/client_temp/
chown nginx. /var/cache/nginx/client_temp/
cat << EOF > /lib/systemd/system/nginx.service
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t
ExecStart=/usr/sbin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF

chmod a+rx /lib/systemd/system/nginx.service
systemctl start nginx
systemctl enable nginx

cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.default
rm -rf /etc/nginx/nginx.conf
cat << EOF > /etc/nginx/nginx.conf

#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


## Trang thai cua cac stream
stream {
    server_traffic_status_zone;
    upstream db-backends {
        server 10.10.10.20:3306;
        server 10.10.10.30:3306 backup;
        server 10.10.10.40:3306 backup;
    }
    server {
        listen 3306;
        proxy_pass db-backends;
    }
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    ## Trang thai cua cac VHOST
    stream_server_traffic_status_zone;
    vhost_traffic_status_zone;
    geoip_country /usr/share/GeoIP/GeoIP.dat;
    vhost_traffic_status_filter_by_set_key $geoip_country_code country::*;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;
    upstream nginx-flat {
        server 10.10.10.20:80;
        server 10.10.10.30:80;
        server 10.10.10.40:80;
    }
    server {
        listen 80;
        server_name nginx.flatbase.com;
        location / {
            proxy_pass http://nginx-flat;
        }
    }

    upstream apache-flat {
        server 10.10.10.20:81;
        server 10.10.10.30:81;
        server 10.10.10.40:81;
    }
    server {
        listen 80;
        server_name apache.flatbase.com;
        location / {
            proxy_pass http://apache-flat;
        }
    }

    server {
        listen       80;
        server_name  status-nginx.com;
        location / {
            return 301 /status-web;
        }
        
        ## Prefix cua trang xem trang thai
        
        location /status-stream {
            stream_server_traffic_status_display;
            stream_server_traffic_status_display_format html;
        }
        vhost_traffic_status_filter_by_set_key $geoip_country_code country::$server_name;
        location /status-web {
            vhost_traffic_status_display;
            vhost_traffic_status_display_format html;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
        location /status-native {
            stub_status on;
        }
    }
}

EOF

systemctl start nginx 
systemctl enable nginx


sudo systemctl disable firewalld
sudo systemctl stop firewalld

sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
echo "127.0.0.1        localhost" > /etc/hosts
echo "10.10.10.8       lb01" >> /etc/hosts
echo "10.10.10.9       lb02" >> /etc/hosts
echo "10.10.10.10      lb03" >> /etc/hosts
echo "10.10.10.20      nd01" >> /etc/hosts
echo "10.10.10.30      nd02" >> /etc/hosts
echo "10.10.10.40      nd03" >> /etc/hosts

yum -y install pacemaker pcs

systemctl start pcsd 
systemctl enable pcsd

passwd hacluster