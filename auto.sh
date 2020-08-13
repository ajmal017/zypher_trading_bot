#!/bin/bash

#git config --global user.email sebastian.oderland@gmail
#git config --global user.name SebastianOderland
#git config --global github.token f07b1d96710b96bcfa767814133f4befdd943c87

branch=$(git rev-parse --abbrev-ref HEAD)
repo_full_name=$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///;s/.git$//')
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
#git@github.com:SebastianOderland/zypher_trading_bot.git
git push origin master

#curl --data "$(generate_post_data)" "https://api.github.com/repos/$repo_full_name/releases?access_token=$token"
# curl \
#   -X POST \
#   -H "Authorization: token " \
#   -H "Accept: application/vnd.github.machine-man-preview+json" \
#   https://api.github.com/app/installations/287237342/access_tokens \
#   -d '{"repository_ids":[287237342]}'
echo $repo_full_name
curl \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/SebastianOderland/zypher_trading_bot/releases \
  -d '$(generate_post_data)'

# curl --data "$(generate_post_data)" "https://api.github.com/repos/$repo_full_name/releases?access_token=$token"



#python3 setup.py sdist "$version"
#twine upload dist/*