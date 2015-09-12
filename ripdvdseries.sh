#!/bin/bash
# extractdvd.sh
# input must be:
#    - <devicename> (which can be anything lsdvd takes)
#    - <outputfolder> where do you want the ripped series
#    - <outputname> the base name of the output

INPUT_DVD=$1
OUTPUT_FOLDER=$2
OUTPUT_NAME=$3

LSDVDOUTPUT=$(lsdvd "$1")

# if available get the title and get the number of titles
TITLE=$(echo "$LSDVDOUTPUT" | grep -i Disc | sed 's/Disc Title: //g')
NOMTITLES=$(echo "$LSDVDOUTPUT" | grep -i Length | wc -l)
echo $NOMTITLES

# iterate over each title
for (( c=1; c <= $NOMTITLES+1; c++ )) do
      PREFIX=''
      if [ $c -lt  10 ]; then PREFIX="0" ; fi
      OUTPUT_NAME_TITLE=$OUTPUT_FOLDER"/"$OUTPUT_NAME"-"$PREFIX$c".m4v"
      HandBrakeCLI -i $INPUT_DVD -o $OUTPUT_NAME_TITLE -t $c -2 -b 512 -s "1" --subtitle-burned --ab 112
done
