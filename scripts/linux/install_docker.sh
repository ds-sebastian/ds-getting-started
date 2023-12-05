#!/bin/bash

# Download the official Docker installation script
curl -fsSL https://get.docker.com -o get-docker.sh

# Execute the Docker installation script
sudo sh get-docker.sh

# Clean up the installation script
rm get-docker.sh

echo "Docker installation script complete!"
