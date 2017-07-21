def customs_cmd():
	os.system("echo '======================================================================================================='")
	os.system("echo '===                                        MAIN                                                     ==='")
	os.system("echo '======================================================================================================='")
	print "Enter `exit` to go out..."
	while True:
		try:
			command = raw_input("[root@127.0.0.1] ~#: ")
			if command == "exit":
				break
			elif "sudo" in command:
				print "Forwarding ..."
		except Exception as e:
			raise e
		finally:
			os.system(command)

def install_nginx_package():
	os.system("echo '======================================================================================================='")
	os.system("echo '===                                        MAIN                                                     ==='")
	os.system("echo '======================================================================================================='")
	temp_cmd = """
	echo "[nginx]" >> /etc/yum.repos.d/nginx.repo
	echo "name=nginx repo" >> /etc/yum.repos.d/nginx.repo
	echo "baseurl=http://nginx.org/packages/mainline/centos/7/x86_64/" >> /etc/yum.repos.d/nginx.repo
	echo "gpgcheck=0" >> /etc/yum.repos.d/nginx.repo
	echo "enabled=1" >> /etc/yum.repos.d/nginx.repo
	"""
	os.system(temp_cmd)
	str_install_nginx = """
	yum install nginx -y
	systemctl start nginx
	systemctl enable nginx
	echo 'Install NGINX done.'
	"""
	os.system(str_install_nginx)
	pass

def install_nginx_source():
	os.system("echo '======================================================================================================='")
	os.system("echo '===                                        MAIN                                                     ==='")
	os.system("echo '======================================================================================================='")
	print """
	System will being install NGINX version 1.11.13
	Installing NGINX Dependencies
	"""
	depend_cmd = """
	echo 'Git will being install on system'
	yum -y install gcc gcc-c++ make zlib-devel pcre-devel \
	openssl-devel git wget geoip-devel epel-release git
	"""
	os.system(depend_cmd)
	temp_cmd = """
	echo 'Downloading source code of NGINX'
	cd /opt/downloads
	wget http://nginx.org/download/nginx-1.13.0.tar.gz
	tar -zxf nginx-1.13.0.tar.gz
	cd nginx-1.13.0
	"""
	os.system(temp_cmd)
	temp_cmd = """
	./configure --user=nginx --group=nginx \
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
	"""
	os.system(temp_cmd)
	temp_cmd = """
	useradd -r nginx
	mkdir -p /var/cache/nginx/client_temp/
	chown nginx. /var/cache/nginx/client_temp/
	echo '[Unit]' >> /lib/systemd/system/nginx.service
	echo 'Description=The NGINX HTTP and reverse proxy server' >> /lib/systemd/system/nginx.service
	echo 'After=syslog.target network.target remote-fs.target nss-lookup.target' >> /lib/systemd/system/nginx.service
	echo '[Service]' >> /lib/systemd/system/nginx.service
	echo 'Type=forking' >> /lib/systemd/system/nginx.service
	echo 'PIDFile=/run/nginx.pid' >> /lib/systemd/system/nginx.service
	echo 'ExecStartPre=/usr/sbin/nginx -t' >> /lib/systemd/system/nginx.service
	echo 'ExecStart=/usr/sbin/nginx' >> /lib/systemd/system/nginx.service
	echo 'ExecReload=/bin/kill -s HUP $MAINPID' >> /lib/systemd/system/nginx.service
	echo 'ExecStop=/bin/kill -s QUIT $MAINPID' >> /lib/systemd/system/nginx.service
	echo 'PrivateTmp=true' >> /lib/systemd/system/nginx.service
	echo '[Install]' >> /lib/systemd/system/nginx.service
	echo 'WantedBy=multi-user.target' >> /lib/systemd/system/nginx.service
	chmod a+rx /lib/systemd/system/nginx.service
	systemctl start nginx
	systemctl enable nginx
	echo 'Install NGINX done.'
	"""
	os.system(temp_cmd)
	

