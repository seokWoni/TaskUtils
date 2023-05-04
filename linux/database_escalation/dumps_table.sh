#!/bin/sh

for table_name in $(cat database_list.txt)
do
   # mysqldump -h [host] -u [user] -p[pass] [database] [table] > [dump_file].sql # data, create 구문 추출
   # mysqldump -d -h [host] -u [user] -p[pass] [database] [table] > [dump_file].sql # data 없이 create 구문만 추출
   # mysqldump -t -h [host] -u  -p[pass] [database] [table] > [dump_file].sql # create 구문없이 data만 추출

done
