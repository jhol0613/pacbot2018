#!/bin/bash
# Run script: ./pacbot.sh external_server_ip external_server_port

if [ "$#" -eq 2 ]; then
	python3 rmServer.py &
	python3 motorModule.py &
	python3 bumperModule.py &

	# $1 and $2 are the external server ip and port respectively
	#python3 commsModule.py "$1" "$2" &
	sleep 5 # Give modules time to initialize
	echo "All sensor and motor modules running"

	python3 gamePlayer.py
	echo "Player module running"
else
	echo "Please include external server IP and port"
fi