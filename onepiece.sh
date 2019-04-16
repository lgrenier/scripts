#! /bin/bash

file=${1%%.*}
extension=${1##*.}
#number=$(grep -o '[[:digit:]]' <<<$1)
number=$(egrep -o [0-9]+ <<<$1)
#number=$((number-98))

#number=${filename//[^0-9]/}

echo number trouvé $number
number=$((number - 69))

echo number calculé $number
echo file $file
echo extension $extension

echo mv "$1" "One.Piece.S06E$number.1080p.h264.$extension"
