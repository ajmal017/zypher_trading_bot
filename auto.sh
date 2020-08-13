#!/bin/bash

#git config --global user.email sebastian.oderland@gmail
#git config --global user.name SebastianOderland
#git config --global github.token f07b1d96710b96bcfa767814133f4befdd943c87

branch=$(git rev-parse --abbrev-ref HEAD)
#repo_full_name=$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///;s/.git$//')
token=$(git config --global github.token)

read -p "Commit description: " desc
read -p "Version: " version

generate_post_data()
{
  cat <<EOF
{
  "tag_name": "v_$version",
  "target_commitish": "$branch",
  "name": "v_$version",
  "body": "$desc",
  "draft": false,
  "prerelease": false
}
EOF
}

git add .

git commit -m "$desc"
git push origin master
curl --data "$(generate_post_data)" "https://api.github.com/repos/SebastianOderland/zypher_trading_bot/releases?access_token=$token"

python3 setup.py sdist "$version"
c:/python38/lib/site-packages/twine upload dist/*