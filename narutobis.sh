#! /bin/bash

for file in ls *.mkv
do
number=$(awk -F'[^0-9]*' '{print $2}' <<< $file)

echo number trouvé $number

number=$((number - 179))
echo number calculé $number

#number=${filename//[^0-9]/}

echo file $file
echo extension $extension

mv "$file" "Naruto.S05E$number.Multi.Dvdrip.X264-MaChO.mkv"
done

