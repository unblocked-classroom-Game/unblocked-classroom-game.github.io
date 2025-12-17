import os
import json
import shutil
import re

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
GAMES_DIR = os.path.join(BASE_DIR, 'games')
DATA_FILE = os.path.join(SRC_DIR, 'data', 'games.json')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'template.html')

print('Starting static site generation (Root Mode)...')

# Ensure games directory exists and is clean
if os.path.exists(GAMES_DIR):
    shutil.rmtree(GAMES_DIR)
os.makedirs(GAMES_DIR)

# 1. Read Data
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    games = json.load(f)

with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    template = f.read()

# 2. No need to copy assets (we are in root)

# 3. Generate Index Page
print('Generating index.html...')

# Generate Game Cards HTML
games_html_list = []
for game in games:
    category = game.get('category', 'Arcade')
    name = game.get('name', 'Unknown')
    slug = game.get('slug', 'unknown')
    image = game.get('image', '')
    
    card_html = f'''
  <a href="./games/{slug}.html" class="game-card" style="animation: fadeIn 0.5s ease;">
    <div class="card-image">
      <img src="{image}" alt="{name}" loading="lazy" />
      <div class="card-overlay">
        <span class="play-icon">▶</span>
      </div>
    </div>
    <div class="card-info">
      <h3>{name}</h3>
      <span class="category">{category}</span>
    </div>
  </a>
'''
    games_html_list.append(card_html)

games_grid_html = ''.join(games_html_list)

home_page_html = f'''
  <section class="home-page">
    <header class="page-header">
      <h2>All Games</h2>
      <div class="search-bar">
        <input type="text" placeholder="Search games..." />
      </div>
    </header>
    <div class="games-grid">
      {games_grid_html}
    </div>
  </section>
'''


index_content = template.replace(
    '<main id="main-content" class="main-content">\n        <!-- Content will be injected here -->\n      </main>',
    f'<main id="main-content" class="main-content">{home_page_html}</main>'
)
with open(os.path.join(BASE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_content)


# 4. Generate Game Pages
print('Generating game pages...')

for game in games:
    game_id = game.get('id', '')
    name = game.get('name', 'Unknown')
    slug = game.get('slug', 'unknown')
    
    if not game_id:
        print(f"Skipping {name} - no ID")
        continue

    game_url = f"https://html5.gamedistribution.com/{game_id}/"

    player_html = f'''
  <section class="player-page">
      <div class="player-header">
        <a href="../index.html" class="btn-back">
          <span class="icon">arrow_back</span> Back
        </a>
        <h2>{name}</h2>
      </div>
      <div class="game-container">
        <div class="iframe-wrapper">
           <iframe 
              src="{game_url}" 
              id="game-frame" 
              frameborder="0" 
              scrolling="no" 
              allowfullscreen 
              referrerpolicy="no-referrer" 
              style="width: 100%; height: 100%; background: white;"
              sandbox="allow-scripts allow-same-origin allow-popups allow-forms allow-pointer-lock allow-top-navigation-by-user-activation"
              allow="autoplay; fullscreen; monetization; clipboard-write; web-share; accelerometer; magnetometer; gyroscope; display-capture">
           </iframe>
        </div>
      </div>
    </section>
'''

    page_content = template.replace(
        '<main id="main-content" class="main-content">\n        <!-- Content will be injected here -->\n      </main>',
        f'<main id="main-content" class="main-content">{player_html}</main>'
    )

    # Fix resource paths for subdirectory
    # We need to change ./src/ -> ../src/ and ./public/ -> ../public/
    page_content = page_content.replace('href="./src/', 'href="../src/')
    page_content = page_content.replace('src="./src/', 'src="../src/')
    page_content = page_content.replace('href="./public/', 'href="../public/')
    page_content = page_content.replace('src="./public/', 'src="../public/')
    
    # Fix Sidebar Links for subdirectory
    page_content = page_content.replace('href="./index.html"', 'href="../index.html"')

    with open(os.path.join(GAMES_DIR, f'{slug}.html'), 'w', encoding='utf-8') as f:
        f.write(page_content)

print('Build complete! Output in root.')
