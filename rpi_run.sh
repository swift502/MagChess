#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

# Update repository
git restore .
git pull

# Activate virtualenv
source ".venv/bin/activate"

ARCH=$(dpkg-architecture -qDEB_HOST_MULTIARCH)
export LD_LIBRARY_PATH="$HOME/.local/lib:/usr/lib/$ARCH:$LD_LIBRARY_PATH"

# Launch app
python "app/__main__.py"
