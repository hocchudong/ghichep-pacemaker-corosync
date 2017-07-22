# 6. Các ràng buộc resources trong pacemaker


____


# Mục lục

- [6.1. Ràng buộc vị trí](#location-constraints)
	- [6.1.1. Cấu hình một "Opt-In" Cluster](#opt-in)
	- [6.1.2. Cấu hình một "Opt-Out" Cluster](#opt-out)
- [6.2. Ràng buộc về thứ tự](#order-constraints)
	- [6.2.1. Thứ tự bắt buộc](#mand-order)
	- [6.2.2. Thứ tự không bắt buộc](#advi-order)
	- [6.2.3. Thứ tự tập các resource](#sets-order)
	- [6.2.4. Xóa bỏ resource từ các ràng buộc thứ tự](#remove-order)
- [6.3. Ràng buộc colocation của resources](#colocation-constraint)
- [6.3.1. Vị trí bắt buộc](#mand-place)
- [6.3.2. Vị trí không bắt buộc](#advi-place)
- [6.3.3. Colocation các tập resource](#sets-place)
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

		+ Việc lựa chọn cấu hình Cluster theo hướng nào phụ thuộc vào ý tưởng cá nhân và cách mà ta tạo ra cluster. Nếu hầu hết các node đều có thể chạy resource thì việc lựa chọn hướng `Opt-Out` sẽ khiến cho việc cấu hình đơn giản hơn. Mặc khác, nếu các resource chỉ có thể chạy trên một tập nhỏ các node trong cluster thì việc lựa chọn hướng  `Opt-In` sẽ khiến việc cấu hình đơn giản hơn.

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

	+ Để tạo ra một cấu hình theo hướng `Opt-Out` cluster, ta cần phải đặt giá trị `symmetric-cluster` để cho phép resource chạy được bất cứ trên node nào trong cluster bằng việc sử dụng câu lệnh:
	
			pcs property set symmetric-cluster=true

		đây là hướng cấu hình mặc định, nếu như bạn chưa từng chỉnh sửa giá trị này thì có thể bỏ qua bước này.

	+ Giả sử, mô hình triển khia cluster có 3 node theo phần [Cài đặt pacemaker](pacemaker-corosync-installing.md#block). Tiếp theo ta cần cấu hình cho phép resource chỉ được hoạt động trên node nào bằng việc thực hiện các câu lệnh sau:

			pcs constraint location Virtual_IP prefers lb01
			pcs constraint location Virtual_IP avoids lb02

			pcs constraint location Web_Cluster prefers lb02
			pcs constraint location Web_Cluster avoids lb01

- ### <a name="order-constraints">6.2. Ràng buộc về thứ tự</a>

	- Ràng buộc này quy định thứ tự mà resource hoạt động. Có thể cấu hình để quy định resource hoạt động hay dừng lại khi có hành động nào xảy ra.

	- Cú pháp để tạo một ràng buộc về thứ tự như sau:

			pcs constraint order [action] resource_id then [action] resource_id [options] 

		trong đó:
			- resource_id: tên của resource
			- action: hành động của constraint

	- Giá trị của các `action` trong câu lệnh tạo ràng buộc bao gồm:

		| Action | Mô tả |
		| ------------- | ------------- |
		| start (mặc định) | Khởi động resource |
		| stop | Dừng hoạt động resource |
		| promote | Thực hiện chuyển resource từ một resource slave thành một resource master |
		| demote | Thực hiện chuyển resource từ một resource master thành một resource slave |
		
	- Ngoài ra còn có thể thêm 2 trường nữa trong câu lệnh tạo ràng buộc trên được cho theo bảng sau:

		| Trường | Giá trị và mô tả |
		| ------------- | ------------- |
		| kind | <ul><li>Optionnal: Chỉ áp dụng ràng buộc nếu cả hai resource đều đang hoạt động hoặc không hoạt động (Xem thêm)[#advi-order]</li><li>Mandatory (mặc định): Nếu resource đầu tiên khai bao mà không hoạt động hoặc không thể khởi động, thì resource thứ hai đã khai bao trong câu lệnh bắt buộc phải không được hoạt động (Xem thêm)[#mand-order]</li><li>Serialize: Đảm bảo rằng sẽ không có hành động dừng lại/ khởi động (stop/start) cùng xảy ra cho cùng một nhóm các resource</li></ul> |
		| symmetrical | <ul><li>true (mặc định): buộc các resource dừng hoạt động theo thứ tự ngược lại, resource khai bao sau sẽ dùng hoạt động trước rồi mới đến resource khai báo đầu tiên</li><li>false: Dừng hoạt động dịch vụ theo đúng thứ tự đã khai báo trong câu lệnh</li></ul> |
		
- ### <a name="mand-order">6.2.1. Thứ tự bắt buộc</a>

	- Ràng buộc chỉ ra rằng resource thứ hai khai báo trong câu lệnh tạo ràng buộc không thể trở lên hoạt động khi không có resource đầu tiên chỉ ra trong câu lệnh đó đang hoạt động.
	- Nếu resource đầu tiên khai báo đang hoạt động và dừng lại thì resource thứ hai trong khai báo câu lệnh cũng sẽ trở lên dừng hoạt động (nếu nó đang hoạt động)
	- Nếu resource đầu tiên khai báo đang không hoạt động và không thể khởi động thì resource thứ hai sẽ phải dừng lại nếu nó đang hoạt động.
	- Nếu resource đầu tiên khai báo khởi động hay khởi động lại trong khi resource khai báo thứ hai đang hoạt động thì resource thứ hai cũng sẽ phải dừng và khởi động lại.
	- Ví dụ: 
			
			pcs constraint order start Virtual_IP then start Web_Cluster

		trong đó:

			- Virtual_IP: là resource khai báo đầu tiên hay resource thứ nhất
			- Web_Cluster: là resource khai báo thứ hai hay resource thứ hai.

- ### <a name="advi-order">6.2.2. Thứ tự không bắt buộc</a>

	- Ràng buộc thứ tự này chỉ ra rằng nó có hiệu lực khi và chỉ khi cả hai resource cùng đang dừng hoạt động hoặc đang khởi động. Các thay đổi trạng thái của resource thứ nhất sẽ không có ảnh hưởng gì đến resource thứ hai.

	- Ví dụ:

			pcs constraint order Virtual_IP then Web_Cluster kind=Optionnal

- ### <a name="sets-order">6.2.3. Thứ tự tập các resource</a>

	- Giả sử, khi bạn có hai hay nhiều hơn các resource phụ thuộc vào nhau. Hay nói cách khác việc hoạt động của resource này sẽ là tiền đề để cho resource tiếp theo hoạt động. Ví dụ ta có 4 resource lần lượt là A, B, C và D và bạn thực hiện cấu hình ràng buộc như sau:

			pcs constraint order start A then start B
			pcs constraint order start B then start C
			pcs constraint order start C then start D

	như vậy ta được một mô tả tương tự như hình sau:

		![set resource](../images/resource-set.png)

	để giải quyết vấn đề trên, bạn có thể dùng đến việc quản lý các resource theo nhóm theo tài liệu tại [5.5. Các nhóm resource](docs/resource-pacemaker.md#groups) nếu như các resource này đều cùng nằm trên cùng 1 node. Tuy nhiên, nếu các resource này không cùng nằm trên một node. Bạn có thể tạo ra một ràng buộc trên một tập các node với câu lệnh:

			pcs constraint order set resource1 resource2 [resourceN]... [options] [set resourceX resourceY ... [options]] [setoptions [constraint_options]]

	câu lệnh trên cung cấp các tùy chọn cấu hình như sau:

	| Tùy chọn | Mô tả cho tùy chọn |
	| ------------- | ------------- |
	| sequentical | Có thể thiết lập giá trị <br><ul><li>true</li><li>false</li></ul><br> để thế hiện bất cứ khi nào các resource cũng phải có thứ tự liên quan tới một resource khác. Nếu được cho giá trị là `false` thì nó cho phép tập các resource có thế được ràng buộc thứ tự liên quan tới các tập resource khác mà không có các resource nó chứa trong tập resource khác ấy.Vì vậy mà nó thực sự có ý nghĩa nếu có nhiều tập resource được thiết lập ràng buộc.|
	| require-all | Có thể có giá trị thiết lập là `true` hoặc `false` với ý nghĩa yêu cầu tất cả các resource phải được hoạt động trước khi tiếp tục chuyển sang tập khác. Nếu đặt là `false` có nghĩa chỉ một resource trong tập resource cần được hoạt động trước khi nó tiếp tục hướng tới tập khác. Tùy chọn này với giá trị false sẽ không có ảnh hưởng trừ khi được sử dụng cùng với các tập không có ràng buộc thứ tự (sequentical phải được đặt là false)|
	| action | với các giá trị `start`, `promote`, `demote`, `stop` được mô tả giống như ở mục [Ràng buộc thứ tự](#order-constraints) |
	| id | Tên của constraint |
	|role| Với các giá trị: Stopped/Started/Master/Slave|

	Với mô tả như đã nói ở phần đầu mục này, ta có thể thực hiện cấu hình như sau với câu lệnh:

			pcs constraint set A B C D sequentical=true

	- Ví dụ:

		Với mô hình như sau:

		![two-sets.png](../images/two-sets.png)

		ta cần thực hiện cấu hình sử dụng các câu lệnh như sau:

			pcs constraint order set A B sequentical=false set C D sequentical=false id=AB-CD

		Với mô hình như sau:

		![three-sets.png](../images/three-sets.png)

		ta cần thực hiện cấu hình sử dụng câu lệnh sau:

			pcs constraint order set A B sequentical=false set C D sequentical=true set E F sequentical=false
	
		Với mô hình phức tạp hơn một chút như sau:

		![three-sets-complex.png](../images/three-sets-complex.png)

		ta thực hiện cấu hình sử dụng câu lệnh:

			pcs constraint order set G F sequentical=true set C D E sequentical=false set B A sequentical=true id=GF-CDE-BA

- ### <a name="remove-order">6.2.4. Xóa bỏ resource từ các ràng buộc thứ tự</a>

	- Sử dụng câu lệnh sau để xóa bỏ sàng buộc thứ tự:

			pcs constraint order remove resource1 [resourceN]...


- ### <a name="colocation-constraint">6.3. Ràng buộc colocation của resources</a>

	- Ràng buộc này quy định vị trí của một resource A phụ thuộc vào vị trí của một resource B đang chạy trên node nào trong cluster. Hay nói cách khác resource A muốn hoạt động thì phải có resource B cũng đang hoạt động và cùng nằm chung trên một node_id với resource A.

	- Để tạo ra một ràng buộc colocation, sử dụng câu lệnh:

			pcs constraint colocation add [master|slave] source_resource with [master|slave] target_resource [score] [options]

		trong đó:

			- source_resource: là resource_id hay tên của resource phụ thuộc vào resource khác
			- target_resource: là resource_id hay tên của resource được resource khác phụ thuộc vào
			- source_resource và target_resource không có ranh giới phân biệt

		Cluster sẽ quyết định vị trí của target_resource trước tiên sau đó sẽ quyết định tới vị trí của source_resource

- ### <a name="mand-place">6.3.1. Vị trí bắt buộc</a>

	- Ràng buộc này thực sự có hiệu lực khi tùy chọn score được đặt giá trị là: +INFINITY hoặc -INFINITY. Với ý nghĩa:

		+ `+INFINITY`: Quy định source_resource phải chạy cùng trên một node với target_resource. Đây là giá trị mặc định
		+ `-INFINITY`: Quy định source_resource không được chạy cùng trên một node với target_resource. 

- ### <a name="advi-place">6.3.2. Vị trí không bắt buộc</a>

	- Đối với số lượng các ràng buộc có score=-INFINITY ít hơn score=INFINITY thì cluster sẽ cố gắng thực hiện mong muốn của bạn.
	Xem thêm thông tin tại [Advisory Placement](http://clusterlabs.org/doc/en-US/Pacemaker/1.0/html/Pacemaker_Explained/ch06s04s03.html)

- ### <a name="sets-place">6.3.3. Colocation các tập resource</a>

	- Ràng buộc này giống như ràng buộc có các thuộc tính giống như của ràng buộc nhóm resource và ràng buộc thứ tự nhưng áp dụng cho nhóm các resource phải nằm cùng trên một node với nhau. Để tạo ràng buộc, ta sử dụng câu lệnh:

			pcs constraint colocation set resource1 resource2 [resourceN]... [options] [set resourceX resourceY ... [options]] [setoptions [constraint_options]]


- ### <a name="colocation-remove">6.3.4. Xóa bỏ ràng buộc colocation</a>

	- Để xóa bảo ràng buộc colocation đã tạo. Ta sử dụng câu lệnh:

		pcs constraint colocation remove source_resource target_resource [constraint_id]

	trong đó: constraint_id là tên của ràng buộc.


- ### <a name="display-constraints">6.4. Hiển thị cấu hình các ràng buộc</a>

	- Để hiển thị thống kê các ràng buộc. Sử dụng câu lệnh:

			pcs constraint

		hoặc

			pcs constraint show --full

		để hiển thị cụ thể chi tiết về từng constraint

	- Để hiển thị các ràng buộc về thứ tự. Sử dụng câu lệnh:

			pcs constraint order show [--full]

	- Để hiển thị ràng buộc về vị trí. Sử dụng câu lệnh:

			pcs constraint location show [--full]			

	- Để hiển thị ràng buộc colocation. Sử dụng câu lệnh:

			pcs constraint colocation show [--full]
			
____



# Các nội dung khác <a name="content-others"></a>

	Sẽ cập nhật sau