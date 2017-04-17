#! /bin/bash

file=${1%%.*}
extension=${1#*.}
#number=$(grep -o '[[:digit:]]' <<<$1)
number=$(egrep -o [0-9]+ <<<$file)
#number=$((number-98))

#number=${filename//[^0-9]/}

number=$((number - 27))

echo number trouvé $number
echo file $file
echo extension $extension

mv "$file.$extension" "Dragon_Ball_Super.S03E$number.1080p.h264-NC.$extension"
