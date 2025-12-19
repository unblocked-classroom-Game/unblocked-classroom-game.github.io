import os
import json
import shutil
from datetime import datetime

BASE_DIR = '/Users/pingwin/Desktop/GAMEREPO'
GAMES_JSON_PATH = os.path.join(BASE_DIR, 'src/data/games.json')
DEST_GAMES_DIR = os.path.join(BASE_DIR, 'games')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'template.html')

PLAYER_LAYOUT = """
  <section class="player-layout">
      <div class="player-main">
        <div class="player-header">
          <a href="../index.html" class="btn-back">
            <span class="icon">arrow_back</span> Back
          </a>
          <h2>%TITLE%</h2>
        </div>
        
        <div class="game-wrapper">
          <div class="iframe-container">
             <iframe 
               src="%IFRAME_SRC%" 
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
          <div class="game-controls">
            <button id="btn-fullscreen" class="control-btn" onclick="const iframe = document.getElementById('game-frame'); if(iframe.requestFullscreen) iframe.requestFullscreen();">
              <span class="icon">fullscreen</span> Fullscreen
            </button>
             <div class="rating">
                <span class="icon">❤️</span> 95%
             </div>
          </div>
        </div>

        <div class="game-info">
          <h3>About %TITLE%</h3>
          <p>Play %TITLE% unblocked. Experience the thrill of this popular game directly in your browser without any restrictions.</p>
          
          <div class="instructions">
             <h3>How to Play</h3>
             <ul>
               <li>Click "Play" to start.</li>
               <li>Follow on-screen instructions.</li>
               <li>Enjoy the game!</li>
             </ul>
          </div>
        </div>
      </div>

      <aside class="player-sidebar">
        <h3>You May Also Like</h3>
        <div class="related-games-list">
            <a href="../games/2048-classic.html" class="related-card">
              <div class="info">
                <h4>2048 Classic</h4>
                <span>Puzzle</span>
              </div>
            </a>
            <a href="../games/tunnel-road.html" class="related-card">
              <div class="info">
                <h4>Tunnel Road</h4>
                <span>Arcade</span>
              </div>
            </a>
        </div>
      </aside>
  </section>
"""

def regenerate():
    # Load data
    with open(GAMES_JSON_PATH, 'r') as f:
        games_data = json.load(f)

    # Load template
    with open(TEMPLATE_PATH, 'r') as f:
        template_content = f.read()

    count = 0
    for game in games_data:
        slug = game.get('slug')
        title = game.get('name')
        image_path = game.get('image', '').replace('./', '../') # Fix relative for games/ dir

        # Skip games that aren't the new ones if needed, OR regenerate all to be safe.
        # But wait, original legacy games might have different structure?
        # Let's target only the ones we know are new/broken if possible, OR check if html file is empty?
        # Safer to regenerate ALL if they follow the same slug structure.
        
        # NOTE: For safety, let's just regenerate all. The old games (2048-classic, tunnel-road) are static/migrated?
        # Games list includes 2048-classic, tunnel-road, etc.
        # "2048 Classic" slug is "2048-classic".
        # Let's ensure iframe src is correct.
        # Older games might not be in "public/games/slug".
        # 1. Check if public/games/slug exists.
        
        iframe_src = ""
        local_game_path = os.path.join(BASE_DIR, 'public/games', slug)
        
        if os.path.exists(local_game_path):
             iframe_src = f"../public/games/{slug}/index.html"
        else:
            # Fallback for old games? Or maybe they aren't in games.json this way?
            # Old games were in games/ folder directly or handled differently?
            # games.json has ALL games.
            # If public/games/slug doesn't exist, we might break old games if we overwrite their HTML.
            print(f"Skipping {slug}: No local folder found in public/games/")
            # Actually, standard games like '2048-classic' likely have different iframe source logic?
            # Wait, 2048-classic might be external? or iframe src?
            # Let's inspect an old game html first if unsure.
            continue
            
        # Generate content
        game_content = PLAYER_LAYOUT.replace('%TITLE%', title).replace('%IFRAME_SRC%', iframe_src)
        
        final_html = template_content
        final_html = final_html.replace('%CONTENT%', game_content)
        final_html = final_html.replace('%TITLE%', f"{title} - ublocked games")
        final_html = final_html.replace('%DESCRIPTION%', f"Play {title} unblocked at ublocked games.")
        final_html = final_html.replace('%KEYWORDS%', f"{title}, unblocked games, free games")
        final_html = final_html.replace('%CANONICAL_URL%', f"https://pingwin-w.github.io/GameBLOCK.github.io/games/{slug}.html")
        final_html = final_html.replace('%URL%', f"https://pingwin-w.github.io/GameBLOCK.github.io/games/{slug}.html")
        
        # Image fix
        final_html = final_html.replace('%IMAGE%', image_path)

        # Fix relative paths
        final_html = final_html.replace('href="./', 'href="../')
        final_html = final_html.replace('src="./', 'src="../')
        
        with open(os.path.join(DEST_GAMES_DIR, f"{slug}.html"), 'w') as f:
            f.write(final_html)
        
        count += 1
        print(f"Regenerated {slug}.html")

    print(f"Regenerated {count} pages.")

if __name__ == "__main__":
    regenerate()