def install_nginx():
	while True:
		os.system("echo '======================================================================================================='")
		os.system("echo '===                                        MAIN                                                     ==='")
		os.system("echo '======================================================================================================='")
		print """
		1. Installing from packages
		2. Installing from source code
		3. Customs
		4. Exit
		"""
		ans = raw_input("Choose one method to install nginx: ")
		if ans == "1":
			install_nginx_package()
			break
		elif ans == "2":
			install_nginx_source()
			break
		elif ans == "3":
			customs_cmd()
		elif ans == "4":
			break
		else:
			print "You only can choose 1, 2 or 3."
		pass

def install_httpd():
	while True:
		os.system("echo '======================================================================================================='")
		os.system("echo '===                                        MAIN                                                     ==='")
		os.system("echo '======================================================================================================='")
		print """
		1. Install from packages
		2. Customs
		3. Exit
		"""
		ans = raw_input("Choose one a method install: ")
		if ans == "1":
			temp_cmd = """
			clear
			yum update -y
			echo 'Installing Apache...'
			yum install httpd -y
			echo 'Installed Apache'
			"""
			os.system(temp_cmd)
		elif ans == "2":
			customs_cmd()
		elif ans == "3":
			break
		else:
			print "You only can choose 1, 2 or 3."
			pass
			
def install_pcmk():
	temp_cmd = """
	clear
	echo 'Installing pacemaker and corosync with some fence agents'
	yum install pcs fence-agents -y
	systemctl start pcsd 
	systemctl enable pcsd
	systemctl enable corosync
	echo 'Install pacemaker and corosync done.'
	"""
	os.system(temp_cmd)
	pwd = raw_input("Input new password for user hacluster created: ")
	temp_cmd = "echo " + pwd + " | passwd --stdin hacluster"
	os.system(temp_cmd)
	return pwd

def create_resource_Virtual_IP():
	while True:
		os.system("echo '======================================================================================================='")
		os.system("echo '===                                        MAIN                                                     ==='")
		os.system("echo '======================================================================================================='")
		print """
		1. Default ( with netmask default is 24)
		2. Customs
		3. Exit
		"""
		ans = raw_input("Choose: ")
		if ans == "1":
			temp = raw_input("Input your ip address which you want make it to VIP: ")
			temp_cmd = """
			echo 'Creating resource ...'
			pcs resource create Virtual_IP ocf:heartbeat:IPaddr2 ip=""" + temp + """ cidr_netmask=24 op monitor interval=30s
			echo 'Done'
			"""
			os.system(temp_cmd)
		elif ans == "2":
			customs_cmd()
		elif ans == "3":
			break
		else:
			print "You only can choose 1, 2 or 3."
			pass

def create_resource_web_cluster():
	while True:
		os.system("echo '======================================================================================================='")
		os.system("echo '===                                        MAIN                                                     ==='")
		os.system("echo '======================================================================================================='")
		print """
		1. Default ()
		2. Customs
		3. Exit
		"""
		ans = raw_input("Choose: ")
		if ans == "1":
			temp_name = raw_input("Input name's resource (default: Web_Cluster): ")
			if temp_name == "":
				temp_name = "Web_Cluster"
			temp_type = raw_input("Input type's resource (default: ocf:heartbeat:nginx): ")
			if temp_type == "":
				temp_type = "ocf:heartbeat:nginx"
			temp_cffile = raw_input("Input file config of resource (default: /etc/nginx/nginx.conf): ")
			if temp_cffile == "":
				temp_cffile = "/etc/nginx/nginx.conf"
			temp_cmd = """
			pcs resource create """ + temp_name + """ """ + temp_type + """ configfile=""" + temp_cffile + """ status10url op monitor interval=5s
			echo 'Done.'
			"""
			os.system(temp_cmd)
		elif ans == "2":
			customs_cmd()
		elif ans == "3":
			break
		else:
			print "You only can choose "
			pass

