# 1. HA Proxy - High Availability Proxy

____

# Mục lục


- [1.1 Mục đích sử dụng của HA Proxy](#about)
- [1.2 Cài đặt HA Proxy](#install)
- [1.3 Tổng quan về cấu trúc file cấu hình của HA Proxy](#instruc)
- [Các nội dung khác](#content-others)

____

# <a name="content">Nội dung</a>

- ### <a name="about">1.1 Mục đích sử dụng của HA Proxy</a>
	- Là phần mềm cân bằng tải TCP/HTP và giải pháp proxy mã nguồn mở phổ biến, có thể chạy trên Linux, Solaris, và FreeBSD. Nó thường dùng để cải thiện hiệu suất (performance) và sự tin cậy (reliability) của môi trường máy chủ bằng cách phân tán lưu lượng tải (workload) trên nhiều máy chủ (như web, application, database)

- ### <a name="install">1.2 Cài đặt HA Proxy</a>

	- Để cài đặt haproxy ta sử dụng câu lệnh sau:
		đối với Centos:

			yum install -y haproxy

		đối với Ubuntu:

			apt-get install -y haproxy

- ### <a name="instruc">1.3 Tổng quan về cấu trúc file cấu hình của HA Proxy</a>
	- Sau khi cài đặt haproxy, ta sẽ quản lý các cấu hình của haproxy cho hệ thống với việc quản lý nội dung trong file `/etc/haproxy/haproxy.cfg`. File có nội dung tương tự như sau:

			#---------------------------------------------------------------------
			# Example configuration for a possible web application.  See the
			# full configuration options online.
			#
			#   http://haproxy.1wt.eu/download/1.4/doc/configuration.txt
			#
			#---------------------------------------------------------------------

			#---------------------------------------------------------------------
			# Global settings
			#---------------------------------------------------------------------
			global
			    # to have these messages end up in /var/log/haproxy.log you will
			    # need to:
			    #
			    # 1) configure syslog to accept network log events.  This is done
			    #    by adding the '-r' option to the SYSLOGD_OPTIONS in
			    #    /etc/sysconfig/syslog
			    #
			    # 2) configure local2 events to go to the /var/log/haproxy.log
			    #   file. A line like the following can be added to
			    #   /etc/sysconfig/syslog
			    #
			    #    local2.*                       /var/log/haproxy.log
			    #
			    log         127.0.0.1 local2

			    chroot      /var/lib/haproxy
			    pidfile     /var/run/haproxy.pid
			    maxconn     4000
			    user        haproxy
			    group       haproxy
			    daemon

			    # turn on stats unix socket
			    stats socket /var/lib/haproxy/stats

			#---------------------------------------------------------------------
			# common defaults that all the 'listen' and 'backend' sections will
			# use if not designated in their block
			#---------------------------------------------------------------------
			defaults
			    mode                    tcp
			    log                     global
			    option                  tcplog
			    option                  dontlognull
			    option http-server-close
			    option forwardfor       except 127.0.0.0/8
			    option                  redispatch
			    retries                 3
			    timeout http-request    10s
			    timeout queue           1m
			    timeout connect         10s
			    timeout client          1m
			    timeout server          1m
			    timeout http-keep-alive 10s
			    timeout check           10s
			    maxconn                 3000

			#---------------------------------------------------------------------
			# main frontend which proxys to the backends
			#---------------------------------------------------------------------
			frontend  main *:80
			    acl url_static       path_beg       -i /static /images /javascript /stylesheets
			    acl url_static       path_end       -i .jpg .gif .png .css .js

			    use_backend static          if url_static
			    default_backend             app

			#---------------------------------------------------------------------
			# static backend for serving up images, stylesheets and such
			#---------------------------------------------------------------------
			backend static
			    balance     roundrobin
			    server      static 127.0.0.1:4331 check

			#---------------------------------------------------------------------
			# round robin balancing between the various backends
			#---------------------------------------------------------------------
			backend app
			    balance     roundrobin
			    server  app1 10.10.10.10:80 check
			    server  app2 10.10.10.127:80 check

	- Nhìn vào nội dung file trên, ta có thể thấy được rằng, 1 file cấu hình của haproxy cơ bản có 4 phần chính:

		- global
		- defaults
		- frontend
		- backend

	- Chức năng của các phần được quy định cụ thể như sau:

		- global: Đây là phần dùng để khai báo các cấu hình dùng chung các tham số liên quan đến hệ thống và chỉ khai báo một lần để dùng cho tất cả các phần khác trong file cấu hình. Có thể bao gồm các từ khóa:

			 * Process management and security
			   - ca-base
			   - chroot
			   - crt-base
			   - cpu-map
			   - daemon
			   - description
			   - deviceatlas-json-file
			   - deviceatlas-log-level
			   - deviceatlas-separator
			   - deviceatlas-properties-cookie
			   - external-check
			   - gid
			   - group
			   - hard-stop-after
			   - log
			   - log-tag
			   - log-send-hostname
			   - lua-load
			   - nbproc
			   - node
			   - pidfile
			   - presetenv
			   - resetenv
			   - uid
			   - ulimit-n
			   - user
			   - setenv
			   - stats
			   - ssl-default-bind-ciphers
			   - ssl-default-bind-options
			   - ssl-default-server-ciphers
			   - ssl-default-server-options
			   - ssl-dh-param-file
			   - ssl-server-verify
			   - unix-bind
			   - unsetenv
			   - 51degrees-data-file
			   - 51degrees-property-name-list
			   - 51degrees-property-separator
			   - 51degrees-cache-size
			   - wurfl-data-file
			   - wurfl-information-list
			   - wurfl-information-list-separator
			   - wurfl-engine-mode
			   - wurfl-cache-size
			   - wurfl-useragent-priority

			 * Performance tuning
			   - max-spread-checks
			   - maxconn
			   - maxconnrate
			   - maxcomprate
			   - maxcompcpuusage
			   - maxpipes
			   - maxsessrate
			   - maxsslconn
			   - maxsslrate
			   - maxzlibmem
			   - noepoll
			   - nokqueue
			   - nopoll
			   - nosplice
			   - nogetaddrinfo
			   - noreuseport
			   - spread-checks
			   - server-state-base
			   - server-state-file
			   - tune.buffers.limit
			   - tune.buffers.reserve
			   - tune.bufsize
			   - tune.chksize
			   - tune.comp.maxlevel
			   - tune.http.cookielen
			   - tune.http.maxhdr
			   - tune.idletimer
			   - tune.lua.forced-yield
			   - tune.lua.maxmem
			   - tune.lua.session-timeout
			   - tune.lua.task-timeout
			   - tune.lua.service-timeout
			   - tune.maxaccept
			   - tune.maxpollevents
			   - tune.maxrewrite
			   - tune.pattern.cache-size
			   - tune.pipesize
			   - tune.rcvbuf.client
			   - tune.rcvbuf.server
			   - tune.recv_enough
			   - tune.sndbuf.client
			   - tune.sndbuf.server
			   - tune.ssl.cachesize
			   - tune.ssl.lifetime
			   - tune.ssl.force-private-cache
			   - tune.ssl.maxrecord
			   - tune.ssl.default-dh-param
			   - tune.ssl.ssl-ctx-cache-size
			   - tune.vars.global-max-size
			   - tune.vars.proc-max-size
			   - tune.vars.reqres-max-size
			   - tune.vars.sess-max-size
			   - tune.vars.txn-max-size
			   - tune.zlib.memlevel
			   - tune.zlib.windowsize

			 * Debugging
			   - debug
			   - quiet

		- defaults: Khai báo các cấu hình cùng với các thông số mặc định cho tất cả các phần khác nhau trong file cấu hình sau sự xuất hiện khai báo `defaults`. Để có thể thay đổi giá trị của các tham số trong nó ứng với các trường hợp, ta cần phải viết lại khai báo cấu hình đó trong một phần khác của file cấu hình hoặc đưa vào trong một phần `defaults` mới.

		- frontend: khai báo cấu hình và cách thức các request sẽ được chuyển hướng đến backends. Trong phần này thường bao gồm các thành phần sau:

			- ACLs
			- Các quy tắc để sử dụng backends phù hợp hoặc sử dụng một defaults backends phụ thuộc vào điều kiện ACL.
			- Tóm lại, nó dùng để khai báo danh sách các sockets đang lắng nghe kết nối để cho phép client kết nối tới.

		- backend: là phần khai báo danh sách các server mà các kết nối client sẽ được chuyển hướng tới đó với các thuật toán kèm theo như: round robin, health check, leastconn,...

		- Ngoài ra còn có các phần khác điển hình như `listen`. Phần này là tổ hợp khai báo của frontend và backend. Nó kém linh hoạt hơn khi sử dụng 2 phần frontend và backend riêng biệt. Nó thể hiện như là một cấu hình `tĩnh` trong file cấu hình haproxy.

	- Ý nghĩa của các dòng cấu hình cơ bản trong haproxy sẽ được nói rõ hơn vào các phần sau.
____

# <a name="content-others">Các nội dung khác</a>
- [A. Tổng quan về High Availability](pcmk-ha-overview.md)
	+ [A.1 Giới thiệu về High Availability](pcmk-ha-overview.md#whatis-ha)
	+ [A.2 Các khái niệm, thuật ngữ cần biết trong HA](pcmk-ha-overview.md#concepts)
		+ [A.2.1 Cluster](pcmk-ha-overview.md#whatis-cl)
		+ [A.2.2 Resource](pcmk-ha-overview.md#resource)
		+ [A.2.3 Pacemaker](pcmk-ha-overview.md#pacemaker)
		+ [A.2.4 Corosync](pcmk-ha-overview.md#corosync)
		+ [A.2.5 Quorum](pcmk-ha-overview.md#quorum)
		+ [A.2.6 STONITH](pcmk-ha-overview.md#stonith)
		+ [A.2.7 Các port sử dụng cho HA cluster](pcmk-ha-overview.md#others-concept)