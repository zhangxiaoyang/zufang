#!/usr/bin/env bash

readonly contentdb=$1
readonly housedb=$2
readonly linkdb=$3
readonly dst=$4
readonly finaldb="$5"

awk -F "\t" '
ARGIND==1{
    hashurl=$1;
    title=$2;
    content=$3;
    jushi=$4;
    shouji=$5;
    zujin=$6;
    dizhi=$7;
    ditie=$8;
    house_arr1[hashurl]=jushi"\t"shouji"\t"zujin"\t"dizhi"\t"ditie;
}
ARGIND==2{
    hashurl=$1;
    url=$2;
    crawl_time=$3;
    source=$4;
    ext=$5;
    house_arr2[hashurl]=url"\t"crawl_time"\t"source"\t"ext;
}
ARGIND==3{
    line=$0;
    hashurl=$1;
    title=$2;
    author=$3;
    images=$4;
    links=$5;
    text=$6;
    pub_time=$7;
    # hashurl  title  author  images  links  text  pub_time  
    # 1        2      3       4       5      6     7
    # jushi  shouji  zujin  dizhi  ditie  url  crawl_time  source  ext
    # 8      9       10     11     12     13   14          15      16
    if(!(hashurl in house_arr1))
    {
        next;
    }
    if(!(hashurl in house_arr2))
    {
        next;
    }
    print line"\t"house_arr1[hashurl]"\t"house_arr2[hashurl];
}
' "$dst/$housedb" "$dst/$linkdb" "$dst/$contentdb" > "$finaldb"
