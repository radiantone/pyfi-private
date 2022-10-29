#!/bin/bash
python setup.py install
git add Makefile
git add docs
git add bin
git add diary.md
git add app
git add pyfi
git commit -m "Updates"
git push origin main
