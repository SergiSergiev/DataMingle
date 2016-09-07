#!/bin/sh
echo "Copying files to Amazon server ..."
rsync  -e ssh --progress --archive --exclude-from=${HOME}/.exclude --recursive ./ aws-hana:~/heatmap
