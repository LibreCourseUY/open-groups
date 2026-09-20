#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install -q -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8324
