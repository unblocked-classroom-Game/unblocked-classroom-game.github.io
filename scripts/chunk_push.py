import os
import subprocess
import time

BASE_DIR = '/Users/pingwin/Desktop/GAMEREPO'
PUBLIC_GAMES_DIR = os.path.join(BASE_DIR, 'public/games')

def run_cmd(cmd):
    print(f"Running: {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=BASE_DIR)

def chunk_push():
    # 1. Add all non-game files first (json, scripts, etc)
    print("Committing metadata and scripts...")
    run_cmd('git add src/data/games.json')
    # Add generated html pages
    run_cmd('git add games/')
    # Add any scripts if modified (ignore errors if clean)
    try:
        run_cmd('git commit -m "Update games metadata and generated pages"')
        run_cmd('git push')
    except subprocess.CalledProcessError:
        print("Nothing to commit for metadata/scripts or push failed, continuing...")

    # 2. Iterate through public/games and commit each game folder individually
    if not os.path.exists(PUBLIC_GAMES_DIR):
        print("No public/games directory found.")
        return

    games = sorted(os.listdir(PUBLIC_GAMES_DIR))
    total = len(games)
    
    for i, game in enumerate(games):
        game_path = os.path.join(PUBLIC_GAMES_DIR, game)
        if not os.path.isdir(game_path):
            continue

        print(f"[{i+1}/{total}] Processing {game}...")
        
        # Add game folder
        run_cmd(f'git add "public/games/{game}"')
        
        # Add corresponding image if exists
        # Image path: public/cache/data/image/game/{game}/
        img_dir = f"public/cache/data/image/game/{game}"
        if os.path.exists(os.path.join(BASE_DIR, img_dir)):
            run_cmd(f'git add "{img_dir}"')

        # Commit
        try:
            run_cmd(f'git commit -m "Add game: {game}"')
        except subprocess.CalledProcessError:
             print(f"Nothing to commit for {game}")

        # Push (attempt even if commit failed, in case of pending commits)
        try:
            run_cmd('git push') 
        except subprocess.CalledProcessError:
             print(f"Push failed for {game}, will retry later.")

    print("Chunked push complete.")

if __name__ == "__main__":
    chunk_push()
