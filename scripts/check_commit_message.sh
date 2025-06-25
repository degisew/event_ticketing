#!/bin/sh

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

pattern="^(feat|fix|docs|style|ref|conf|test|chore|perf)(\([a-z0-9\-]+\))?: .+"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
  echo "Commit message doesn't follow Conventional Commit format"
  echo "Format: <type>(optional-scope): message"
  echo "Example: feat(auth): add token login"
  exit 1
fi
