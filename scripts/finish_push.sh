#!/bin/bash

# Base directory
cd /Users/pingwin/Desktop/GAMEREPO

# List of game directories to process
# We get all directories in public/games/
for game_path in public/games/*; do
    if [ -d "$game_path" ]; then
        game_slug=$(basename "$game_path")
        echo "Processing $game_slug..."
        
        # Add game directory
        git add "$game_path"
        
        # Add corresponding image directory
        img_path="public/cache/data/image/game/$game_slug"
        if [ -d "$img_path" ]; then
            git add "$img_path"
        fi
        
        # Commit if there are changes
        # We rely on git commit returning 0 if succesful, non-zero if empty
        if git commit -m "Add game: $game_slug"; then
            echo "Committed $game_slug. Pushing..."
            git push
        else
            echo "Nothing to commit for $game_slug (skipped)."
        fi
    fi
done

echo "Bash push script complete."
