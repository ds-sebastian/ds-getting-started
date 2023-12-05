#!/bin/bash

sudo apt-get update -y && sudo apt-get full-upgrade -y && sudo apt-get autoremove -y && sudo apt-get autoclean -y

# Install development tools
sudo apt install -y build-essential git cmake

# Install network tools
sudo apt install -y net-tools whois dnsutils wget curl traceroute

# Install Python and R
sudo apt install -y python3 python3-pip r-base

# Install database clients
sudo apt install -y sqlite3

# Install system monitoring tools
sudo apt install -y htop ncdu

# Install miscellaneous tools
sudo apt install -y tmux openssh-server neofetch

# Check for NVIDIA GPU
if lspci | grep -i nvidia; then
    echo "NVIDIA GPU detected"

else
    echo "No NVIDIA GPU detected"
fi


# Clone the dotfiles repository
git clone https://github.com/ds-sebastian/dotfiles.git "$HOME/dotfiles"

# Run other necessary scripts
bash "$HOME/dotfiles/scripts/install_fish.sh"
bash "$HOME/dotfiles/scripts/install_starship.sh"
bash "$HOME/dotfiles/scripts/install_mambaforge.sh"
bash "$HOME/dotfiles/scripts/install_docker.sh"

# Symlink dotfiles
# ln -sv "$HOME/dotfiles/.bashrc" "$HOME/.bashrc"

# Source the .bashrc to bring in new aliases, functions, etc.
# source "$HOME/.bashrc"

echo "Bootstrap complete!"
