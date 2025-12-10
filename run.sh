#!/usr/bin/env bash

# Run the Reed-Solomon demo with proper library path for macOS
# This script sets the DYLD_LIBRARY_PATH for zbar library

export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
uv run python main.py
