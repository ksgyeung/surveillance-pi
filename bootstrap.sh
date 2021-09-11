#!/bin/bash

if [ ! -d "surveillance-pi" ]; then
    git clone https://github.com/ksgyeung/surveillance-pi.git
fi
cd surveillance-pi
git fetch
git pull
cd ..

