#!/usr/bin/env bash
# zhangxiaoyang.hit[at]gmail.com

readonly WORKSPACE=$(pwd)
readonly dbs=(\
    "link.db"\
    "link.meta"\
    "pagelist"\
    "content.db"\
    "house.db"\
    "imglist"\
    "imglist.0"\
    "imglist.diff"\
    "final.db"\
    "final.db.2"\
    "zufang.house.json"\
    "sim.db"\
)
readonly modules=(\
    "link-spider"\
    "link-spider"\
    "page-spider"\
    "content-extractor"\
    "house-refinery"\
    "data-aggregator"\
    "data-aggregator"\
    "data-aggregator"\
    "data-aggregator"\
    "data-aggregator"\
    "data-aggregator"\
    "data-aggregator"\
)
readonly opts=("import" "export")

function nothing()
{
    echo "do nothing... exit"
    exit 0;
}

function adapter()
{
    if [[ ${opts[@]} =~ "$1" ]]
    then
        opt="$1"
        path="$2"
    else
        echo "Usage: ./adapter.sh [import/export] directory"
        nothing
    fi

    case "$opt" in
        "import" )
            if [ -d "$path" ]
            then
                for ((i=0;i<${#dbs[@]};i++))
                do  
                    db=${dbs[$i]}
                    module=${modules[$i]}
                    mkdir -p "$WORKSPACE/$module/output"
                    echo "cp $path/$db -> $WORKSPACE/$module/output"
                    cp "$path/$db" "$WORKSPACE/$module/output"
                done
            else
                nothing
            fi
        ;;
        "export" )
            if [ -d "$path" ]
            then
                zufang="$path/zufang-$(date +%Y%m%d-%H%M%S)"
                mkdir -p "$zufang"
                for ((i=0;i<${#dbs[@]};i++))
                do  
                    db=${dbs[$i]}
                    module=${modules[$i]}
                    echo "cp $WORKSPACE/$module/output/$db -> $zufang"
                    cp "$WORKSPACE/$module/output/$db" "$zufang"
                done
            else
                nothing
            fi
        ;;
        * )
            nothing
        ;;
    esac
}

# Main entrance
adapter "$1" "$2"
