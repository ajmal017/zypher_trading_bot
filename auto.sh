#!/bin/bash

branch=$(git rev-parse --abbrev-ref HEAD)
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
python3 -m twine upload dist/*
