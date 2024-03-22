#!/bin/bash

install_dir="/opt/Hiddify-Manager-Bot"
repository_url="https://github.com/H-Return/Hiddify-Manager-Bot.git"

# Update and upgrade system packages
apt update && apt upgrade -y

# Install necessary packages
apt install -y python3 python3-pip git python3-dev python3-venv docker docker-compose

# Clone the repository
git clone "$repository_url" "$install_dir"

# Change to the installation directory
cd "$install_dir"

# Prompt for environment variables
clear
echo "Please provide the following environment variables:"

read -p "Chat ID: " ALLOWED_USER_IDS
read -p "Admin uuid: " ADMIN_UUID
read -p "Admin panel url: " ADMIN_URLAPI
read -p "Panel sublink url: " SUBLINK_URL
read -p "Bot Token: " TELEGRAM_TOKEN

# Set environment variables in .env file
echo "ALLOWED_USER_IDS=$ALLOWED_USER_IDS" >> .env
echo "ADMIN_UUID=$ADMIN_UUID" >> .env
echo "ADMIN_URLAPI=$ADMIN_URLAPI" >> .env
echo "SUBLINK_URL=$SUBLINK_URL" >> .env
echo "TELEGRAM_TOKEN=$TELEGRAM_TOKEN" >> .env

# Start the Docker containers
docker-compose up -d

echo "HiddifyBot Docker containers are now up and running."
