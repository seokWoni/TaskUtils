#!/bin/sh

for i in $(grep -R -l "match_char" file_name.ext)
do
    filename=$(basename "$i");
    # 변경한 정보 확인
    sed 's/{match_char}/\1/g' $i > /path/$filename.ch;
    # 파일 비교
    diff $i /path/$filename.ch > /path/$filename.diff;
done
