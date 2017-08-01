# Tổng quan về resource agents


___


# Mục lục

+ [Resource là gì?](#whatis)
+ [Cách liệt kê về các resource hiện có trên hệ thống](#list)
+ [Các nội dung khác](#others-content)


___

# Nội dung

+  <a name="whatis">Resource là gì?</a>

	- Để tạo một resource, chúng ta cần phải có các resource agents (RAs). Một resource agent giống như một kịch bản dùng để load dịch vụ đó được sử dụng trong  System-V runlevels. Nhưng một RAs chúng còn bao gồm có các tham số của cluster. RAs được cài đặt cùng với cluster và chia ra thành các lớp khác nhau:

		- lsb: LSB (viết tắt của Linux Standard Base) resource agents là một kịch bản khởi động System-V runlevels có thể khởi động từ cluster. Được cài đặt cùng với OS.

		- ocf: OCF (Open Cluster Framework) resource agents không giống như lsb resource agents có các tham số đặc biệt liên quan đến cluster bao gồm các tính chất thuồng được lưu trữ trong file cấu hình. Giữa ocf và lsb thì ta nên chọn ocf resource agents. Trong ocf resource agents chia ra thành các lớp "provider" như sau:

			+ heartbeat
			+ linbit
			+ lvm2
			+ ocfs2
			+ pacemaker

		- service: Được quản lý bởi system daemon (systemd) của hệ thống. Tránh sử dụng nếu một ocf thay thế đang tồn tại

		- stonith: Một resource agent dùng cho cơ chế STONITH

		
+ <a name="list">Cách liệt kê về các resource hiện có trên hệ thống</a>

	- Liệt kê ra các resource agents đi kèm cùng với cài đặt:

			pcs resource standards

	- Liệt kê ra các lớp provider trong ocf resource agents:

			pcs resource providers

	- Liệt kê ra các lựa chọn được cung cấp bởi standards resource và provider:

			pcs resource agents standards:providers

		ví dụ:

			pcs resource agents ocf:heartbeat
___

- # <a name="others-content">Các nội dung khác</a>

- [1. Cài đặt pacemaker](pcmk-pacemaker-corosync-installing.md)
	- [1.1 Môi trường cài đặt](pcmk-pacemaker-corosync-installing.md#envir)
	- [1.2 Mô hình hệ thống](pcmk-pacemaker-corosync-installing.md#block)
	- [1.3 IP Plan](pcmk-pacemaker-corosync-installing.md#ipPlan)
	- [1.4 Cài đặt nginx và modules](pcmk-pacemaker-corosync-installing.md#nginx)
	- [1.5 Kiểm tra cài đặt nginx](pcmk-pacemaker-corosync-installing.md#test)
	- [1.6 Cài đặt pacemaker và corosync để tạo cluster cho nginx](pcmk-pacemaker-corosync-installing.md#pacemaker)
	- [1.7 Cấu hình để thêm các resources vào Cluster](pcmk-pacemaker-corosync-installing.md#configCluster)
	- [1.8 Thêm resource NGINX để pacemaker quản lý.](pcmk-pacemaker-corosync-installing.md#addResources)
	- [1.9 Quản lý các resource với Web-GUI](pcmk-pacemaker-corosync-installing.md#webgui)