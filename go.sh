#!/bin/bash  
find . -name "*.pyc" -exec rm -rf {} \;
git add .  
read -p "Commit description: " desc  
git commit -m "$desc"  
git push origin master