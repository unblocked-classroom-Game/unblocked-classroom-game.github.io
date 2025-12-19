import os
import shutil

BASE_DIR = '/Users/pingwin/Desktop/GAMEREPO'
PUBLIC_GAMES_DIR = os.path.join(BASE_DIR, 'public/games')
GAMES_DIR = os.path.join(BASE_DIR, 'games')

def fix_all_games():
    if not os.path.exists(PUBLIC_GAMES_DIR):
        print("No public/games directory found.")
        return

    # List all games in public/games
    # These are the ones we migrated and need to move.
    # Note: vex3 is already moved, so it won't be in this list (or folder is empty/gone)
    
    games = sorted(os.listdir(PUBLIC_GAMES_DIR))
    
    for game_slug in games:
        src_path = os.path.join(PUBLIC_GAMES_DIR, game_slug)
        if not os.path.isdir(src_path):
            continue
            
        dest_path = os.path.join(GAMES_DIR, f"{game_slug}_files")
        
        print(f"Processing {game_slug}...")
        
        # 1. Move directory
        if os.path.exists(dest_path):
            print(f"  Destination {dest_path} already exists. Skipping move.")
        else:
            print(f"  Moving to {dest_path}...")
            shutil.move(src_path, dest_path)
            
        # 2. Update HTML wrapper
        html_file = os.path.join(GAMES_DIR, f"{game_slug}.html")
        if os.path.exists(html_file):
            with open(html_file, 'r') as f:
                content = f.read()
            
            # Replace the old src with new src
            # Old: ../public/games/{slug}/index.html
            # New: {slug}_files/index.html
            
            old_src = f"../public/games/{game_slug}/index.html"
            new_src = f"{game_slug}_files/index.html"
            
            if old_src in content:
                print(f"  Updating {game_slug}.html...")
                new_content = content.replace(old_src, new_src)
                with open(html_file, 'w') as f:
                    f.write(new_content)
            else:
                print(f"  Warning: Pattern '{old_src}' not found in {game_slug}.html")
        else:
             print(f"  Warning: {html_file} not found.")

    print("All done.")

if __name__ == "__main__":
    fix_all_games()
