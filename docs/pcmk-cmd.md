# 2. Các câu lệnh của pacemaker


____


# Mục lục

- [Các câu lệnh pcs](#cmd-pcs)
- [Các nội dung khác](#contents-other)
____


# Nội dung


- ### <a name="cmd-pcs">2.1 Câu lệnh pcs</a>

	- pacemaker cung cấp đầy đủ các câu lệnh cho phép người dùng tương tác với cluster. Tử quản lý các node, resource, các ràng buộc ... liên quan đến cluster đều được pacemaker cung cấp. Chung được chia thành các nhóm sau:

		| Câu lệnh | Mô tả |
		| ------------- | ------------- |
		| pcs cluster | Đây là câu lệnh cho phép thực hiện cấu hình các tùy chọn và các node trong cluster. Xem [Tạo và quản lý Cluster](pcmk-create-cluster.md) để biết cách sử dụng câu lệnh |
		| pcs resource | Quản lý các resource trong cluster. Xem [Quản lý các resource](pcmk-resource.md) để biết cách dùng câu lệnh|
		| pcs constraint | Quản lý các ràng buộc của resource. Xem [Các ràng buộc resources trong pacemaker](pcmk-constraint.md)|
		| pcs status | Xem thông tin, trạng thái của cluster |
		| pcs property | Thiết lập các giá trị cho chính sách PEengine. Để biết rõ về các giá trị cũng như chức năng của các giá trị. Chúng ta sử dụng câu lệnh `man pengine` |
____


# <a name="contents-other">Các nội dung khác</a>

- [3. Tạo và quản lý một cluster](pcmk-create-cluster.md)
	- [3. 1  Tạo một cluster](pcmk-create-cluster.md#create)
		- [3.1.1 Khởi động pacemaker](pcmk-create-cluster.md#start)
		- [3.1.2 Xác thực các node tham gia vào cluster](pcmk-create-cluster.md#authen)
		- [3.1.3 Cấu hình và khởi động các node trong cluster](pcmk-create-cluster.md#cluster-nodes)
		- [3.1.4 Enable và Disable các dịch vụ cluster](pcmk-create-cluster.md#ed-services)
	- [3.2 Quản lý các node trong cluster](pcmk-create-cluster.md#man-node)
		- [3.2.1 Dừng các dịch vụ trong cluster](pcmk-create-cluster.md#stop-node)
		- [3.2.2 Thêm node mới vào cluster](pcmk-create-cluster.md#add-node)
		- [3.2.3 Xóa bỏ node trong cluster](pcmk-create-cluster.md#rem-node)
	- [3.3 Xóa cấu hình cluster](pcmk-create-cluster.md#rem-config)
	- [3.4 Hiển thị trạng thái cluster](pcmk-create-cluster.md#disp-stat)