#!/bin/bash

# Internally forward port 8888 to 80
sudo /sbin/iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8888

# Activate conda; start jupyter lab
source /home/vcm/miniconda3/etc/profile.d/conda.sh
conda activate BioClocksClass
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser --config /home/vcm/.jupyter/jupyter_server_config.json
