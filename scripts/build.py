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

# Ensure games directory exists
if not os.path.exists(GAMES_DIR):
    os.makedirs(GAMES_DIR)

# 1. Read Data
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    games = json.load(f)

with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
    template = f.read()

# Sitemap Storage
sitemap_urls = []
base_url = "https://pingwin-w.github.io/GameBLOCK.github.io"

# 2. No need to copy assets (we are in root)

# 3. Helper to Generate Grid Pages
def generate_grid_page(games_list, page_title, output_filename, active_nav='', seo_title='', seo_desc=''):
    print(f'Generating {output_filename}...')
    
    # Defaults
    if not seo_title:
        seo_title = f"{page_title} - Modern Game Portal"
    if not seo_desc:
        seo_desc = "Play the best free online games at Modern Game Portal. Discover arcade, puzzle, and action games in a premium, ad-free environment."
    seo_image = f"{base_url}/public/cache/data/image/options/geometry_dash.png"
    seo_url = f"{base_url}/{output_filename}"
    seo_keywords = "online games, free games, arcade games, puzzle games, browser games, html5 games"
    
    # Add to sitemap
    sitemap_urls.append(seo_url)
    
    games_html_list = []
    for game in games_list:
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

    page_html = f'''
      <section class="home-page">
        <header class="page-header">
          <h2>{page_title}</h2>
          <div class="search-bar">
            <input type="text" placeholder="Search games..." />
          </div>
        </header>
        <div class="games-grid">
          {games_grid_html}
        </div>
      </section>
    '''

    # Replacement string matches current template.html structure with extra newlines
    target_string = '<main id="main-content" class="main-content">\n        <!-- Content will be injected here -->\n\n\n      </main>'
    if target_string not in template:
        # Fallback if whitespace differs slightly - try the original single version just in case, or a regex
        # But for now let's try the likely one. If this fails, we might need a smarter replacement.
        # Let's actually use a regex to be safe suitable for this simple case
        page_content = re.sub(
            r'<main id="main-content" class="main-content">.*?</main>', 
            f'<main id="main-content" class="main-content">{page_html}</main>', 
            template, 
            flags=re.DOTALL
        )
    else:
        page_content = template.replace(target_string, f'<main id="main-content" class="main-content">{page_html}</main>')

    
    # Set Active Nav State
    # Note: This is simple string replacement, might be brittle if classes change
    if active_nav == 'home':
         page_content = page_content.replace('href="./index.html" class="nav-item"', 'href="./index.html" class="nav-item active"')
    elif active_nav == 'popular':
         page_content = page_content.replace('href="./popular.html" class="nav-item"', 'href="./popular.html" class="nav-item active"')
    elif active_nav == 'new':
         page_content = page_content.replace('href="./new.html" class="nav-item"', 'href="./new.html" class="nav-item active"')

    # Inject SEO
    page_content = page_content.replace('%TITLE%', seo_title)
    page_content = page_content.replace('%DESCRIPTION%', seo_desc)
    page_content = page_content.replace('%IMAGE%', seo_image)
    page_content = page_content.replace('%URL%', seo_url)
    page_content = page_content.replace('%KEYWORDS%', seo_keywords)
    page_content = page_content.replace('%CANONICAL_URL%', seo_url)

    # CRITICAL: Remove main.js from popular/new pages to prevent SPA from overwriting static content
    # We want these pages to be pure static HTML
    if output_filename in ['popular.html', 'new.html'] or output_filename.startswith('games/'):
         page_content = page_content.replace('<script type="module" src="./src/main.js"></script>', '')
         page_content = page_content.replace('<script type="module" src="../src/main.js"></script>', '') # For subdirectories

    with open(os.path.join(BASE_DIR, output_filename), 'w', encoding='utf-8') as f:
        f.write(page_content)

# 3.6 Generate ads.txt
def generate_ads_txt():
    # Deprecated: Do not regenerate ads.txt as it contains user ID now
    if not os.path.exists(os.path.join(BASE_DIR, 'ads.txt')):
         print('Generating ads.txt placeholder...')
         content = "google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0"
         with open(os.path.join(BASE_DIR, 'ads.txt'), 'w', encoding='utf-8') as f:
            f.write(content)

