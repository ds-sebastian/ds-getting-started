#!/bin/bash

# Install Fish Shell
sudo apt update
sudo apt install -y fish

# Change the default shell to fish
chsh -s /usr/bin/fish

echo "Fish shell installed and set as default."
