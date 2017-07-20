# 6. Các ràng buộc resources trong pacemaker


____


# Mục lục

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
- [Các nội dung khác](#content-others)
____


# Nội dung


- ### <a name="location-constraints">6.1. Ràng buộc vị trí</a>

	- Ý nghĩa của ràng buộc này quy định resource có thể hoạt động trên những node nào. Ta có thể thực hiện cấu hình để xác định ràng buộc vị trí cho resource được phép hoạt động hay không hoạt động trên một node nào đó!

	- Để tạo ra một ràng buộc về vị trí cho phép resource hoạt động trên node nào đó, ta sử dụng câu lệnh:

			pcs constraint location resource_id prefers node_id

		trong đó:
			- resource_id: tên của resource
			- node_id: tên của node

	- Để tạo ra một ràng buộc về vị trí mà resource không được phép hoạt động, ta sử dụng câu lệnh:

			pcs constraint location resource_id avoids node_id

		trong đó:

			- resource_id: tên của resource
			- node_id: tên của node

	- Có hai hướng để cấu hình ràng buộc về vị trí cho các resources:

		+ `"Opt-In" Cluster`: Cấu hình Cluster mà mặc định các resource không thể hoạt động trên bất kỳ node nào đó. Sau đó ta sẽ khai báo resource có thể được hoạt động trên node nào. [Xem thêm](#opt-in)

		+ `"Opt-Out" Cluster`: Cấu hình Cluster mà mặc định các resource có thể chạy trên tất cả các node. Sau đó ta sẽ khai báo resource không được phép hoạt động trên node nào. [Xem thêm](#opt-out)

		+ Việc lựa chọn cấu hình Cluster theo hướng nào phụ thuộc vào ý tưởng cá nhân và cách mà ta tạo ra cluster. Nếu hầu hết các node đều có thể chạy resource thì việc lựa chọn hướng `Opt-Out` sẽ khiến cho việc cấu hình đơn giản hơn. Mặc khác, nếu các resource chỉ có thể chạy trên một tập hợp nhỏ các node trong cluster thì việc lựa chọn hướng  `Opt-In` sẽ khiến việc cấu hình đơn giản hơn.

- ### <a name="opt-in">6.1.1. Cấu hình một "Opt-In" Cluster</a>

	+ Để tạo ra một cấu hình `Opt-In` cluster, ta cần phải đặt lại giá trị `symmetric-cluster` để ngăn việc resource chạy được bất cứ trên node nào trong cluster bằng việc sử dụng câu lệnh:

			pcs property set symmetric-cluster=false

	+ Giả sử, mô hình triển khia cluster có 3 node theo phần [Cài đặt pacemaker](pacemaker-corosync-installing.md#block). Tiếp theo ta cần cấu hình cho phép resource chỉ được hoạt động trên node nào bằng việc thực hiện các câu lệnh sau:

			pcs constraint location Virtual_IP prefers lb01
			pcs constraint location Virtual_IP prefers lb03


			pcs constraint location Web_Cluster prefers lb02
			pcs constraint location Web_Cluster prefers lb03

		ý nghĩa: 

		+ Chỉ cho phép resource Virtual_IP hoạt động trên node lb01 và node lb03
		+ Chỉ cho phép resource Web_Cluster hoạt động trên node lb02 và node lb03
		+ Khi các node lb01, lb02 bị lỗi thì quá trình fail-over sẽ xảy ra - resource Virtual_IP, Web_Cluster sẽ được dịch chuyển sang node lb03

- ### <a name="opt-out">6.1.2. Cấu hình một "Opt-Out" Cluster</a>

	
- ### <a name="order-constraints">6.2. Ràng buộc về thứ tự</a>
- ### <a name="mand-order">6.2.1. Thứ tự cố định</a>
- ### <a name="advi-order">6.2.2. Thứ tự linh động</a>
- ### <a name="sets-order">6.2.3. Thứ tự tập hợp các resource</a>
- ### <a name="remove-order">6.2.4. Xóa bỏ resource từ các ràng buộc thứ tự</a>
- ### <a name="colocation-constraint">6.3. Ràng buộc colocation của resources</a>
- ### <a name="mand-place">6.3.1. Vị trí cố định</a>
- ### <a name="advi-place">6.3.2. Vị trí linh động</a>
- ### <a name="sets-place">6.3.3. Colocation các tập hợp resource</a>
- ### <a name="colocation-remove">6.3.4. Xóa bỏ ràng buộc colocation</a>
- ### <a name="display-constraints">6.4. Hiển thị cấu hình các ràng buộc</a>

____


# Các nội dung khác <a name="content-others"></a>

	Sẽ cập nhật sau