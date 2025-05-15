#!/bin/bash

# Try to run python command
if command -v python &> /dev/null
then
    # Run program if python is found
    python main.py students.csv

#Try to run python3 if python is not found
elif command python3 &> /dev/null
then
    # Run program if python3 is found
    python3 main.py students.csv
else
    # Python not found
    echo Error: Python installation not found.
    echo You can install Python from https://www.python.org/downloads/
fi