# SKIP generate_ads_txt to preserve manual edits
# generate_ads_txt()


# Generate Home (Default Order)
generate_grid_page(games, 'All Games', 'index.html', active_nav='home', 
                   seo_title="Modern Game Portal - Play Best Free Online Games",
                   seo_desc="Play the best free online games at Modern Game Portal. Discover arcade, puzzle, and action games in a premium, ad-free environment. Play now without downloads!")

# Generate Popular (Shuffle)
import random
popular_games = games.copy()
random.shuffle(popular_games)
generate_grid_page(popular_games, 'Popular Games', 'popular.html', active_nav='popular')

# Generate New (Reverse Order)
new_games = games.copy()
new_games.reverse()
generate_grid_page(new_games, 'New Games', 'new.html', active_nav='new')



# Generate Category Pages
categories = list(set([g.get('category', 'Arcade') for g in games]))

# Add manual mapping if needed or just slugify
def get_cat_slug(cat_name):
    return cat_name.lower().replace(' ', '-')

for cat in categories:
    cat_slug = get_cat_slug(cat)
    # Filter games for this category
    cat_games = [g for g in games if g.get('category', 'Arcade') == cat]
    generate_grid_page(cat_games, f'{cat} Games', f'{cat_slug}.html', active_nav=cat_slug)

# Ensure specific requested category pages exist even if empty/mapped
# 'Action', 'Arcade', 'Puzzle', 'Racing', 'Sports'
requested_cats = ['Action', 'Arcade', 'Puzzle', 'Racing', 'Sports']
for req_cat in requested_cats:
    req_slug = get_cat_slug(req_cat)
    if not os.path.exists(os.path.join(BASE_DIR, f'{req_slug}.html')):
        print(f"Generating fallback page for {req_cat}...")
        # Fallback: shows all games or a subset if real category missing
        # For now, show all games but title it correctly
        generate_grid_page(games, f'{req_cat} Games', f'{req_slug}.html', active_nav=req_slug)

# 3.5 Helper to Generate Content Pages

def generate_content_page(title, content_html, output_filename, seo_title='', seo_desc=''):
    print(f'Generating {output_filename}...')
    
    if not seo_title:
        seo_title = f"{title} - Modern Game Portal"
    if not seo_desc:
        seo_desc = f"{title} for Modern Game Portal."
    
    seo_image = f"{base_url}/public/cache/data/image/options/geometry_dash.png"
    seo_url = f"{base_url}/{output_filename}"
    
    # Add to sitemap
    sitemap_urls.append(seo_url)
    
    page_html = f'''
      <section class="content-page" style="max-width: 800px; margin: 0 auto; padding: 2rem;">
        <header class="page-header">
          <h2>{title}</h2>
        </header>
        <div class="glass-panel" style="background: var(--glass); padding: 2rem; border-radius: var(--radius); border: 1px solid var(--glass-border);">
          {content_html}
        </div>
      </section>
    '''

    # Replacement string matches current template.html structure with extra newlines
    # Using regex for robustness as defined above
    page_content = re.sub(
        r'<main id="main-content" class="main-content">.*?</main>', 
        f'<main id="main-content" class="main-content">{page_html}</main>', 
        template, 
        flags=re.DOTALL
    )

    
    # SEO
    page_content = page_content.replace('%TITLE%', seo_title)
    page_content = page_content.replace('%DESCRIPTION%', seo_desc)
    page_content = page_content.replace('%IMAGE%', seo_image)
    page_content = page_content.replace('%URL%', seo_url)
    page_content = page_content.replace('%KEYWORDS%', "privacy policy, terms of service, contact, about us")
    page_content = page_content.replace('%CANONICAL_URL%', seo_url)

    with open(os.path.join(BASE_DIR, output_filename), 'w', encoding='utf-8') as f:
        f.write(page_content)

