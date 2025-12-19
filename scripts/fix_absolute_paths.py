import os

BASE_DIR = '/Users/pingwin/Desktop/GAMEREPO/games'

def fix_absolute_paths():
    print("Scanning for absolute paths...")
    
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check for common absolute paths found in the grep
                # src="/js/main.js" -> src="js/main.js"
                # href="/favicon.ico" -> href="favicon.ico"
                
                new_content = content
                
                # Replace src="/... with src="... (relative)
                # We need to be careful not to replace src="//" (protocol relative)
                # So we look for src="/[a-zA-Z]
                
                # Specific replacements based on grep findings
                replacements = [
                    ('src="/js/main.js"', 'src="js/main.js"'),
                    ('href="/favicon.ico"', 'href="favicon.ico"'),
                    ('src="/assets/', 'src="assets/'),
                    ('href="/assets/', 'href="assets/'),
                    ('src="/img/', 'src="img/'),
                    ('href="/img/', 'href="img/'),
                ]
                
                changed = False
                for old, new in replacements:
                    if old in new_content:
                        new_content = new_content.replace(old, new)
                        changed = True
                        print(f"  Fixed {old} in {file_path}")
                
                if changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

    print("Absolute path fix complete.")

if __name__ == "__main__":
    fix_absolute_paths()
