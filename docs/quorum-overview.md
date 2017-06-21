# Tổng quan về quorum


___


# Mục lục

+ [Quorum là gì?](#concept)

+ [Các nội dung khác](#others-content)


___

# Nội dung

+  <a name="concept">Quorum là gì?</a>

	+ Là giải pháp tránh sự "split brain" trong cluster - một trường hopjq mà cluster được tách thành nhiều phần. Nhưng mỗi phần lại tiếp tục hoạt động như những cluster riêng biệt, có khả năng ghi vào cùng một dữ liệu và  có thể gây ra mất mát dữ liệu.

	+ Để duy trì tính toàn vẹn và sẵn có của cluster, các hệ thống cluster sử dụng khái niệm này để ngắn ngừa sự mất mát dữ liệu. Một cluster có quorum khi có hơn một nửa số lượng các node đang có trạng thái online. Để giảm thiểu nguy cơ mất mát dữ liệu, mặc định pacemaker sẽ ngừng tất cả các resource nếu cluster không có quorum

	+ quorum được hình thành bằng các sử dụng `voting system` khi mà một node trong cluster không hoạt động như mong muốn hoặc mất liên lạc với phần còn lại của cluster, các node còn lại trong cluster có thể thực hiện `vote` để cô lập và nếu cần thiết thì loại bỏ node đang bị lỗi, ... này ra khỏi cluster

	+ Ví dụ: trong một cluster có 6 node và số node đang hoạt động cần có ít nhất là 4 node mới có thể hình thành lên quorum. Nếu đa số các node không hoạt động hoặc trở nên không khả dụng thì mặc định cụm không có quorum và pacemaker sẽ ngừng các dịch vụ trong cluster.
	
	+ Trong trường hợp mà số lượng các node khả dụng và không khả dụng bằng nhau quorum có thể được cấu hình để có chính sách `tiebreaker` để tiếp tục quorum và duy trì các node trong cluster còn lại và dành quorum cho node mà có id thấp nhất.

	+ quorum chấp nhận 4 giá trị được cấu hình tương ứng với 4 hành động sau khi cluster xảy ra lỗi:

		- ignore: Tiếp tục quản lý tất cả các tài nguyên
		- freeze: Tiếp tục quản lý tất cả các tài nguyên, nhưng không phục hồi tài nguyên từ node lỗi
		- stop: Dừng tất cả các resource trong vùng ảnh hưởng.
		- suicide: Lập rào cản tất cả các node trong vùng có cluster bị ản hưởng

___


- # <a name="others-content">Các nội dung khác</a>

	Sẽ cập nhật sau
	+ [](#)