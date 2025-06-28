#!/bin/bash
cd /home/kavia/workspace/code-generation/busbooker-115199-a669f9c2/bus_booking_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

