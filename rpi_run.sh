#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$SCRIPT_DIR/.venv/bin/activate"

# detect the architecture (armhf, arm64, etc.)
ARCH=$(dpkg-architecture -qDEB_HOST_MULTIARCH)

# prepend your ~/.local/lib to LD_LIBRARY_PATH
export LD_LIBRARY_PATH="$HOME/.local/lib:/usr/lib/$ARCH:$LD_LIBRARY_PATH"

# run your python app
NO_AT_BRIDGE=1 python "$SCRIPT_DIR/app/__main__.py"
