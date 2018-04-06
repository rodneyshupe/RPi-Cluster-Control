#!/bin/bash

CURRENT_DIRECTORY=$PWD
TOP_DIR="$( cd "$(dirname "$0")" && cd .. && pwd)"
cd "$TOP_DIR"

rm -Rf tests/__pycache__
rm -Rf lib/__pycache__
rm -Rf services/master/__pycache__
rm -Rf services/status/__pycache__
rm -Rf services/status_led/__pycache__

cd "$CURRENT_DIRECTORY"