def create_constraint_resource():
	temp_cmd = """
	pcs constraint order Virtual_IP then Web_Cluster
	pcs constraint colocation add Web_Cluster with Virtual_IP INFINITY
	echo "Created done."
	"""
	os.system(temp_cmd)
	

def disable_firewall():
	temp_cmd = """
	sudo systemctl disable firewalld
	sudo systemctl stop firewalld
	sed -i 's/SElinux=enforcing/SElinux=disabled/g' /etc/sysconfig/selinux
	sed -i 's/SElinux=enforcing/SElinux=disabled/g' /etc/selinux/config
	setenforce 0
	echo 'Disabled firewall'
	"""
	os.system(temp_cmd)
	

def install_main_webserver():
	while True:
		os.system("echo '======================================================================================================='")
		os.system("echo '===                                        MAIN                                                     ==='")
		os.system("echo '======================================================================================================='")
		print """
		1. Install NGINX
		2. Install Apache
		3. Exit
		"""
		ans = raw_input("Choose: ")
		pass
		if ans == "1":
			install_nginx()
		elif ans == "2":
			install_httpd()
		elif ans == "3":
			break
		else:
			print "You only can choose 1, 2 or 3"
			pass

def create_cluster():
	cluster = []
	temp = ""
	temp_num = input("Input number node in cluster: ")
	for i in range(temp_num):
		temp_name = raw_input("Input name's node: ")
		temp_ip = raw_input("Input ip's node: ")
		e = temp_name, temp_ip
		cluster.append(e)
	for k, v in dict(cluster).iteritems():
		temp_cmd = """echo """ + v + """    """ + k + """ >> /etc/hosts"""
		os.system(temp_cmd)
	for x in dict(cluster).iterkeys():
		temp += x + " "
	os.system("pcs cluster auth " + temp + " -u hacluster -p "+ install_pcmk())
	print "Processing create a cluster"
	temp_name = raw_input("Input name's cluster (default: ha_cluster): ")
	pass
	if temp_name == "":
		temp_name = "ha_cluster"
	os.system("pcs cluster setup --name " + temp_name + " " + temp)
	print "Created done. \n Starting all node ..."
	temp_cmd = """
	pcs cluster start --all
	pcs cluster enable --all
	"""
	os.system(temp_cmd)
	
def disable_fences():
	temp_cmd = """
	pcs property set stonith-enabled=false
	pcs property set no-quorum-policy=ignore
	pcs property set default-resource-stickiness="INFINITY"
	"""
	os.system(temp_cmd)


def main():
	try:
		while True:
			os.system("echo '======================================================================================================='")
			os.system("echo '===                                        MAIN                                                     ==='")
			os.system("echo '======================================================================================================='")
			print """
			1. Install pacemaker and corosync
			2. Install nginx, apache
			3. Create a cluster
			4. Create resource Virtual_IP
			5. Create resource Web_Cluster
			6. Create constraint between Virtual_IP with Web_Cluster
			7. Disable firewall (recommend)
			8. Customs
			9. Exit
			"""
			ans = raw_input("\t Choose: ")
			pass
			if ans == "1":
				install_pcmk()
				pass
			elif ans == "2":
				install_main_webserver()
				pass
			elif ans == "3":
				create_cluster()
				disable_fences()
				pass
			elif ans == "4":
				create_resource_Virtual_IP()
				pass
			elif ans == "5":
				create_resource_web_cluster()
				pass
			elif ans == "6":
				create_constraint_resource()
				pass
			elif ans == "7":
				disable_firewall()
				pass
			elif ans == "8":
				customs_cmd()
				pass
			elif ans == "9":
				break
			else:
				print "You only can choose 1-9. "
				pass
	except BaseException as e:
		raise e
try:
	import os
	if os.getuid() == 0:
		main()
	else:
		print "You must run this script with sudo right."
except Exception as e:
	raise e