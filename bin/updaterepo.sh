#!/bin/bash
python setup.py install
git add pyfi
git commit -m "Updates"
sudo git push origin main
