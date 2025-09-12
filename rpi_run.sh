#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

git pull

source ".venv/bin/activate"

ARCH=$(dpkg-architecture -qDEB_HOST_MULTIARCH)
export LD_LIBRARY_PATH="$HOME/.local/lib:/usr/lib/$ARCH:$LD_LIBRARY_PATH"

python "app/main.py"
