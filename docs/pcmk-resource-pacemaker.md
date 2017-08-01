# 4. Tìm hiểu về cách quản lý các resource trong pacemaker

____


# Mục lục

- [4.1. Tạo một resource](#create)
- [4.2. Các tính chất của resource](#properties)
- [4.3. Các tham số cụ thể về resource](#parameter)
- [4.4. Các tùy chọn cho resource](#options)
- [4.5. Các nhóm resource](#groups)
	- [4.5.1. Các tùy chọn cho nhóm resource](#options-group)
	- [4.5.2. Các gắn kết liên quan tới nhóm](#stickness)
- [4.6. Sự vận hành các resource](#operations)
- [4.7. Hiển thị cấu hình của resource](#display-config)
- [4.8. Chỉnh sửa các tham số cụ thể của resource](#modified-parameters)
- [4.9 Kích hoạt, vô hiệu hóa nhóm các resource](#enabling-disabling)
- [4.10. Xóa các cảnh báo của các resource](#cleanup)
- [Các nội dung khác](#content-others)
____


# Nội dung


- ### <a name="create">4.1. Tạo một resource</a>
	
	+ Để tạo mới một resource trong cluster, ta sử dụng cú pháp câu lệnh như sau:

			pcs resource create	resource_id(name) standard:provider:type|type [resource options]

		ví dụ:
		Trong phần [overview](pacemaker-corosync-installing.md), ta đã gặp câu lệnh sau:

			pcs resource create Virtual_IP ocf:heartbeat:IPaddr2 ip=172.16.69.254 cidr_netmask=24 op monitor interval=30s

		ý nghĩa:
		
			- pcs resource create: yêu cầu gọi chức năng của câu lệnh
			- Virtual_IP: tên của resource hay resource_id
			- ocf:heartbeat:IPaddr2: khai báo kiểu resource agent.
			    Xem thêm tại [Resource Overview](resource-overview.md)
			- ip=172.16.69.254, cidr_netmask=24: các giá trị của resource.
			- op monitor interval=30s: Khai báo các tùy chọn cho resource.
				Xem thêm tại [Giám sát resource](#monitoring-resource)
		
		Việc tạo các resource được gán giá trị mặc định cho `standard` là `ocf` và `provider` là `heartbeat`. Thế nên ta vẫn có thể sự dụng câu lệnh sau để tạo mới một resource. Ví dụ:

			pcs resource create Virtual_IP IPaddr2 ip=172.16.69.254 cidr_netmask=24 op monitor interval=30s
		
		Sau khi tạo mới một resource, nó ngay lập tức sẽ được hoạt động.

	+ Để xóa đi một resource, ta sử dụng cú pháp câu lệnh như sau:

			pcs resource delete resource_id

		ví dụ:

			pcs resource delete Virtual_IP

		câu lệnh trên sẽ xóa đi resource có tên hay resource_id là Virtual_IP.

- ### <a name="properties">4.2. Các tính chất của resource</a>

	- Các tính chất quy định của một resource nhắm thông báo cho cluster rằng kịch bản (resource agents) nào sẽ được sử dụng cho resource. Bao gồm các giá trị sau:

		| Giá trị | Mô tả |
		| ------------- | ------------- |
		| resource_id | Tên của resource |
		| standard | Tiêu chuẩn của kịch bản (resource agents) tuân thủ theo |
		| provider | Khai báo lớp của resource agents (nhà cung cấp kịch bản này) |
		| type | Tên của resource agents muốn sử dụng được cung cấp bởi provider |
		
	- Để liệt kê ra danh sách các resource, ta sử dụng câu lệnh:

			pcs resource list

		xem thêm tại [Resource Overview](resource-overview.md#list)

- ### <a name="parameter">4.3. Các tham số cụ thể về resource</a>

	- Để biết được các tham số cụ thể của resource thuộc một kiểu nào đó, ta sử dụng câu lệnh như sau:

			pcs resource describe resource_type

		ví dụ:

			pcs resource describe nginx

		kết quả nhận được tương tự như sau:
	
			ocf:heartbeat:nginx - Manages an Nginx web/proxy server instance

			This is the resource agent for the Nginx web/proxy server.
			This resource agent does not monitor POP or IMAP servers, as
			we don't know how to determine meaningful status for them.

			The start operation ends with a loop in which monitor is
			repeatedly called to make sure that the server started and that
			it is operational. Hence, if the monitor operation does not
			succeed within the start operation timeout, the nginx resource
			will end with an error status.

			The default monitor operation will verify that nginx is running.

			...	


- ### <a name="options">4.4. Các tùy chọn cho resource</a>

	- Ngoài các tham số cụ thể cho resource. Ta còn có thể thiết lập thêm các giá trị tùy chọn cho resource theo các giá trị cho giống như bảng sau:

		| Meta options | Default | Mô tả |
		| ------------- | ------------- | ------------- |
		| priority | 0 | Nếu không phải tất cả các tài nguyên đều có thể hoạt động, cluster sẽ dừng các resource có độ ưu tiên thấp để giữ lại các resource có độ ưu tiên cao đang hoạt động |
		| target-role | Started | Quy định việc cố gắng giữ resource trong node nào đó. Bao gồm các giá trị: <br> <ul><li>Stopped: Buộc resource phải dừng hoạt động</li><li>Started: Cho phép resource sẽ được khởi động</li><li>Master: Cho phép resource sẽ được khởi động nếu phù hợp với node nào đó</li></ul>|
		| is-managed | true | Là cluster cho phép khởi động hoặc dừng resource. Giá trị cho phép: true, false |
		| resource-stickiness | 0 | Giá trị thể hiện có bao nhiêu resource được chỉ định ở tại nơi mà resource này đang hoạt động |
		| migration-threshold | INFINITY(disabled) | Có bao nhiêu lỗi có thể xảy ra cho resource này trong một node trước khi node này được xác định là node không có đủ điều khiện để lưu trữ resource |
		| multiple-active | stop_start | Quy định những gì mà cluster sẽ thực hiện khi phát hiện một resource đang chạy đồng thời trên nhiều node khác nhau. Các giá trị cho phép như sau: <br> <ul><li>block - quy định resource không được quản lý. Sẽ tạm dừng hoạt động resource. Đưa ra cảnh báo </li><li>stop_only: Dừng tất cả các trường hợt hoạt động</li><li>stop_start: Dừng tất cả các trường hợp hoạt động và thử khởi động lại</li></ul> |

	- Để thay đổi một giá trị mặc định của resource, ta sử dụng câu lệnh sau:

		pcs resource defaults resource-stickiness=69

	- Có thể thiết lập giá trị cho các meta-options này khi đã tạo hoặc tạo mới một resource bằng 1 trong 2 cú pháp câu lệnh sau:

		+ Khi tạo mới một resource:

				pcs create resource_id type value meta meta_options

			ví dụ:

				pcs resource create IPaddr2 ip=172.16.69.254 cidr_netmask=24 meta resource-stickiness=69

		+ Khi đã tạo resource đó rồi thì ta dùng câu lệnh sau:

				pcs resource meta resource_id meta_options

			ví dụ:

				pcs resource meta Virtual_IP resource-stickiness=69

- ### <a name="groups">4.5. Các nhóm resource</a>

	- Một điều quan trọng và phổ biến trong cluster đó là một tập các resource cần được cài đặt nằm ở cùng một vị trí trên một node nào đó và được khởi động một cách tuần tự và việc tắt đi sẽ ngược lại. Để đơn giản hóa cho khai báo cấu hình này, khái niệm nhóm (group) trong pacemaker xuất hiện.

	- Bạn có thể tạo ra một resource group bằng câu lệnh khai báo các resource nằm bên trong group sẽ tạo. Nếu như một group mà bạn chuẩn bị tạo ra đã thự sự tồn tại trên hệ thống thì các resource sẽ được tiếp tục thêm vào group đã tồn tại đó. Ngược lại, thì một group mới sẽ được tạo ra. Cú pháp của câu lệnh tạo group này rất quan trọng bởi việc thứ tự khởi động các resource trong group phụ thuộc vào việc bạn viết câu lệnh này như thế nào. Đơn giản sẽ là, việc khai báo resource nào trước trong câu lệnh thì nó sẽ được khởi động trước và việc dừng lại sẽ hoạt động theo thứ tự ngược lại.

	- Cú pháp của câu lệnh như sau:

			pcs resource group add group_name resource_id ... resource_id_n

		trong đó:

			- group_name: Là tên group bạn sẽ định tạo ra
			- resource_id: Là tên của resource, resource này sẽ được khởi động đầu tiên ...
			- resource_id_n: Là rên của resource thứ n mà bạn muốn thêm vào group


	- Bạn cũng có thể thực hiện thêm resource vào một group đã tồn tại khi tạo mới resource đó theo cú pháp:

			pcs resource create resource_id type --group group_name

		trong đó:

			- group_name: là tên group bạn muốn thêm resource chuẩn bị tạo vào đó.

	- Để gỡ bỏ một resource trong group, ta sử dụng câu lệnh sau:

			pcs resource group remove group_name resource_id

		##### Lưu ý:

			- Nếu resource_id không tồn tại trong group_name thì group_name này sẽ bị xóa bỏ.

	- Ví dụ:

			pcs resource group add Web Virtual_IP Web_Cluster

		câu lệnh trên sẽ tạo ra một resource group có tên là `Web`. Và cách thức hoạt động cụ thể như sau:

		- Resource có tên là `Virtual_IP` sẽ khởi động trước sau đó mới khởi động `Web_Cluster`
		- Resource có tên là `Web_Cluster` sẽ dừng hoạt động trước sau đó mới dừng hoạt động của `Virtual_IP`

		Vì vậy, nếu:

		- `Virtual_IP` không thể chạy ở bất cứ trên node nào đó thì `Web_Cluster` cũng không thể hoạt động
		- `Web_Cluster` không thể hoạt động ở bất cứ đâu thì `Virtual_IP` chưa chắc đã không hoạt động được

	- ### <a name="options-group">4.5.1 Các tùy chọn cho nhóm resource</a>

		- Các tùy chọn meta-options cho resource group được kế thừa từ các tùy chọn meta-options cho resource với các giá trị:

			- priority
			- target-role
			- is-managed

		xem thêm tại [Các tùy chọn cho resource](#options)

	- ### <a name="stickness">4.5.2 Các gắn kết liên quan tới nhóm</a>

		- Sự gắn kết, đo đạc có bao nhiêu resource muốn tồn tại trên node đều phụ thuộc vào nhóm mà nó nằm trong đó. Mỗi hoạt động của resource trong nhóm sẽ góp phần làm tăng giá trị liên kết cho toàn bộ nhóm. Vì vậy, nếu độ tin cậy (resource-stickiness) mặc định là 100 và mỗi nhóm có 7 thành viên (resource) mà có 5 resource còn đang hoạt động thì độ gắn kết (resource-stickiness) của toàn nhóm sẽ là 500.

- ### <a name="operations">4.6 Sự vận hành các resource</a>

	- Để đảm bảo các resource hoạt động một cách ổn định nhất, ta có thể thêm các hoạt động giám sát tới một định nghĩa của resource. Nếu ta không khai báo hoạt động giám sát cho một resource, mặc định thì nó sẽ vẫn được tạo ra với một khoảng thời gian lặp lại giám sát được quy định bởi resource agents. Nếu resource agents không cung cấp khoảng thời gian giám sát mặc định thì hoạnt động giám sát được tạo ra với khoảng thời gian là 60s (giây).

	- Các thuộc tính của hoạt động giám sát bao gồm:

		| Thuộc tính | Mô tả |
		| ------------- | ------------- |
		| id | Giá trị đại diện và là duy nhất cho hành động giám sát. Nó được hệ thống gán khi thực hiện cấu hình hoạt động giám sát |
		| name | Hành động thực thi. Bao gồm `monitor`, `start`, `stop` |
		| interval | Quy định khoảng thời gian (tính theo giây) thực thi hoạt động giám sát. Mặc định là 0s |
		| timeout | Quy định thời gian chờ trước khi quyết đinh hoạt động giám sát bị lỗi. |
		| on-fail | Hành động thực hiện thi mà hoạt động giám sát luôn bị thất bại. Với các giá trị cho phép như sau: <br><ul><li>ignore: Phớt lờ việt hoạt động bị lỗi. Nói cách khác là: coi như không có chuyện gì</li><li>block: Không thực hiện thêm bất kỳ hoạt động nào khác trên hệ thống</li><li>stop: Dừng resource này lại và không khởi động nó trên bất kỳ node nào khác</li><li>restart: Thực hiện khởi động lại resource</li><li>fence: STONITH trên node mà resource đó bị lỗi</li><li>standby: Di chuyển tất cả các resource ra khỏi node mà có resource bị lỗi</li></ul> |
		| enable | Nếu được thiết lập là false thì hoạt động giám sát sẽ coi nó như chưa hề tồn tại. Có thể có giá trị true hoặc false |
		
	- Ví dụ, trong phần [Cài đặt pacmaker - corosync](#addResources), ta có thực hiện tạo ra một resource khi tạo mới nó như sau:

			pcs resource create Virtual_IP IPaddr2 ip=172.16.69.254 cidr_netmask=24 op monitor interval=30s

		tuy nhiên, ta cũng có thể thêm các tùy chọn này sau khi đã tạo resource bằng việc dùng câu lệnh:

			pcs resource op add resource_id operation_actions operation_properties

		trong đó:

		- operation_actions: là các giá trị: `monitor`, `start`, `stop`
		- operation_properties: là các giá trị được cho theo bảng bên trên, ví dụ: interval, fence, ...

		tương tự, để gỡ các hoạt động giám sát này, ta dùng câu lệnh:

			pcs resource op remove resource_id operation_actions operation_properties

		và có thể thiết lập các biến đó với giá trị mặc định mà mình đã quy định:

			pcs resource op defaults [options]

		ví dụ:

			pcs resource op defaults timeout=240s

- ### <a name="display-config">4.7 Hiển thị cấu hình của resource</a>

	- Để liệt kê ra danh sách tất các các resource đã cấu hình, ta sử dụng câu lệnh sau:

			pcs resource show

		kết quả nhận được tương tự như sau:

			 Virtual_IP     (ocf::heartbeat:IPaddr2):       Started 
			 Web_Cluster    (ocf::heartbeat:nginx): Started 

		hoặc dùng câu lệnh sau để hiện thị tất cả những gì liên quan tới resource:

			pcs resource show --full

		kết quả nhận được tương tự như sau:

			Resource: Virtual_IP (class=ocf provider=heartbeat type=IPaddr2)
			  Attributes: ip=172.16.69.254 cidr_netmask=24
			  Operations: start interval=0s timeout=20s (Virtual_IP-start-interval-0s)
			              stop interval=0s timeout=20s (Virtual_IP-stop-interval-0s)
			              monitor interval=30s (Virtual_IP-monitor-interval-30s)
			Resource: Web_Cluster (class=ocf provider=heartbeat type=nginx)
			  Attributes: configfile=/etc/nginx/nginx.conf
			  Operations: start interval=0s timeout=60s (Web_Cluster-start-interval-0s)
			              stop interval=0s timeout=60s (Web_Cluster-stop-interval-0s)
			              monitor interval=5s (Web_Cluster-monitor-interval-5s)

	- Để hiển thị ra cấu hình của resource nào đó, ta dùng câu lệnh:

			pcs resource show resource_id

		ví dụ:

			pcs resource_id show Virtual_IP

		kết quả nhận được:

			Resource: Virtual_IP (class=ocf provider=heartbeat type=IPaddr2)
			  Attributes: ip=172.16.69.254 cidr_netmask=24
			  Operations: start interval=0s timeout=20s (Virtual_IP-start-interval-0s)
			              stop interval=0s timeout=20s (Virtual_IP-stop-interval-0s)
			              monitor interval=30s (Virtual_IP-monitor-interval-30s)


- ### <a name="modified-parameters">4.8 Chỉnh sửa các tham số cụ thể của resource</a>

	- Để cập nhật lại cấu hình cho resource bao gồm các tham số, ta sử dụng câu lệnh sau:

			pcs resource update resource_id resource_options

		ví dụ:

			pcs resource update Virtual_IP cidr_netmask=32

		kết quả sau khi thay đổi như sau:
			
			Resource: Virtual_IP (class=ocf provider=heartbeat type=IPaddr2)
			  Attributes: ip=172.16.69.254 cidr_netmask=32
			  Operations: start interval=0s timeout=20s (Virtual_IP-start-interval-0s)
			              stop interval=0s timeout=20s (Virtual_IP-stop-interval-0s)
			              monitor interval=30s (Virtual_IP-monitor-interval-30s)


- ### <a name="enabling-disabling">4.9 Kích hoạt, vô hiệu hóa nhóm các resource</a>

	- Để khởi động một resource ta dùng câu lệnh:

			pcs resource enable resource_id

	- Để dừng hoạt động của một resource, ta dùng câu lệnh:

			pcs resource disable resource_id

- ### <a name="cleanup">4.10 Xóa các cảnh báo của các resource</a>
	
	- Trong quá trình các resource hoạt động, đôi khi sẽ xuất hiện các cảnh báo lỗi. Và bạn muốn đặt lại trạng thái của nó thì dùng câu lệnh sau để đặt lại toàn bộ trạng thái của resource và failcount của resource:

			pcs resource cleanup resource_id

____


# Các nội dung khác <a name="content-others"></a>

- [5. Các ràng buộc trong pacemaker cho resource](constraint.md)
	- [5.1. Ràng buộc vị trí](constraint.md#location-constraints)
		- [5.1.1. Cấu hình một "Opt-In" Cluster](constraint.md#opt-in)
		- [5.1.2. Cấu hình một "Opt-Out" Cluster](constraint.md#opt-out)
	- [5.2. Ràng buộc về thứ tự](constraint.md#order-constraints)
		- [5.2.1. Thứ tự cố định](constraint.md#mand-order)
		- [5.2.2. Thứ tự linh động](constraint.md#advi-order)
		- [5.2.3. Thứ tự tập hợp các resource](constraint.md#sets-order)
		- [5.2.4. Xóa bỏ resource từ các ràng buộc thứ tự](constraint.md#remove-order)
	- [5.3. Ràng buộc colocation của resources](constraint.md#colocation-constraint)
	- [5.3.1. Vị trí cố định](constraint.md#mand-place)
	- [5.3.2. Vị trí linh động](constraint.md#advi-place)
	- [5.3.3. Colocation các tập hợp resource](constraint.md#sets-place)
	- [5.3.4. Xóa bỏ ràng buộc colocation](constraint.md#colocation-remove)
	- [5.4. Hiển thị cấu hình các ràng buộc](constraint.md#display-constraints)