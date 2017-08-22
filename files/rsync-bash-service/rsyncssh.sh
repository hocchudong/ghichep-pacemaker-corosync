#!/usr/bin/bash
# @author: r3s3arch3r

# /kvmpool la thu muc chia se
# lb02 la ten host can dong bo (cau hinh trong /etc/hosts)
# tren host lb02 co thu muc /kvmpool voi reministry lam owner
# reministry la ten dang nhap host lb02


while true; do
    rsync -azve ssh /kvmpool reministry@lb02:/;
done
