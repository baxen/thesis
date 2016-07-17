#!/bin/bash

# Python script to
#   - Increment version number
#   - Record a word and figure count for progress monitoring
#   - Update a progress plot (not yet implemented)
#   - Rebuild axen_thesis.pdf with latex
python ../../utility/pre-commit.py

# Add resulting changes
if [ $? -e 0]; then
    git add axen_thesis.pdf
    git add figures/progress.png
else
    echo "Failed to updated and build axen_thesis.pdf! Fix errors above before pushing."
    exit 1
fi
exit 0
