#!/bin/bash
echo "Hammering port 25565..."
while true; do
  nc -vz 127.0.0.1 25565 &>/dev/null
done
