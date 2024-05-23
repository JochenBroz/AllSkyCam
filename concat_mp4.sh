#!/bin/bash
cd "$(dirname "$0")"

REFERENCE=$(date +%Y-%m-%d_%H-%M-%S).mpg
touch $REFERENCE
FILES_TO_PROCESS=$(find *.jpg -not -newer $REFERENCE -print | sort)
stat -c "file %n duration %Y" $FILES_TO_PROCESS > images.txt
awk 'NR > 1 { print $1 " " $2 " " $3 " " ($4-prev)/1800.}{ prev = $4 }' <  images.txt  > images_with_duration.txt
ffmpeg -f concat -i images_with_duration.txt -r 30 -vf scale=1280:-2 ${REFERENCE%.*}.mp4
rm $FILES_TO_PROCESS
