#!/bin/bash

git config --global user.email sebastian.oderland@gmail
git config --global user.name SebastianOderland
git config --global github.user SebastianOderland
git config --global github.pass Ferabulok7568
git config --global github.passwd Ferabulok7568
git config --global github.password Ferabulok7568

git add .
read -p "Commit description: " desc
git commit -m "$desc"
echo "SebastianOderland" | git push origin master

#read -p "Version: " version
#git tag "v_$version"

#python setup.py sdist
#twine upload dist/*