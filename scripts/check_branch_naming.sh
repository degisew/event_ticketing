#!/bin/sh

branch_name=$(git rev-parse --abbrev-ref HEAD)

pattern="^(feat|bugfix|hotfix|ref|test|perf|chore|docs)/[a-z0-9\-_]+$"

if ! echo "$branch_name" | grep -qE "$pattern"; then
  echo "Branch name doesn't follow Conventional branch name format"\n
  echo "Format: <type>/branch-name"\n
  echo -e "\e[36mExample:  feature/feature-branch-name\e[0m" \n \n
  echo -e "\e[36mAvailable tpes are [feature, bugfix, hotfix, refactor, test, perf, chore, docs]\e[0m"
  exit 1
fi
