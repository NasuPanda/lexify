#!/bin/bash

# List all docker volumes
echo "Listing all Docker volumes:"
docker volume ls

# Confirm with the user
read -p "Are you sure you want to remove all Docker volumes? This cannot be undone. (y/n) " -n 1 -r
echo    # Move to a new line

if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Get all volume names
    volumes=$(docker volume ls -q)

    # Check if there are any volumes to delete
    if [ -z "$volumes" ]
    then
        echo "No volumes to remove."
    else
        # Remove all volumes
        echo "Removing all Docker volumes..."
        docker volume rm $volumes
        echo "All volumes have been removed."
    fi
else
    echo "Operation cancelled."
fi

