#!/bin/bash
echo "ffmpeg -i \"$file\" -vcodec mpeg4 -vtag xvid -r 25 -s 624x352 -b 1024k -acodec libmp3lame -ar 48000 -ab 128k -ac 2 \"$file.archos.avi\" "

