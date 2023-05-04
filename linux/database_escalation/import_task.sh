#!/bin/sh

host='host'
database='database_name'

table_list=$(find ./file_path -name "*.sql")

for sql_file in $table_list
do
    mysql -h $host -u user_name -p password $database < $sql_file;
done
