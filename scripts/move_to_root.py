import os
import shutil

# Paths
BASE_DIR = os.getcwd()
PUBLIC_GAMES_DIR = os.path.join(BASE_DIR, "public", "games")
TARGET_GAMES_DIR = os.path.join(BASE_DIR, "games")

def move_games_to_root():
    if not os.path.exists(PUBLIC_GAMES_DIR):
        print(f"Source directory {PUBLIC_GAMES_DIR} does not exist.")
        return

    # Ensure target directory exists (it should, as it has wrappers)
    if not os.path.exists(TARGET_GAMES_DIR):
        os.makedirs(TARGET_GAMES_DIR)

    games = [d for d in os.listdir(PUBLIC_GAMES_DIR) if os.path.isdir(os.path.join(PUBLIC_GAMES_DIR, d))]
    
    print(f"Found {len(games)} games to move from public/games to games/...")

    for game in games:
        src_path = os.path.join(PUBLIC_GAMES_DIR, game)
        dst_path = os.path.join(TARGET_GAMES_DIR, game)

        if os.path.exists(dst_path):
            print(f"Target {dst_path} exists. Removing it first...")
            shutil.rmtree(dst_path)
        
        print(f"Moving {game} -> games/{game}")
        shutil.move(src_path, dst_path)

    # Check if empty
    if not os.listdir(PUBLIC_GAMES_DIR):
        print("Removing empty public/games directory")
        os.rmdir(PUBLIC_GAMES_DIR)

if __name__ == "__main__":
    move_games_to_root()
