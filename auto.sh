#!/bin/bash

git config --global user.email sebastian.oderland@gmail
git config --global user.name SebastianOderland
git config --global github.token 802f80d7640739421cf7b57db9126985d2a1ff71

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

echo "Ferabulok7568" | curl -u "SebastianOderland" https://api.github.com --data "$(generate_post_data)" "https://api.github.com/repos/$repo_full_name/releases?access_token=$token"
# curl \
#   -X POST \
#   -H "Authorization: token " \
#   -H "Accept: application/vnd.github.machine-man-preview+json" \
#   https://api.github.com/app/installations/287237342/access_tokens \
#   -d '{"repository_ids":[287237342]}'

# curl --data "$(generate_post_data)" "https://api.github.com/repos/$repo_full_name/releases?access_token=$token"



python3 setup.py sdist
#twine upload dist/*