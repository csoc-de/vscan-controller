#!/bin/bash

if [ "$DEV" = "true" ]; then
  python3 ./main.py --dev
else
  python3 ./main.py
fi
