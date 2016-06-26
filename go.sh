#!/bin/sh

echo "Deleting .pyc files"
find . -name "*.pyc" -exec rm -rf {} \;

echo "git add ."
git add .

echo "git commit"
git commit -m $1
