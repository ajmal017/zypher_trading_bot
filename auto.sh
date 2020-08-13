#!/bin/bash

git config --global user.email sebastian.oderland@gmail
git config --global user.name SebastianOderland

git add .
read -p "Commit description: " desc
git commit -m "$desc"
#git push origin master

#read -p "Version: " version
#git tag "v_$version"

#python setup.py sdist
#twine upload dist/*