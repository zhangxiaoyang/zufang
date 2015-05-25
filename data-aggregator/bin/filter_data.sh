#!/usr/bin/env bash

readonly finaldb="$1"
readonly month_limit="$2"
now=$(date "+%Y-%m-%d")

awk -F "\t" '
BEGIN{
    now = "'$now'";
    month_limit = "'$month_limit'"+0;
    split(now, tmp_arr, " ");
    split(tmp_arr[1], now_arr, "-");
    now_year = now_arr[1];
    now_month = now_arr[2];
    now_day = now_arr[3];
    delete tmp_arr;
}
{
    # hashurl  title  author  images  links  text  pub_time  
    # 1        2      3       4       5      6     7
    # jushi  shouji  zujin  dizhi  ditie  url  crawl_time  source  ext
    # 8      9       10     11     12     13   14          15      16

    pub_time=$7;
    split(pub_time, tmp_arr, " ");
    split(tmp_arr[1], date_arr, "-");
    year = date_arr[1];
    month = date_arr[2];
    day = date_arr[3];

    if((now_year-year)*12+(now_month-month)+1 <= month_limit) {
        print $0;
    }
}
' "$finaldb" > "$finaldb.$month_limit"
