#!/bin/bash

git config --global user.email sebastian.oderland@gmail
git config --global user.name SebastianOderland
git config --global github.token 7eada1464f1ef7f528ffe4c070aaf43b5c5a6178 

GIT_PASSWORD="Ferabulok7568"
git add .
read -p "Commit description: " desc
git commit -m "$desc"
git push https://SebastianOderland:Ferabulok7568@github.com/SebastianOderland/zypher_trading_bot.git master

read -p "Version: " version

branch=$(git rev-parse --abbrev-ref HEAD)
repo_full_name=$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///;s/.git$//')
token=$(git config --global github.token)

generate_post_data()
{
  cat <<EOF
{
  "tag_name": "$version",
  "target_commitish": "$branch",
  "name": "$version",
  "body": "",
  "draft": false,
  "prerelease": false
}
EOF
}

curl --data "$(generate_post_data)" "https://api.github.com/repos/$repo_full_name/releases?access_token=$token"

#python setup.py sdist
#twine upload dist/*