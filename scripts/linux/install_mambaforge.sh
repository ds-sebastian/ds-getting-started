#!/bin/bash

# This script is for installing Mambaforge

# Download the Mambaforge installation script
echo "Downloading Mambaforge installer..."
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

# Make the installer executable
chmod +x "Miniforge3-$(uname)-$(uname -m).sh"

# Install Mambaforge without modifying the .bashrc/.zshrc (since we're using fish)
echo "Installing Mambaforge..."
bash "Miniforge3-$(uname)-$(uname -m).sh" -b -p "$HOME/mambaforge"

# Remove the installer script after installation
rm "Miniforge3-$(uname)-$(uname -m).sh"

echo "Mambaforge installation complete."

# You might want to initialize Mambaforge in your current shell session
# But since we're using Fish shell and the initialization is already in config.fish, this is not necessary
# You can just start a new Fish shell session or source the config.fish file
