#!/bin/bash
python setup.py install
git add *.txt
git add Makefile
git add docs
git add bin
git add diary.md
git add ui
git add pyfi
git commit -m "Updates"
git push origin main
