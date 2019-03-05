#!/bin/bash
#

printf '\n\e[1;31mpip3 install -r requirements\e[0m\n'
pip3 install -r requirements

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    printf '\n\e[1;31msudo apt install redis-server\e[0m\n'
    sudo apt install redis-server
elif [[ "$OSTYPE" == "darwin"* ]]; then
    printf '\n\e[1;31mbrew install redis\e[0m\n'
    brew install redis
fi
