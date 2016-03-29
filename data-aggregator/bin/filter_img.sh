#!/usr/bin/env bash

readonly finaldb_cut="$1"
readonly imglist="$2"

#grep -o "http://[a-zA-Z0-9]*\.douban\.com/view/group_topic/large/public/[a-zA-Z0-9]*\.jpg" "$finaldb_cut" | sort | uniq > "$imglist"
egrep -o 'http[s]?://[^\S:]*?/\w*?\.jpg' "$finaldb_cut" | sort | uniq > "$imglist"
