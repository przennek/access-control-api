#!/bin/bash
cd /home/pc/src/gpio || exit
python buzzer.py&
python close_lock.py
