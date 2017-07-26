# Tổng quan về fencing
 

___


# Mục lục

+ [STONITH là gì?](#stonith)
+ [Fencing là gì](#whatis)
+ [Các nội dung khác](#others-content)


___

# Nội dung

+ <a name="stonith">STONITH là gì?</a>

	+ STONITH là viết tắt của cụm từ `Shoot Other Node In The Head` đây là một kỹ thuật dành cho fencing.
	+ Khởi động lại hoặt tắt hẳn các node bị lỗi trong cluster
	+ Dùng để bảo vệ dữ liệu tránh sự mất mát trong trường hợp sử dụng storage shared
	+ Lý do cần dùng đến cơ chế STONITH:

		- Giả sử trong một cluster có một node A bị lỗi. Node A sẽ được khởi động lại và được thêm lại vào cluster một lần nữa. Điều này có vẻ đã được khắc phục lỗi. Nhưng nếu đây là một lỗi quan trọng và ngay sau khi khởi động lại node A. Node A vẫn gặp lại lỗi đó và lại được khởi động lại, điều này cứ lặp đi lặp lại như thế nhưng lỗi thì vẫn cứ lỗi. STONITH rất cần thiết trong trường hợp này và chúng ta cần cấu hình cho phép tắt node A này đi để ngăn việc node A cứ khởi động lại như vậy. [Xem thêm](fencing-overview.md#whatis)


+  <a name="whatis">Fencing là gì?</a>

	- Trong một hệ thống cluster, có thể có nhiều node làm việc cùng sử dụng chung một phần dữ liệu quan trọng. Khi mà các node trong cluster rơi vào trạng thái không khả dụng, đa số các node còn lại trong cluster bắt đầu trở lên thất thường hoặc trở lên không hoạt động  dẫn đến cần có các hành động thủ công của người quản trị viên. Các vấn đề gây ra bởi các node trong cluster có thể được giảm nhẹ bằng việc thiết lập một chính sách fencing.
___

- # <a name="others-content">Các nội dung khác</a>

- [B. Tổng quan về pacemaker](docs/pacemaker-overview.md)
	- [B.1 Tổng quan về quorum](docs/quorum-overview.md)
	- [B.2 Tổng quan về STONITH/ fencing](docs/fencing-overview.md)
	- [B.3 Tổng quan về resource](docs/resource-overview.md)