# Tích hợp ZFS với Pacemaker và Corosync

____

# Mục lục


- [1. ZFS là gì?](#what-is)
- [2. Tích hợp ZFS với Pacemaker và Corosync](#integrate)
- [3. Kiểm tra kết quả](#checksummed)
- [Các nội dung khác](#content-others)

____

# <a name="content">Nội dung</a>

- ### <a name="what-is">1. ZFS là gì?</a>

    - ZFS (Zettabyte File System) là sự kết hợp giữa Volume Manager và Filesystem hoạt động cơ bản bằng việc thay đổi cách mà file systems quản lý với nhiều tính năng và lợi ích mà không thế tìm thấy trong bất kỳ hệ thống hiện có ngày nay. ZFS hoạt động một cách mạnh mẽ và dễ dàng để quản lý.

- ### <a name="integate">2. Tích hợp ZFS với Pacemaker và Corosync</a>

    - Đầu tiên, ta cần tạo ra một cluster sử dụng Pacemaker và Corosync. Mô hình của toàn bộ hệ thống thực hiện lab giống như sau:


    - Trên 2 node `lb01` và `lb02`, ta thực hiện cài đặt Pacemaker và Corosync để có thể tạo ra được 1 cluster từ 2 node này:
    
            yum install -y pcs pcsd 

        khi cài đặt xong, ta cần khởi động các dịch vụ `pacemaker` và `corosync`:

            systemctl start pcsd
            systemctl start corosync

        cho phép `pacemaker` và `corosync` khởi động cùng với hệ thống:

            systemctl enable pcsd
            systemctl enable corosync

    - Tiếp theo, ta cần thực hiện cài đặt `zfs` trên cả 2 node `ha-zfs01` và `ha-zfs02`, thực hiện chạy câu lệnh sau trên cả 2 node:

            yum install -y http://download.zfsonlinux.org/epel/zfs-release.el7_3.noarch.rpm
            gpg --quiet --with-fingerprint /etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux

        sau đó, ta cần sửa lại nội dung file /etc/yum.repo/zfs.repo tương tự như sau để khi cài đặt zfs, hệ thống sẽ cài thêm gói `zfs-kmod` thay vì cài gói `zfs-dkms` như mặc định để đề phòng cho trường hợp bạn gặp phải lỗi `modprobe: FATAL: Module zfs not found.` ở bước phía dưới:

            # /etc/yum.repos.d/zfs.repo

            [zfs]
            name=ZFS on Linux for EL 7 - dkms
            baseurl=http://download.zfsonlinux.org/epel/7/$basearch/
            enabled=0
            metadata_expire=7d
            gpgcheck=1
            gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux
            [zfs-kmod]
            name=ZFS on Linux for EL 7 - kmod
            baseurl=http://download.zfsonlinux.org/epel/7/kmod/$basearch/
            enabled=1
            metadata_expire=7
            gpgcheck=1
            gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux

        cuối cùng ta chạy câu lệnh sau để cài đặt zfs trên cả 2 node và device-mapper-multipath software:

            yum install -y zfs device-mapper-multipath

    - Tạo ra một file cấu hình trống để cho de vice-mapper-multipath có thể khởi chạy:

            touch /etc/multipath.conf
            systemctl start multipathd
            systemctl enable multipath

    - Cho phép zfs tự động mount disk và khởi động cùng hệ thống:

            systemctl enable zfs-import-cache.service zfs-mount.service zfs-share.service zfs-zed.service zfs.target

    - Việc cuối cùng dành cho bước cài đặt `zfs` này là, ta cần import module của zfs vào trong kernel bằng việc sử dụng câu lệnh:

            modprobe zfs

        sau đó ta cần tạo ra một storage pool trước khi thực hiện thêm mới một resource zfs cho pacemaker quản lý bằng cách xử dụng câu lệnh sau:

            zpool create -f vol1 /dev/sdb /dev/sdc

        trong đó:

            - vol1 là tên của storage pool
            - /dev/sdb và /dev/sdc là đường mount của 2 đĩa disk mà bạn muốn dùng nó để gộp lại thành một storage pool

        bạn có thể lấy thông tin về đường dẫn disk qua việc sử dụng câu lệnh:

            fdisk -l

        kết quả ta được tương tự như sau:

            Disk /dev/sda: 21.5 GB, 21474836480 bytes, 41943040 sectors
            Units = sectors of 1 * 512 = 512 bytes
            Sector size (logical/physical): 512 bytes / 512 bytes
            I/O size (minimum/optimal): 512 bytes / 512 bytes
            Disk label type: dos
            Disk identifier: 0x0000cc55

               Device Boot      Start         End      Blocks   Id  System
            /dev/sda1   *        2048     2099199     1048576   83  Linux
            /dev/sda2         2099200    41943039    19921920   8e  Linux LVM

            Disk /dev/sdb: 1073 MB, 1073741824 bytes, 2097152 sectors
            Units = sectors of 1 * 512 = 512 bytes
            Sector size (logical/physical): 512 bytes / 512 bytes
            I/O size (minimum/optimal): 512 bytes / 512 bytes


            Disk /dev/sdc: 1073 MB, 1073741824 bytes, 2097152 sectors
            Units = sectors of 1 * 512 = 512 bytes
            Sector size (logical/physical): 512 bytes / 512 bytes
            I/O size (minimum/optimal): 512 bytes / 512 bytes


            Disk /dev/mapper/cl-root: 18.2 GB, 18249416704 bytes, 35643392 sectors
            Units = sectors of 1 * 512 = 512 bytes
            Sector size (logical/physical): 512 bytes / 512 bytes
            I/O size (minimum/optimal): 512 bytes / 512 bytes


            Disk /dev/mapper/cl-swap: 2147 MB, 2147483648 bytes, 4194304 sectors
            Units = sectors of 1 * 512 = 512 bytes
            Sector size (logical/physical): 512 bytes / 512 bytes
            I/O size (minimum/optimal): 512 bytes / 512 bytes

        qua kết quả của câu lệnh trên thì ta thấy /dev/sdb và /dev/sdc chính là đường dẫn của 2 disk mà ta đang muốn gộp chúng lại.

    - Để kiểm tra kết quả của việc tạo ra storage pool đã thành công hay chưa, ta có thể sử dụng câu lệnh sau để kiểm tra:

            zpool status

        nếu đã tạo thành công, kết quả sẽ tương tự giống như sau:

              pool: vol1
             state: ONLINE
              scan: none requested
            config:

                    NAME        STATE     READ WRITE CKSUM
                    vol1        ONLINE       0     0     0
                      sdb       ONLINE       0     0     0
                      sdc       ONLINE       0     0     0

            errors: No known data errors

        tại thời điểm này, bạn hãy thử reboot lại cả 2 node `ha-zfs01` và `ha-zfs02` sau đó chạy câu lệnh sau để kiểm tra kết quả:

            zfs list

        kết quả sẽ được trả về nếu ta đã cài đặt hoàn toàn thành công tương tự như sau:

            NAME   USED  AVAIL  REFER  MOUNTPOINT
            vol1  85.5K  1.84G    24K  /vol1

        nếu gặp lỗi sau:

            The ZFS modules are not loaded.
            Try running '/sbin/modprobe zfs' as root to load them.

        ta cần chạy câu lệnh sau đây để khắc phục vấn đề này (xem theo nội dung tại: [ZFS 0.6.5.8 modules not loading during boot (CentOS 7)](https://github.com/zfsonlinux/zfs/issues/5191)):

            systemctl preset zfs-import-cache zfs-import-scan zfs-mount zfs-share zfs-zed zfs.target


    - Download resource zfs cho pacemaker để có thể tạo ra một resource zfs cho pacemaker quản lý. Để download, ta thực hiện câu lệnh sau trên cả hai node `lb01` và `lb02`:

            cd /usr/lib/ocf/resource.d/heartbeat/
            wget https://github.com/skiselkov/stmf-ha/raw/master/heartbeat/ZFS
            chmod +x ZFS

        tiếp theo, để tạo ra resource cho dịch vụ zfs, ta sử dụng câu lệnh sau:

            pcs resource create vol1 ZFS pool="vol1" op start timeout="90" op stop timeout="90" --group=vol-zfs
        
        trong đó:

            - vol1: là tên của resource
            - ZFS: là loại resource
            - pool="vol1": khai báo storage pool cho resource quản lý đó là vol1
            - importargs="-d /dev/mapper/": là tham số khai báo cho phép zpool import sử dụng

    - Tạo ràng buộc cho resource vol1 và resource Virtual_IP phải cùng chạy với nhau trên 1 node. Vì ta sử dụng zfs cho chức năng lưu trữ và chia sẻ file cho các node. Ta nhận thấy resource vol1 cần phải phụ thuộc vào resource Virtual_IP, nên ta cần phải chạy câu lệnh sau để tạo ra ràng buộc:

            pcs constraint colocation add vol1 with Virtual_IP

    - Để sử dụng các chức năng về chia sẻ cũng như đồng bộ dữ liệu giữa các node `ha-zfs01` và `ha-zfs02`, zfs sử dụng việc chia sẻ các snapshot để đồng bộ giữa các node cài đặt zfs hoặc chia sẻ theo hướng client-server sử dụng dịch vụ nfs và rpcbind. Đầu tiên, ta cần khởi chạy 2 dịch vụ nfs và rpcbind để có thể sử dụng đầy đủ 2 hướng đồng bộ và chia sẻ dữ liệu trên qua việc chạy câu lệnh sau trên cả 2 node `ha-zfs01` và `ha-zfs02`:

            systemctl enable rpcbind nfs
            systemctl start rpcbind nfs

        sau đó, ta cần thiết lập cho storage pool nào được phép chia sẻ dữ liệu qua nfs bằng việc sử dụng câu lệnh sau trên cả 2 node `ha-zfs01` và `ha-zfs02`:

            zfs set sharenfs=rw=@192.168.77.0/24,sync,no_root_squash,no_wdelay vol1/management

        trong đó:
            
            - vol1: là thư mục được chia sẻ cho các node khác
            - 192.168.77.0/24: là dải mạng mà các máy chủ phải nằm trong đó mới có thể sử dụng
            - rw: là quyền được phép của các máy chủ khi sử dụng. Ở đây là Read và Write
            - Các tham số khác có thể xem thêm ở đây: https://www.server-world.info/en/note?os=CentOS_7&p=nfs&f=1

        
- ### <a name="checksummed">3. Kiểm tra kết quả</a>

____

# <a name="content-others">Các nội dung khác</a>
