#!/bin/bash
echo "Starting IntervalometerPi Django Project"
cd /home/waffleer/Intervalometer-Pi-V2/intervalometerPi/
python3 manage.py runserver 0:8000
