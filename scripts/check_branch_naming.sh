#!/bin/sh

branch_name=$(git rev-parse --abbrev-ref HEAD)

pattern="^(feature|bugfix|hotfix|refactor|chore|docs)/[a-z0-9\-_]+$"

if ! echo "$branch_name" | grep -qE "$pattern"; then
  echo "Branch name '$branch_name' is invalid!"
  echo "Use: feature/my-feature-name"
  exit 1
fi
