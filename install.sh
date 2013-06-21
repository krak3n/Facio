#!/bin/bash

# Install Facio as an egg - 1 optional argument, extras_require environment.

if [ $1 ]
then
    pip install -e .[$1]
else
    pip install -e .
fi