# Content for Pages
privacy_content = '''
<h3>1. Introduction</h3>
<p>Welcome to Modern Game Portal. We respect your privacy and are committed to protecting your personal data.</p>
<h3>2. Data Collection</h3>
<p>We do not collect personal data directly. We use third-party services like Google AdSense and Google Analytics which may use cookies to serve ads and analyze traffic.</p>
<h3>3. Cookies</h3>
<p>Cookies are small text files stored on your device. You can disable cookies in your browser settings. By using our site, you consent to our use of cookies.</p>
<h3>4. Third-Party Links</h3>
<p>Our website contains links to other sites. We are not responsible for the privacy practices of those sites.</p>
<h3>5. Contact</h3>
<p>If you have questions, please contact us at info@example.com.</p>
'''

terms_content = '''
<h3>1. Acceptance of Terms</h3>
<p>By accessing Modern Game Portal, you agree to be bound by these Terms of Service.</p>
<h3>2. Use License</h3>
<p>Permission is granted to play games on Modern Game Portal for personal, non-commercial transitory viewing only.</p>
<h3>3. Disclaimer</h3>
<p>The materials on Modern Game Portal are provided on an 'as is' basis. We make no warranties, expressed or implied.</p>
<h3>4. Limitations</h3>
<p>In no event shall Modern Game Portal be liable for any damages arising out of the use or inability to use the materials on our website.</p>
'''

about_content = '''
<h3>About Modern Game Portal</h3>
<p>Modern Game Portal is your ultimate destination for free online gaming. We provide a safe, secure, and family-friendly environment where you can play the best HTML5 games without any downloads or installations.</p>
<h4>Our Mission</h4>
<p>We aim to bring the highest quality games to your browser. From intense action games to brain-teasing puzzles, our collection is curated to ensure you have the best experience possible.</p>
<h4>Why Choose Us?</h4>
<ul>
<li><strong>No Downloads:</strong> Play instantly in your web browser.</li>
<li><strong>Cross-Platform:</strong> Works on Desktop, Tablet, and Mobile.</li>
<li><strong>Safe & Secure:</strong> All games are tested for safety.</li>
</ul>
'''

contact_content = '''
<h3>Contact Information</h3>
<p>We value your feedback! valid concerns, or DMCA requests should be directed to our support team.</p>
<div style="margin-top: 2rem;">
    <p><strong>General Inquiries:</strong> joe6nen@gmail.com</p>
    <p><strong>Support:</strong> joe6nen@gmail.com</p>
    <p><strong>Business:</strong> joe6nen@gmail.com</p>
</div>
<div style="margin-top: 2rem; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 8px;">
    <h4>Report an Issue</h4>
    <p>If you encounter a bug or inappropriate content, please report it immediately with the game URL.</p>
</div>
'''

# Generate Content Pages
generate_content_page('Privacy Policy', privacy_content, 'privacy.html')
generate_content_page('Terms of Service', terms_content, 'terms.html')
generate_content_page('About Us', about_content, 'about.html')
generate_content_page('Contact Us', contact_content, 'contact.html')


# 4. Generate Game Pages
print('Generating game pages...')

