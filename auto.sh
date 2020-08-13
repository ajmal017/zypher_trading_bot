#!/bin/bash

git config --global user.email sebastian.oderland@gmail
git config --global user.name SebastianOderland
git config --global github.token f07b1d96710b96bcfa767814133f4befdd943c87

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
  "body": "",
  "draft": false,
  "prerelease": false
}
EOF
}

git add .

git commit -m "$desc"
git push https://SebastianOderland:Ferabulok7568@github.com/"$repo_full_name".git master

curl -u "SebastianOderland:f07b1d96710b96bcfa767814133f4befdd943c87" https://api.github.com/user #--data "$(generate_post_data)" "https://api.github.com/repos/$repo_full_name/releases?access_token=$token"
# curl \
#   -X POST \
#   -H "Authorization: token " \
#   -H "Accept: application/vnd.github.machine-man-preview+json" \
#   https://api.github.com/app/installations/287237342/access_tokens \
#   -d '{"repository_ids":[287237342]}'

# curl --data "$(generate_post_data)" "https://api.github.com/repos/$repo_full_name/releases?access_token=$token"



python3 setup.py sdist "$version"
#twine upload dist/*