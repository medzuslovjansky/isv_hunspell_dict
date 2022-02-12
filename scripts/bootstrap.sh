#!/usr/bin/env bash

if [[ -z "PACKAGE_NAME" ]]; then
  npx lerna bootstrap --no-ci
else
  npx lerna bootstrap --no-ci --include-dependents --include-dependencies --scope "$PACKAGE_NAME"
fi
