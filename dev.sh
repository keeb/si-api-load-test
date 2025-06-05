#!/usr/bin/env sh

export SI_API_KEY="$(cat key)"
export SI_BASE_URL="http://localhost:5380"
export PYTHONPATH=src
 
python demo.py
