#!/bin/bash

# Install Starship prompt
sh -c "$(curl -fsSL https://starship.rs/install.sh)"

# Link starship configuration
ln -sv "$HOME/dotfiles/.config/starship.toml" "$HOME/.config/starship.toml"

echo "Starship prompt installed."
