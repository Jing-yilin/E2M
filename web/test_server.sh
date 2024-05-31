#!/bin/bash

# Wait for the server to start
while ! nc -z 127.0.0.1 3000; do
  sleep 0.1
done


# Check if the server is running on 127.0.0.1:3000
response=$(curl --write-out "%{http_code}" --silent --output /dev/null http://127.0.0.1:3000)

if [ "$response" -eq 200 ]; then
  echo "Server is running on 127.0.0.1:3000"
  exit 0
else
  echo "Server is not running on 127.0.0.1:3000"
  exit 1
fi
