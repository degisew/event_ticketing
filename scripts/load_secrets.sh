#!/bin/bash
echo -e "\e[36mLoading secrets to GitHub...\e[0m"

while IFS='=' read -r key value; do
  if [[ ! -z "$key" && ! "$key" =~ ^# ]]; then
    gh secret set "$key" --body "$value"
    echo -e "\e[1;32m✓ $key uploaded\e[0m"
  fi
done < .env.ci
