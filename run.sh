#!/bin/bash

USERNAME="devuser"
PASSWORD="Password1"
EMAIL="devuser@gmail.com"


python3 main.py --help
python3 main.py --action create_user --username $USERNAME --email $EMAIL --password $PASSWORD
python3 main.py --action validate_user --username $USERNAME
python3 main.py --action update_user --username $USERNAME --email $EMAIL --password $PASSWORD --admin
python3 main.py --action validate_user --username $USERNAME
python3 main.py --action delete_user --username $USERNAME
python3 main.py --action validate_user --username $USERNAME