for game in games:
    game_id = game.get('id', '')
    name = game.get('name', 'Unknown')
    slug = game.get('slug', 'unknown')
    
    if not game_id:
        print(f"Skipping {name} - no ID")
        continue

    # Determine URL: Check if local folder exists with index.html
    # We look for a folder named '{slug}_files' inside games directory
    # OR we look for the old public/games style if applicable, but we prefer checking GAMES_DIR
    local_game_index = os.path.join(GAMES_DIR, f"{slug}_files", "index.html")
    
    if os.path.exists(local_game_index):
        game_url = f"{slug}_files/index.html"
    else:
        game_url = f"https://html5.gamedistribution.com/{game_id}/"

    # Select 6 random other games for sidebar
    import random
    other_games = [g for g in games if g.get('slug') != slug]
    random.shuffle(other_games)
    sidebar_games = other_games[:6]
    
    sidebar_html_list = []
    for bg in sidebar_games:
        bg_name = bg.get('name', 'Game')
        bg_slug = bg.get('slug', '')
        bg_cat = bg.get('category', 'Game')
        bg_img = bg.get('image', '')
        # Fix relative image path for subplot
        if bg_img.startswith('./'):
             bg_img = '.' + bg_img 
        
        sidebar_html_list.append(f'''
            <a href="../games/{bg_slug}.html" class="related-card">
              <img src="{bg_img}" alt="{bg_name}" loading="lazy" />
              <div class="info">
                <h4>{bg_name}</h4>
                <span>{bg_cat}</span>
              </div>
            </a>
        ''')
    sidebar_html = ''.join(sidebar_html_list)

    # Game Description
    g_desc_text = game.get('description', '')
    if not g_desc_text:
        g_desc_text = f"Play {name} online for free. This is a popular {game.get('category','Arcade')} game."

    player_html = f'''
  <section class="player-layout">
      <div class="player-main">
        <div class="player-header">
          <a href="../index.html" class="btn-back">
            <span class="icon">arrow_back</span> Back
          </a>
          <h2>{name}</h2>
        </div>
        
        <div class="game-wrapper">
          <div class="iframe-container">
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
          <h3>About {name}</h3>
          <p>{g_desc_text}</p>
          
          <div class="instructions">
             <h3>How to Play</h3>
             <ul>
               <li>Click "Play" to start.</li>
               <li>Use Mouse or Keyboard to control.</li>
               <li>Complete objectives and earn high scores!</li>
             </ul>
          </div>
        </div>
      </div>

      <aside class="player-sidebar">
        <h3>You May Also Like</h3>
        <div class="related-games-list">
          {sidebar_html}
        </div>
      </aside>
    </section>
'''

    page_content = re.sub(
        r'<main id="main-content" class="main-content">.*?</main>', 
        f'<main id="main-content" class="main-content">{player_html}</main>', 
        template, 
        flags=re.DOTALL
    )

    
    # Game SEO Data
    g_title = f"{name} - Play Online for Free"
    g_desc = game.get('description', '')
    if not g_desc:
        g_desc = f"Play {name} online for free. One of the best {game.get('category','Arcade')} games. No downloads required!"
    
    # Fix image path for SEO (make absolute if possible, or at least relative correctly)
    # The image path is like /cache/... or ./public/...
    # Ideally use absolute URL for OG tags
    g_image = game.get('image', '')
    if g_image.startswith('./'):
        g_image = g_image[1:] # remove dot, keep /public...
    
    full_image_url = f"{base_url}{g_image}"
    full_page_url = f"{base_url}/games/{slug}.html"
    
    # Add to sitemap
    sitemap_urls.append(full_page_url)
    
    page_content = page_content.replace('%TITLE%', g_title)
    page_content = page_content.replace('%DESCRIPTION%', g_desc)
    page_content = page_content.replace('%IMAGE%', full_image_url)
    page_content = page_content.replace('%URL%', full_page_url)
    page_content = page_content.replace('%KEYWORDS%', f"play {name}, {name} game, free online games, {game.get('category','Arcade')} games")
    page_content = page_content.replace('%CANONICAL_URL%', full_page_url)

    # Fix resource paths for subdirectory
    # We need to change ./src/ -> ../src/ and ./public/ -> ../public/
    page_content = page_content.replace('href="./src/', 'href="../src/')
    page_content = page_content.replace('src="./src/', 'src="../src/')
    page_content = page_content.replace('href="./public/', 'href="../public/')
    page_content = page_content.replace('src="./public/', 'src="../public/')
    
    # Fix Sidebar Links for subdirectory
    page_content = page_content.replace('href="./index.html"', 'href="../index.html"')
    page_content = page_content.replace('href="./popular.html"', 'href="../popular.html"')
    page_content = page_content.replace('href="./new.html"', 'href="../new.html"')

    with open(os.path.join(GAMES_DIR, f'{slug}.html'), 'w', encoding='utf-8') as f:
        f.write(page_content)

# 5. Generate Sitemap
print('Generating sitemap.xml...')
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_content += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2025-12-18</lastmod>\n  </url>\n'
sitemap_content += '</urlset>'

with open(os.path.join(BASE_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

print(f'Build complete! Output in root. Generated sitemap with {len(sitemap_urls)} URLs.')
