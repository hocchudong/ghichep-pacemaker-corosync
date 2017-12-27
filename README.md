# ghichep-pacemaker-corosync
Ghi chép về pacemaker corosync


___


# Nội dung

## Giới thiệu

____

## Phần 1: Lý thuyết

- [A. Tổng quan về High Availability](docs/pcmk-ha-overview.md)
	+ [A.1 Giới thiệu về High Availability](docs/pcmk-ha-overview.md#whatis-ha)
	+ [A.2 Các khái niệm, thuật ngữ cần biết trong HA](docs/pcmk-ha-overview.md#concepts)
		+ [A.2.1 Cluster](docs/pcmk-ha-overview.md#whatis-cl)
		+ [A.2.2 Resource](docs/pcmk-ha-overview.md#resource)
		+ [A.2.3 Pacemaker](docs/pcmk-ha-overview.md#pacemaker)
		+ [A.2.4 Corosync](docs/pcmk-ha-overview.md#corosync)
		+ [A.2.5 Quorum](docs/pcmk-ha-overview.md#quorum)
		+ [A.2.6 STONITH](docs/pcmk-ha-overview.md#stonith)
		+ [A.2.7 Các port sử dụng cho HA cluster](docs/pcmk-ha-overview.md#others-concept)

- [B. Tổng quan về pacemaker](docs/pcmk-pacemaker-overview.md)
	- [B.1 Tổng quan về quorum](docs/pcmk-quorum-overview.md)
	- [B.2 Tổng quan về STONITH/ fencing](docs/pcmk-fencing-overview.md)
	- [B.3 Tổng quan về resource](docs/pcmk-resource-overview.md)

- [1. Cài đặt pacemaker](docs/pcmk-pacemaker-corosync-installing.md)
	- [1.1 Môi trường cài đặt](docs/pcmk-pacemaker-corosync-installing.md#envir)
	- [1.2 Mô hình hệ thống](docs/pcmk-pacemaker-corosync-installing.md#block)
	- [1.3 IP Plan](docs/pcmk-pacemaker-corosync-installing.md#ipPlan)
	- [1.4 Cài đặt nginx và modules](docs/pcmk-pacemaker-corosync-installing.md#nginx)
	- [1.5 Kiểm tra cài đặt nginx](docs/pcmk-pacemaker-corosync-installing.md#test)
	- [1.6 Cài đặt pacemaker và corosync để tạo cluster cho nginx](docs/pcmk-pacemaker-corosync-installing.md#pacemaker)
	- [1.7 Cấu hình để thêm các resources vào Cluster](docs/pcmk-pacemaker-corosync-installing.md#configCluster)
	- [1.8 Thêm resource NGINX để pacemaker quản lý.](docs/pcmk-pacemaker-corosync-installing.md#addResources)
	- [1.9 Quản lý các resource với Web-GUI](docs/pcmk-pacemaker-corosync-installing.md#webgui)

- [2. Các câu lệnh của pacemaker](docs/pcmk-cmd.md)

- [3. Tạo và quản lý một cluster](docs/pcmk-create-cluster.md)
	- [3. 1  Tạo một cluster](docs/pcmk-create-cluster.md#create)
		- [3.1.1 Khởi động pacemaker](docs/pcmk-create-cluster.md#start)
		- [3.1.2 Xác thực các node tham gia vào cluster](docs/pcmk-create-cluster.md#authen)
		- [3.1.3 Cấu hình và khởi động các node trong cluster](docs/pcmk-create-cluster.md#cluster-nodes)
		- [3.1.4 Enable và Disable các dịch vụ cluster](docs/pcmk-create-cluster.md#ed-services)
	- [3.2 Quản lý các node trong cluster](docs/pcmk-create-cluster.md#man-node)
		- [3.2.1 Dừng các dịch vụ trong cluster](docs/pcmk-create-cluster.md#stop-node)
		- [3.2.2 Thêm node mới vào cluster](docs/pcmk-create-cluster.md#add-node)
		- [3.2.3 Xóa bỏ node trong cluster](docs/pcmk-create-cluster.md#rem-node)
	- [3.3 Xóa cấu hình cluster](docs/pcmk-create-cluster.md#rem-config)
	- [3.4 Hiển thị trạng thái cluster](docs/pcmk-create-cluster.md#disp-stat)

- [4. Tìm hiểu về cách quản lý các resource trong pacemaker](docs/pcmk-resource.md)
	- [4.1. Tạo một resource](docs/pcmk-resource.md#create)
	- [4.2. Các tính chất của resource](docs/pcmk-resource.md#properties)
	- [4.3. Các tham số cụ thể về resource](docs/pcmk-resource.md#parameter)
	- [4.4. Các tùy chọn cho resource](docs/pcmk-resource.md#options)
	- [4.5. Các nhóm resource](docs/pcmk-resource.md#groups)
		- [4.5.1. Các tùy chọn cho nhóm resource](docs/pcmk-resource.md#options-group)
		- [4.5.2. Các gắn kết liên quan tới nhóm](docs/pcmk-resource.md#stickness)
	- [4.6. Sự vận hành các resource](docs/pcmk-resource.md#operations)
	- [4.7. Hiển thị cấu hình của resource](pcmk-/resource.md#displaydocs-config)
	- [4.8. Chỉnh sửa các tham số cụ thể của resource](pcmk-/resource.md#modifieddocs-parameters)
	- [4.9 Kích hoạt, vô hiệu hóa nhóm các resource](pcmk-/resource.md#enablingdocs-disabling)
	- [4.10. Xóa các cảnh báo của các resource](docs/pcmk-resource.md#cleanup)

- [5. Các ràng buộc trong pacemaker cho resource](docs/pcmk-constraint.md)
	- [5.1. Ràng buộc vị trí](docs/pcmk-constraint.md#location-constraints)
		- [5.1.1. Cấu hình một "Opt-In" Cluster](docs/pcmk-constraint.md#opt-in)
		- [5.1.2. Cấu hình một "Opt-Out" Cluster](docs/pcmk-constraint.md#opt-out)
	- [5.2. Ràng buộc về thứ tự](docs/pcmk-constraint.md#order-constraints)
		- [5.2.1. Thứ tự bắt buộc](docs/pcmk-constraint.md#mand-order)
		- [5.2.2. Thứ tự không bắt buộc](docs/pcmk-constraint.md#advi-order)
		- [5.2.3. Thứ tự tập hợp các resource](docs/pcmk-constraint.md#sets-order)
		- [5.2.4. Xóa bỏ resource từ các ràng buộc thứ tự](docs/pcmk-constraint.md#remove-order)
	- [5.3. Ràng buộc colocation của resources](docs/pcmk-constraint.md#colocation-constraint)
		- [5.3.1. Vị trí cố định](docs/pcmk-constraint.md#mand-place)
		- [5.3.2. Vị trí linh động](docs/pcmk-constraint.md#advi-place)
		- [5.3.3. Colocation các tập hợp resource](docs/pcmk-constraint.md#sets-place)
		- [5.3.4. Xóa bỏ ràng buộc colocation](docs/pcmk-constraint.md#colocation-remove)
	- [5.4. Hiển thị cấu hình các ràng buộc](docs/pcmk-constraint.md#display-constraints)
	

## Phần 2: Thực hành

- [E. Thực hiện cấu hình tạo cluster với chế độ active/active](docs/pcmk-master-resource.md)
	- [E.1 Cài đặt pacemaker và tạo nginx.](docs/pcmk-master-resource.md#install)
	- [E.2 Cấu hình resource](docs/pcmk-master-resource.md#configure)
		- [E.2.1 Sử dụng câu lệnh](docs/pcmk-master-resource.md#cmd)
		- [E.2.2 Sử dụng giao diện website](docs/pcmk-master-resource.md#gui)
		- [E.2.3 Khởi động lại dịch vụ trong cluster](docs/pcmk-master-resource.md#star)

- [F. Cấu hình NFS trên 1 node chia sẻ dữ liệu cho các KVM trong Cluster](docs/pcmk-shared-storage-failover.md)
	- [F.1 Yêu cầu giải quyết](docs/pcmk-shared-storage-failover.md#issue)
	- [F.2 Mô hình triển khai](docs/pcmk-shared-storage-failover.md#models)
	- [F.3 Cài đặt KVM](docs/pcmk-shared-storage-failover.md#kvm-settings)
	- [F.4 Triển khai, cấu hình NFS](docs/pcmk-shared-storage-failover.md#nfs)
	- [F.5 Tạo resources quản lý KVM](docs/pcmk-shared-storage-failover.md#resource)
	- [F.6 Kiểm tra kết quả](docs/pcmk-shared-storage-failover.md#stat)


- ## G. Các tài liệu mở rộng liên quan đến Pacemaker - Corosync
	- [1. Sao chép dữ liệu lưu trữ sử dụng DRBD - Distributed Replicated Block Device kết hợp sử dụng Pacemaker.](docs/pcmk-drbd.md)
		- [1.1 Yêu cầu giải quyết bài toán](docs/pcmk-drbd.md#issue)
		- [1.2 Mô hình triển khai và các yêu cầu](docs/pcmk-drbd.md#models)
		- [1.3 Tiến hành cài đặt](docs/pcmk-drbd.md#install)
			- [1.3.1 Cài đặt httpd - Web Server](docs/pcmk-drbd.md#httpd)
			- [1.3.2 Tạo, format ổ đĩa cho việc đồng bộ dữ liệu](docs/pcmk-drbd.md#format)
			- [1.3.3 Cài đặt DRBD và cấu hình](docs/pcmk-drbd.md#install-drbd)
			- [1.3.4 Cài đặt pacemaker và corosync](docs/pcmk-drbd.md#install-pcsd)
			- [1.3.5 Tạo cluster, thêm các resource và ràng buộc sử dụng pacemaker](docs/pcmk-drbd.md#pcsd-resource)
		- [1.4 Kiểm tra kết quả](docs/pcmk-drbd.md#test)
		
	- [2. Tích hợp ZFS với Pacemaker và Corosync](docs/pcmk-zfs.md)
		- [1. ZFS là gì?](docs/pcmk-zfs.md#what-is)
		- [2. Storage pools](docs/pcmk-zfs.mds-pools)
		- [3. Toàn vẹn dữ liệu](docs/pcmk-zfs.md#di)
		- [4. Snapshot](docs/pcmk-zfs.md#ss)
		- [5. Tích hợp ZFS với Pacemaker và Corosync](docs/pcmk-zfs.md#integrate)
		- [6. Kiểm tra kết quả](docs/pcmk-zfs.md#checksummed)
		
# Tài liệu tham khảo:

- [High Availability Add-on](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/High_Availability_Add-On_Overview/ch-introduction-HAAO.html)

- [Cluster Labs](http://clusterlabs.org/doc/en-US/Pacemaker/1.0/html/Pacemaker_Explained/index.html)
