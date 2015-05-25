#!/usr/bin/env bash

number=$1
filename=$2

count=`wc -l "$filename" | awk '{print $1;}'`
rand_array=()

function in_array()
{
    local rand_array=$1
    local rand=$2
    local i
    for i in ${rand_array[@]}
    do
        if [ "$i" = "$rand" ]
        then
            return 0
        fi
    done
    return 1
}
# Generate random line number(count from 1).
for i in $(seq "$number")
do
    let rand=$RANDOM*$RANDOM%$count+1
    tmp_array=`echo ${rand_array[@]}`
    while true
    do
        in_array "$tmp_array" "$rand"
        if [ $? = 0 ]
        then
            let rand=$RANDOM*$RANDOM%$count+1
        else
            break
        fi
    done
    #echo "add " $i $rand
    rand_array[$i]=$rand
done

# Extract lines.
string=`echo ${rand_array[@]} | awk '
{
    gsub(" ", "p;", $0);
    print $0"p";
}
'`
eval "sed -n" "'${string}'" "$filename"
