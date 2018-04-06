#!/bin/bash

CURRENT_DIRECTORY=$PWD
TOP_DIR="$( cd "$(dirname "$0")" && cd .. && pwd)"
cd "$TOP_DIR"
cd tests
python3 -m unittest discover -p "*_ut.py" -v
cd "$CURRENT_DIRECTORY"
