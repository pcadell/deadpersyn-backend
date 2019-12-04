#!/bin/bash

python3 /home/anteo/sei-cranberry-gobblers/capstone/deadpersyn-flask/deadpersyn_app.py

while ! lsof -i -P -n | grep LISTEN &
	do echo 'Awaiting Flask'
done
wget http://127.0.0.1:5000/send-mail 


#while ! lsof -i -P -n | grep LISTEN; #&>dev/null;
#	do python3 /home/anteo/sei-cranberry-gobblers/capstone/deadpersyn-flask/deadpersyn_app.py;
#done
#echo "Flask running"
#wget http://127.0.0.1:5000/send-mail


#statement=`grep -n "hello" self-delete1.sh`
#echo $statement