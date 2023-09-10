#!/bin/bash

# Install required Python packages
while read -r package; do
    echo "Installing $package"
    pip install "$package"
done < requirements.txt