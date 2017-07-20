# ghichep-pacemaker-corosync
Ghi chép về pacemaker corosync


___


# Nội dung

- [Tổng quan về High Availability](docs/ha-overview.md)
- [Tổng quan về pacemaker](docs/pacemaker-overview.md)
	- [Tổng quan về quorum](docs/quorum-overview.md)
	- [Tổng quan về STONITH/ fencing](docs/fencing-overview.md)
	- [Tổng quan về resource](docs/resource-overview.md)
- [1. Cài đặt pacemaker](docs/pacemaker-corosync-installing.md)
	- [1.1 Môi trường cài đặt](#envir)
	- [1.2 Mô hình hệ thống](#block)
	- [1.3 IP Plan](#ipPlan)
	- [1.4 Cài đặt nginx và modules](#nginx)
	- [1.5 Kiểm tra cài đặt nginx](#test)
	- [1.6 Cài đặt pacemaker và corosync để tạo cluster cho nginx](#pacemaker)
	- [1.7 Cấu hình để thêm các resources vào Cluster](#configCluster)
	- [1.8 Thêm resource NGINX để pacemaker quản lý.](#addResources)
- [2. Các câu lệnh của pacemaker](#)
	Sẽ cập nhật sau.
- [3. Tạo và quản lý một cluster](#)
	Sẽ cập nhật sau
- [4. Fence - Cấu hình STONITH](#)
	Sẽ cập nhật sau
- [5. Tìm hiểu về cách quản lý các resource trong pacemaker](docs/resource-pacemaker.md)
	- [5.1. Tạo một resource](#create)
	- [5.2. Các tính chất của resource](#properties)
	- [5.3. Các tham số cụ thể về resource](#parameter)
	- [5.4. Các tùy chọn cho resource](#options)
	- [5.5. Các nhóm resource](#groups)
		- [5.5.1. Các tùy chọn cho nhóm resource](#options-group)
		- [5.5.2. Các gắn kết liên quan tới nhóm](#stickness)
	- [5.6. Sự vận hành các resource](#operations)
	- [5.7. Hiển thị cấu hình của resource](#display-config)
	- [5.8. Chỉnh sửa các tham số cụ thể của resource](#modified-parameters)
	- [5.9 Kích hoạt, vô hiệu hóa nhóm các resource](#enabling-disabling)
	- [5.10. Xóa các cảnh báo của các resource](#cleanup)
- [6. Các ràng buộc trong pacemaker cho resource](docs/constraint-pacemaker.md)
	- [6.1. Ràng buộc vị trí](#location-constraints)
		- [6.1.1. Cấu hình một "Opt-In" Cluster](#opt-in)
		- [6.1.2. Cấu hình một "Opt-Out" Cluster](#opt-out)
	- [6.2. Ràng buộc về thứ tự](#order-constraints)
		- [6.2.1. Thứ tự cố định](#mand-order)
		- [6.2.2. Thứ tự linh động](#advi-order)
		- [6.2.3. Thứ tự tập hợp các resource](#sets-order)
		- [6.2.4. Xóa bỏ resource từ các ràng buộc thứ tự](#remove-order)
	- [6.3. Ràng buộc colocation của resources](#colocation-constraint)
	- [6.3.1. Vị trí cố định](#mand-place)
	- [6.3.2. Vị trí linh động](#advi-place)
	- [6.3.3. Colocation các tập hợp resource](#sets-place)
	- [6.3.4. Xóa bỏ ràng buộc colocation](#colocation-remove)
	- [6.4. Hiển thị cấu hình các ràng buộc](#display-constraints)

# Tài liệu tham khảo:

- [High Availability Add-on](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/High_Availability_Add-On_Overview/ch-introduction-HAAO.html)

- [Cluster Labs](http://clusterlabs.org/doc/en-US/Pacemaker/1.0/html/Pacemaker_Explained/index.html)
