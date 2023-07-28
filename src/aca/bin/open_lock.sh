#!/bin/bash

cd /home/pc/src/bin || exit
python buzzer.py&
python open_lock.py
