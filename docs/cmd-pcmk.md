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
		| pcs cluster | Đây là câu lệnh cho phép thực hiện cấu hình các tùy chọn và các node trong cluster. Xem [Tạo và quản lý Cluster](create-cluster-pcmk.md) để biết cách sử dụng câu lệnh |
		| pcs resource | Quản lý các resource trong cluster. Xem [Quản lý các resource](resource-pacemaker.md) để biết các dùng câu lệnh|
		| pcs constraint | Quản lý các ràng buộc của resource. Xem [Các ràng buộc resources trong pacemaker](constraint-pacemaker.md)|
		| pcs status | Xem thông tin, trạng thái của cluster |

____


# <a name="contents-other">Các nội dung khác</a>

- [3. Tạo và quản lý một cluster](docs/create-cluster-pcmk.md)
	- [3. 1  Tạo một cluster](docs/create-cluster-pcmk.md#create)
		- [3.1.1 Khởi động pacemaker](docs/create-cluster-pcmk.md#start)
		- [3.1.2 Xác thực các node tham gia vào cluster](docs/create-cluster-pcmk.md#authen)
		- [3.1.3 Cấu hình và khởi động các node trong cluster](docs/create-cluster-pcmk.md#cluster-nodes)
		- [3.1.4 Enable và Disable các dịch vụ cluster](docs/create-cluster-pcmk.md#ed-services)
	- [3.2 Quản lý các node trong cluster](docs/create-cluster-pcmk.md#man-node)
		- [3.2.1 Dừng các dịch vụ trong cluster](docs/create-cluster-pcmk.md#stop-node)
		- [3.2.2 Thêm node mới vào cluster](docs/create-cluster-pcmk.md#add-node)
		- [3.2.3 Xóa bỏ node trong cluster](docs/create-cluster-pcmk.md#rem-node)
	- [3.3 Xóa cấu hình cluster](docs/create-cluster-pcmk.md#rem-config)
	- [3.4 Hiển thị trạng thái cluster](docs/create-cluster-pcmk.md#disp-stat)