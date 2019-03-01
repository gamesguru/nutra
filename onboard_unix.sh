#!/bin/bash

#pip3 install -r requirements

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    printf 'sudo apt install redis-server\n'
    sudo apt install redis-server
elif [[ "$OSTYPE" == "darwin"* ]]; then
    printf 'brew install redis\n'
    brew install redis
fi
