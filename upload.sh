#!/bin/sh
rsync  -e ssh --progress --archive --exclude-from=${HOME}/.exclude --recursive ./ do-hana:~/heatmap
rsync  -e ssh --progress --archive --exclude-from=${HOME}/.exclude --recursive ./ aws-hana:~/heatmap
