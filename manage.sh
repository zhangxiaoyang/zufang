#!/usr/bin/env bash
# zhangxiaoyang.hit[at]gmail.com

####################################################
# I take control of all the modules >_>
#
# Usage:
#   ./manage.sh [run/clean/status/kill] [modulename]
#   ./manage.sh [run/clean] all
#
# Note:
#   `clean all` will DELETE all the data!
#    Use `ctrl+z` to hang me up
#    then use `bg` to make me run in the background.
#
# Flow:
#   -----------------------------------------------
#   link-spider -> page-spider -> content-extractor
#   -> house-refinery -> data-aggregator
#   -----------------------------------------------
#                      |
#                   adapter.sh
#                    /    \ 
#               import    export
####################################################

readonly WORKSPACE=$(pwd)
readonly modules=("link-spider" "page-spider" "content-extractor" "house-refinery" "data-aggregator")
readonly opts=(${modules[@]} "all")
export PYTHONPATH="$WORKSPACE/libs"

function run_module()
{
    echo "run $modulepath"
    local modulepath=$1
    mkdir -p "$modulepath/data"
    mkdir -p "$modulepath/output"
    mkdir -p "$modulepath/log"
    eval "$modulepath/bin/run"
}

function clean_module()
{
    echo "clean $modulepath"
    local modulepath=$1
    rm -rf "$modulepath/data"
    rm -rf "$modulepath/output"
    rm -rf "$modulepath/log"
}

function kill_module()
{
    local modulepath=$1
    local pid=`ps aux|grep $modulepath|head -1|awk '{print $2;}'`
    kill -9 "$pid"
    local pid=`ps aux|grep $modulepath|head -1|awk '{print $2;}'`
    kill -9 "$pid"
    echo "kill $pid $modulepath"
    ps aux|grep $modulepath
}

function run_all()
{
    echo "run all"
    for module in ${modules[@]}
    do
        modulepath="$WORKSPACE/$module"
        run_module "$modulepath"
    done
}

function clean_all()
{
    echo "clean all"
    for module in ${modules[@]}
    do
        modulepath="$WORKSPACE/$module"
        clean_module "$modulepath"
    done
}

function kill_all()
{
    echo "kill all"
    for module in ${modules[@]}
    do
        modulepath="$WORKSPACE/$module"
        kill_module "$modulepath"
    done
}

function nothing()
{
    echo "do nothing... exit"
    exit 0;
}

function manage()
{
    if [[ ${opts[@]} =~ "$2" ]]
    then
        module="$2"
        modulepath="$WORKSPACE/$module"
    else
        nothing
    fi

    case "$1" in
        "clean" )
            if [ "$2" = "all" ]
            then
                clean_all
            elif [[ "$2" && ${modules[@]} =~ "$2" ]]
            then
                clean_module "$modulepath"
            else
                nothing
            fi
        ;;
        "run" )
            if [ "$2" = "all" ]
            then
                run_all
            elif [[ "$2" && ${modules[@]} =~ "$2" ]]
            then
                run_module "$modulepath"
            else
                nothing
            fi
        ;;
        "status" )
            if [[ "$2" && ${modules[@]} =~ "$2" ]]
            then
                ps aux | grep "$2" | head -1
                cat "$2"/log/log
            else
                nothing
            fi
        ;;
        "kill" )
            if [ "$2" = "all" ]
            then
                kill_all
            elif [[ "$2" && ${modules[@]} =~ "$2" ]]
            then
                kill_module "$modulepath"
            else
                nothing
            fi
        ;;
        * )
            if [[ "$1" && ${modules[@]} =~ "$1" ]]
            then
                module="$1"
                modulepath="$WORKSPACE/$module"
                run_module "$modulepath"
            else
                nothing
            fi
        ;;
    esac
}

# Main entrance
manage "$1" "$2"
