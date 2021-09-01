#!/bin/bash
python setup.py install
git add pyfi
git commit -m "Updates"
git push origin main
