#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

git reset --hard
git clean -fd
git fetch --prune origin
git checkout -B players origin/players
git reset --hard
git clean -fd

source ".venv/bin/activate"

ARCH=$(dpkg-architecture -qDEB_HOST_MULTIARCH)
export LD_LIBRARY_PATH="$HOME/.local/lib:/usr/lib/$ARCH:$LD_LIBRARY_PATH"

python "app/__main__.py"
