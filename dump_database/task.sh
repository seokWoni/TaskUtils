#!/bin/sh

for table_name in $(cat database_list.txt)
do
    echo $table_name;
   # mysql 5.x 버전에서는 --column-statistics=0 추가
   # mysqldump --column-statistics=0 -h [host] -u [user] -p[pass] [database] [table] > [dump_file].sql # data, create 구문 추출
   # mysqldump --column-statistics=0 -d -h [host] -u [user] -p[pass] [database] [table] > [dump_file].sql # data 없이 create 구문만 추출
   # mysqldump --column-statistics=0 -t -h [host] -u  -p[pass] [database] [table] > [dump_file].sql # create 구문없이 data만 추출

done
