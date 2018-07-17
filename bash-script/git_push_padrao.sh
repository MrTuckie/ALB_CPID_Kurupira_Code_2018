#!/bin/bash

cd /home/pi/Desktop/Kurupira
git status
sleep 2
git pull
sleep 2
git commit --amend -m "atualização padrão"
sleep 2
git add .
git status
sleep 2
git push origin master
sleep 2