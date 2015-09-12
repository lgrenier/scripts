#!/bin/bash
for file in *.mkv
do
mkvdts2ac3.sh -n --new -w . $file
done

