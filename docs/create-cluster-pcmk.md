# 3. Tạo và quản lý một cluster


____


# Mục lục

- [3. 1  Tạo một cluster](#create)
	- [3.1.1 Khởi động pacemaker](#start)
	- [3.1.2 Xác thực các node tham gia vào cluster](#authen)
	- [3.1.3 Cấu hình và khởi động các node trong cluster](#cluster-nodes)
	- [3.1.4 Enable và Disable cluster](#ed-services)
- [3.2 Quản lý các node trong cluster](#man-node)
	- [3.2.1 Dừng dịch vụ cluster trong các nodes](#stop-node)
	- [3.2.2 Thêm node mới vào cluster](#add-node)
	- [3.2.3 Xóa bỏ node trong cluster](#rem-node)
- [3.3 Cấp quyền cho user](#permit)
- [3.4 Xóa cấu hình cluster](#rem-config)
- [3.5 Hiển thị trạng thái cluster](#disp-stat)
- [Các nội dung khác](#contents-other)
____


# Nội dung


- ### <a name="create">3. 1  Tạo một cluster</a>
- #### <a name="start">3.1.1 Khởi động pacemaker</a>
	- Để khởi động dịch vụ pacemaker và cho phép tự khởi động cùng với OS. Ta chạy 2 câu lệnh sau:

			systemctl start pcsd
			systemctl enable pcsd

- #### <a name="authen">3.1.2 Xác thực các node tham gia vào cluster</a>

	- Trước khi tạo mới 1 cluster, ta cần kiểm tra kết nối tới các node sẽ tham gia hình hành lên cluster xem có được liên lạc với nhau hay không?. Giả sử, ta sẽ tạo ra một HA Cluster với 3 node như sau:

		| Tên node | Địa chỉ IP của node |
		| ------------- | ------------- |
		| lb01 | 10.10.10.8 |
		| lb02 | 10.10.10.9 |
		| lb03 | 10.10.10.10 |
		
	với nội dung file cấu hình `/etc/hosts` như sau:

			...
			10.10.10.8    lb01
			10.10.10.9    lb02
			10.10.10.10   lb03

	trước khi tạo mới 1 cluster, ta nên thêm thông tin các địa chỉ IP của từng host vào file `/etc/hosts` để đơn giản hơn cho việc cấu hình.

	- Tiếp theo, ta nên sử dụng một mật khẩu giống nhau cho user `hacluster` trên tất cả các node. Câu lệnh sử dụng để tạo xác thực liên lạc giữa các node có cú pháp như sau:

			pcs cluster auth [node] [...] [-u username] [-p password]

		trong đó:

			- username: phải là `hacluster`
			- password: là mật khẩu của user `hacluster`
			- node: có thể là địa chỉ ip hoặc tên của node tham gia trong cluster

	- Ví dụ, với 3 node `lb01`, `lb02`, `lb03` như đã nói ở trên, ta sử dụng câu lệnh sau để kiểm tra quá trình xác thực:

			pcs cluster auth lb01 lb02 lb03

		trong câu lệnh trên, bạn không cần phải khai báo ngay mật khẩu cho user `hacluster` vì sau đó hệ thống sẽ hiện lên một nhắc nhở yêu cầu bạn nhập mật khẩu cho user này. Kết quả: 

			[ root@127.0.0.1 ]#: pcs cluster auth lb01 lb02 lb03
			Username: hacluster
			Password:
		
		nhập đúng password cho user `hacluster` ta nhận được thông báo:

			lb01: Authorized
			lb02: Authorized
			lb03: Authorized

		nếu tất cả các node đều được thông báo `Authorized`. Ta mới tiến hành cấu hình một cluster.

- #### <a name="cluster-nodes">3.1.3 Cấu hình và khởi động các node trong cluster</a>

	- Để tiến hành cấu hình cho một cluster. Ta sử dụng câu lệnh:

			pcs cluster setup [--start] [--local] --name cluster_name node1 [node2] [...]

		trong đó:

			- cluster_name: là tên của cluster sẽ được tạo ra
			- node1 [node2] [...]: là dãy tên các node tham gia vào cluster.

		ví dụ:

			pcs cluster setup --name ha_cluster lb01 lb02 lb03 --start

- #### <a name="ed-services">3.1.4 Enable và Disable cluster</a>

	- Để cho phép cluster khởi động cùng với hệ thống, sử dụng câu lệnh:

			pcs cluster enable --all

	- Hủy bỏ, không cho phép cluster khởi động cùng hệ thống, sử dụng câu lệnh:

			pcs cluster disable --all

- ### <a name="man-node">3.2 Quản lý các node trong cluster</a>
- #### <a name="stop-node">3.2.1 Dừng dịch vụ cluster trong các nodes</a>
	
	- Để dừng hoạt động của một node trong cluster ta sử dụng câu lệnh:

			pcs cluster stop node_name

		trong đó:

			- node_name: là tên của node mà bạn muốn dừng hoạt động của nó trong cluster

		hoặc:

			pcs cluster stop --all

		để dừng hoạt động của tất cả các node trong cluster

- #### <a name="add-node">3.2.2 Thêm node mới vào cluster</a>

	- Để thêm mới một node vào trong cluster đã tồn tại. Ta thực hiện sử dụng câu lệnh sau trên một node đã nằm trong cluster ấy:
			
			pcs cluster auth node_name

			pcs cluster node add node_name --start

		trong đó:

			node_name là tên của node cần thêm vào cluster


- #### <a name="rem-node">3.2.3 Xóa bỏ node trong cluster</a>

	- Để xóa bảo một node đã tồn tại trong cluster. Ta sử dụng câu lệnh sau trên một node đã nằm trong cluster:

			pcs cluster node remove node_name

		trong đó:

			node_name: là tên của node cần xóa khỏi cluster

- ### <a name="rem-config">3.3 Xóa cấu hình cluster</a>

	- Khi bạn không muốn sử dụng các node này như một cluster. Ta có thể thực hiện xóa cluster này đi bằng việc thực hiện:

		+ Bước 1: Dừng dịch vụ cluster trên các node

				pcs cluster stop --all

		+ Bước 2: Xóa vĩnh viễn dịch vụ trên tất cả các node

				pcs cluster destroy --all


- ### <a name="disp-stat">3.4 Hiển thị trạng thái cluster</a>

	- Để hiển thị trạng thái của cluster. Sử dụng câu lệnh sau trên node đã nằm trong cluster.

			pcs status

____


# <a name="contents-other">Các nội dung khác</a>

- [4. Tìm hiểu về cách quản lý các resource trong pacemaker](docs/resource-pacemaker.md)
	- [4.1. Tạo một resource](docs/resource-pacemaker.md#create)
	- [4.2. Các tính chất của resource](docs/resource-pacemaker.md#properties)
	- [4.3. Các tham số cụ thể về resource](docs/resource-pacemaker.md#parameter)
	- [4.4. Các tùy chọn cho resource](docs/resource-pacemaker.md#options)
	- [4.5. Các nhóm resource](docs/resource-pacemaker.md#groups)
		- [4.5.1. Các tùy chọn cho nhóm resource](docs/resource-pacemaker.md#options-group)
		- [4.5.2. Các gắn kết liên quan tới nhóm](docs/resource-pacemaker.md#stickness)
	- [4.6. Sự vận hành các resource](docs/resource-pacemaker.md#operations)
	- [4.7. Hiển thị cấu hình của resource](/resource-pacemaker.md#displaydocs-config)
	- [4.8. Chỉnh sửa các tham số cụ thể của resource](/resource-pacemaker.md#modifieddocs-parameters)
	- [4.9 Kích hoạt, vô hiệu hóa nhóm các resource](/resource-pacemaker.md#enablingdocs-disabling)
	- [4.10. Xóa các cảnh báo của các resource](docs/resource-pacemaker.md#cleanup)