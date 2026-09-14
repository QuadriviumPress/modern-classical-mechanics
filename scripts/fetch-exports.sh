#!/usr/bin/env bash
# Fetch print editions produced by exports.yml (or the latest release fallback).
set -euo pipefail

mkdir -p exports

run_id=$(gh run list \
  --repo "$GITHUB_REPOSITORY" \
  --workflow exports.yml \
  --status success \
  --limit 1 \
  --json databaseId \
  --jq '.[0].databaseId // empty')

artifact_dir=$(mktemp -d)
if [ -n "$run_id" ] && gh run download "$run_id" \
    --repo "$GITHUB_REPOSITORY" \
    --name modernClassicalMechanics-exports \
    --dir "$artifact_dir" \
  && [ -f "$artifact_dir/modernClassicalMechanics.pdf" ] \
  && [ -f "$artifact_dir/modernClassicalMechanics.docx" ]; then
  mv "$artifact_dir"/* exports/
  rm -rf "$artifact_dir"
  echo "Fetched exports from latest Exports workflow run $run_id"
  exit 0
fi
rm -rf "$artifact_dir"

release_dir=$(mktemp -d)
if gh release download --repo "$GITHUB_REPOSITORY" \
  --pattern 'modernClassicalMechanics.pdf' \
  --pattern 'modernClassicalMechanics.docx' \
  --dir "$release_dir" \
  && [ -f "$release_dir/modernClassicalMechanics.pdf" ] \
  && [ -f "$release_dir/modernClassicalMechanics.docx" ]; then
  mv "$release_dir"/* exports/
  rm -rf "$release_dir"
  echo "Fetched exports from latest GitHub release"
  exit 0
fi
rm -rf "$release_dir"

echo "::warning::No complete export set was found. Run the Exports workflow once to populate the site's PDF and Word downloads."
