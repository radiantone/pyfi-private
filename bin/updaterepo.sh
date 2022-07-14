#!/bin/bash
python setup.py install
git add bin
git add app
git add pyfi
git commit -m "Updates"
git push origin main
