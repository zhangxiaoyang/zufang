#!/usr/bin/env bash
# zhangxiaoyang.hit[at]gmail.com

imgdir="../db/imgdir"
mongopath="../db"
imglist="data-aggregator/output/imglist"
pagedir="page-spider/output/douban"

function load_env()
{
    source env/bin/activate
}

function clean_img_cache()
{
    local imglist="$1"
    local imgdir="$2"

    while read url
    do
        imgname=`echo -n "$url" | cut -d "/" -f 8`
        mv "$imgdir/$imgname" "$imgdir/$imgname.bak"
    done < "$imglist"

    for imgname in `ls $imgdir | grep -v "bak$"`
    do
        rm -f "$imgdir/$imgname"
    done

    for imgname in `ls $imgdir`
    do
        newname=`echo $imgname | sed 's/\.bak$//'`
        mv "$imgdir/$imgname" "$imgdir/$newname"
    done
}

function clean_page_cache()
{
    local pagedir="$1"
    rm -rf  "$pagedir"
}

echo "START: $(date '+%Y-%m-%d %H:%M:%S')"
load_env

lastestCmd=`ps aux | grep  "zufang.*run\|manage.sh" | grep -v "runserver" | grep -v grep`
if [ "$lastestCmd" == "" ]
then
    echo "Updating ..."
    bash manage.sh run all

    echo "Moving images ..."
    #mv data-aggregator/output/imgdir/* "$imgdir"
    find data-aggregator/output/imgdir/ -name '*.*' | xargs -i mv {} "$imgdir"

    echo "Cleaning img cache ..."
    clean_img_cache "$imglist" "$imgdir"

    echo "Cleaning page cache ..."
    clean_page_cache "$pagedir"

    echo "Cleaning DB ..."
    "$mongopath/mongo" zufang --eval "db.dropDatabase()"

    echo "Pushing DB ..."
    "$mongopath/mongoimport" -d zufang -c house data-aggregator/output/zufang.house.json
else
    echo "Stopped"
fi
echo "DONE: $(date '+%Y-%m-%d %H:%M:%S')"
