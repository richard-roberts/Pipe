#!/bin/bash
echo "Running Pipe - tail ~/.forever/pipe for logging"
rm -f ~/.forever/pipe
sudo forever start -l pipe -c ./run.sh pipe/server.py

