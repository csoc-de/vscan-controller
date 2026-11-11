#!/bin/bash

if [ "$DEV" = "true" ]; then
  vscan-controller --dev
else
  vscan-controller
fi
