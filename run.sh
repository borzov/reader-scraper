#!/bin/bash

# Step 1: Create a virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    python3 -m venv env
fi

# Step 2: Activate the virtual environment
source env/bin/activate

# Step 3: Run the Python script with any passed arguments
python main.py "$@"

# Deactivate the virtual environment if necessary
deactivate