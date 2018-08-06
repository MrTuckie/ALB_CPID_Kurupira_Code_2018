#!/bin/bash



cd /home/pi/Desktop/Kurupira
git status
sleep 2
git add .
sleep 2
git commit -m "$(date +"%d-%m-%Y") $(date +"%T")"
sleep 2
git status
sleep 2
git push origin master
sleep 2