#!/bin/sh
# Standalone checkouts may lack the sibling parent tooling. pre-commit's verbose
# hooks display the explicit skip even when this wrapper exits successfully.
set -eu
validator="../.org/tooling/validators/$1"
if [ ! -e "$validator" ] && [ ! -L "$validator" ]; then
    printf 'SKIPPED: missing parent validator %s\n' "$validator"
    exit 0
fi
exec "$validator" .
