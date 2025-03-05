#!/bin/bash

sed -i "s/<gvm_password>/${GVM_PASSWORD}/g" /app/VulnScanner.conf

/usr/bin/tmux new-session -d -s vulnscan
#/usr/bin/tmux set-option set-remain-on-exit on
/usr/bin/tmux new-window -d -n 'vulnscan' -t vulnscan:2 'cd /app && python main.py -a'
/usr/bin/tmux new-window -d -n 'vulnmon' -t vulnscan:1 'tail -f /app/log/vscan-controller.log'

tail -f /app/log/vscan-controller.log
