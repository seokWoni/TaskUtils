#!/bin/sh

for table_name in $(cat database_list.txt)
do
    echo $table_name;
   # mysqldump --column-statistics=0 -h [host] -u [user] -p[pass] [database] [table] > [dump_file].sql

done
