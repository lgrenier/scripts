#! /bin/bash

file=${1%%.*}
extension=${1#*.}
#number=$(grep -o '[[:digit:]]' <<<$1)
number=$(egrep -o [0-9]+ <<<$file)
#number=$(awk -F'[^0-9]*' '{print $2}' <<< $1)
number=$((number - 458))
#number=${filename//[^0-9]/}
echo number trouvé $number
echo file $file
echo extension $extension
mv "$file.$extension" "Naruto_Shippuuden.S22E$number.720p.HDTV.h264-FansubResistance.$extension"

