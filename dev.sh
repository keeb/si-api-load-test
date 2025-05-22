#!/usr/bin/env sh

export SI_API_KEY=$(cat key)
export PYTHONPATH=src

python demo.py
