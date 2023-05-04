#!/bin/sh
# $1 ~ n terminal에서 입력한 args

# 각 환경별 변수 설정
host='host'
database='database_name'

# data 혹은 table 마다 list가 다름
table_list=$(cat file_name.txt)

# charset (euc-kr, utf-8, etc..)
for table_name in $table_list
do
    if [ $1 = 'only_data' ] ; then
        # create 구문없이 data만 추출
        if [ $table_name = 'wherecase' ]; then
            # where 조건 dump
            mysqldump -t -h $host -u user_name -p password $database $table_name --where="wherecase" --default-character-set='charset' > ./path/file_name.tmp
        elif [ $table_name = 'nomal' ] ; then
            # where 조건 없이
            mysqldump -t -h $host -u user_name -p password $database $table_name --default-character-set='charset' > ./path/file_name.tmp
        fi

        # 필요시 iconv 및 sed
        if [ $table_name = 'sed_and_iconv' ]; then
            iconv -f cp949 -t utf-8 -c ./path/file_name.tmp > ./path/file_name.sql
            sed -i 's/{match_char}/{replace_char}/g' ./path/file_name.sql
        fi
    elif [ $1 = 'only_create' ]; then
        # table create 구문만 추출
        mysqldump --skip-add-drop-table -d -h $host -u user_name -p password $database ${table_name} > ./path/file_name.sql
    fi
done
