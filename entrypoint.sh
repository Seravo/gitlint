#!/bin/sh
set -e

OWNER="$(stat --printf='%u' "${PWD}")"

echo "Execute gitlint..."
gosu "${OWNER}" gitlint "$@"
