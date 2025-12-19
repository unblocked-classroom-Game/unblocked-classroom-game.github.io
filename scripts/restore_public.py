import os
import shutil

BASE_DIR = '/Users/pingwin/Desktop/GAMEREPO'
GAMES_DIR = os.path.join(BASE_DIR, 'games')
PUBLIC_GAMES_DIR = os.path.join(BASE_DIR, 'public/games')

def restore_public_games():
    if not os.path.exists(PUBLIC_GAMES_DIR):
        os.makedirs(PUBLIC_GAMES_DIR)

    # 1. Find all *_files folders in games/
    for item in os.listdir(GAMES_DIR):
        if item.endswith('_files') and os.path.isdir(os.path.join(GAMES_DIR, item)):
            slug = item.replace('_files', '')
            src_path = os.path.join(GAMES_DIR, item)
            dest_path = os.path.join(PUBLIC_GAMES_DIR, slug)
            
            print(f"Restoring {slug} to {dest_path}...")
            
            # Move the folder content
            if os.path.exists(dest_path):
                print(f"  Warning: Destination {dest_path} exists. Merging/Overwriting.")
                # shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                # shutil.rmtree(src_path) 
                # Better to just move internal contents or use move if dest empty?
                # simpler: delete dest and move src
                shutil.rmtree(dest_path)
                shutil.move(src_path, dest_path)
            else:
                shutil.move(src_path, dest_path)
                
            # 2. Update the wrapper HTML in games/<slug>.html
            # It currently points to "<slug>_files/index.html"
            # It SHOULD point to "<slug>/index.html" because in dist/, 
            # games/<slug>.html and public/games/<slug> will be merged into dist/games/
            
            html_file = os.path.join(GAMES_DIR, f"{slug}.html")
            if os.path.exists(html_file):
                with open(html_file, 'r') as f:
                    content = f.read()
                
                # Replace OLD logic path
                old_src_1 = f"src=\"{slug}_files/index.html\""
                # Also handling the very original broken path if any remain
                old_src_2 = f"src=\"../public/games/{slug}/index.html\""
                
                new_src = f"src=\"{slug}/index.html\""
                
                content_fixed = content.replace(old_src_1, new_src).replace(old_src_2, new_src)
                
                if content != content_fixed:
                    print(f"  Updating wrapper {html_file}...")
                    with open(html_file, 'w') as f:
                        f.write(content_fixed)
            else:
                print(f"  Warning: Wrapper {html_file} not found.")

    print("Restoration complete.")

if __name__ == "__main__":
    restore_public_games()
