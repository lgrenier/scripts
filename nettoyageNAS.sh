#!/bin/bash
ssh root@192.168.0.1 "find /volume1/Partage/ \( -name '@eaDir' -o -name 'nohup.out' -o -name 'Thumbs.db' \) -exec rm -rf {} \;"
ssh root@192.168.0.1 "rm -rf /volume1/Partage/\#recycle /volume1/Partage/.Trash-1000"
#core
ssh root@192.168.0.1 "chown -R lgrenier:lgrenier /volume1/Partage/*"
ssh root@192.168.0.1 "find /volume1/Partage/* -type d -exec chmod 777 {} \;"
ssh root@192.168.0.1 "find /volume1/Partage/* -type f -exec chmod 666 {} \;"
