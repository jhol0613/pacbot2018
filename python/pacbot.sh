#!/bin/bash
# Run script: ./pacbot.sh external_server_ip external_server_port

if [ "$#" -eq 2 ]; then

	echo "Initializing modules..."
	python3 rmServer.py &
	sleep 2
	python3 commsModule.py  "$1" "$2" &
	sleep 2
	python3 motorModule.py &
	sleep 2
	python3 bumperModule.py &
	sleep 2
	python3 ultrasonicSensorModule.py &
	sleep 2
	python3 odometryModule.py &

	# $1 and $2 are the external server ip and port respectively
	#python3 commsModule.py "$1" "$2" &
	sleep 8 # Give modules time to initialize
	echo "All sensor and motor modules running"
	echo "Starting player module..."

	python3 gamePlayer.py

	# End background processes cleanly on main program exit
	echo "Shutting down all modules..."
	sleep 1
	trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

else

	echo "Please include external server IP and port"

fi