#!/bin/bash

cd /home/pi/Desktop/Kurupira
git status
sleep 2
git add .
sleep 2
git commit -m "atualização padrão"
sleep 2
git status
sleep 2
git push origin master
sleep 2