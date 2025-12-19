import { getGameBySlug, getAllGames } from '../store.js';
import { updateSEO } from '../utils/seo.js';

export function renderPlayer(container, slug) {
  const game = getGameBySlug(slug);

  if (!game) {
    console.error("Game not found for slug:", slug);
    container.innerHTML = `<div class="error-state"><h2>Game not found</h2><a href="#/" class="btn-back">Go Home</a></div>`;
    return;
  }
  console.log("Rendering player for:", game);

  updateSEO({
    title: `${game.name} - Play Online for Free`,
    description: game.description || `Play ${game.name} online for free. one of the best ${game.category || 'Arcade'} games. No downloads required!`,
    image: game.image,
    url: window.location.href
  });

  try {
    const section = document.createElement('section');
    section.className = 'player-layout'; // Use new layout class

    // Get random Games for "More Games"
    const allGames = getAllGames();
    const otherGames = allGames.filter(g => g.slug !== slug).sort(() => 0.5 - Math.random()).slice(0, 6);

    section.innerHTML = `
      <div class="player-main">
        <div class="player-header">
          <a href="#/" class="btn-back">
            <span class="icon">arrow_back</span> Back
          </a>
          <h2>${game.name}</h2>
        </div>
        
        <div class="game-wrapper">
          <div class="iframe-container"></div>
          <div class="game-controls">
            <button id="btn-fullscreen" class="control-btn">
              <span class="icon">fullscreen</span> Fullscreen
            </button>
             <div class="rating">
                <span class="icon">❤️</span> 95%
             </div>
          </div>
        </div>

        <div class="game-info">
          <h3>About ${game.name}</h3>
          <p>${game.description || `Play ${game.name} online for free. This is a popular ${game.category || 'Arcade'} game.`}</p>
          
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
          ${otherGames.map(g => `
            <a href="#/game/${g.slug}" class="related-card">
              <img src="${g.image}" alt="${g.name}" loading="lazy" />
              <div class="info">
                <h4>${g.name}</h4>
                <span>${g.category || 'Game'}</span>
              </div>
            </a>
          `).join('')}
        </div>
      </aside>
    `;

    // Create iframe programmatically
    const iframe = document.createElement('iframe');

    let gameUrl;
    // Check if ID is a GameDistribution GUID (32 hex chars). 
    // If not, assume it's a local game residing in /games/{slug}/
    const isGameDistribution = /^[a-f0-9]{32}$/i.test(game.id);

    if (isGameDistribution) {
      gameUrl = `https://html5.gamedistribution.com/${game.id}/`;
    } else {
      // Local game
      gameUrl = `games/${game.slug}/index.html`;
    }

    iframe.src = gameUrl;
    iframe.id = 'game-frame';
    iframe.frameBorder = '0';
    iframe.scrolling = 'no';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = "no-referrer";
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.background = "white";

    // Sandbox options
    // For local games, we might need slightly different permissions, but this set is generally permissive enough.
    iframe.sandbox = "allow-scripts allow-same-origin allow-popups allow-forms allow-pointer-lock allow-top-navigation-by-user-activation";
    iframe.allow = "autoplay; fullscreen; monetization; clipboard-write; web-share; accelerometer; magnetometer; gyroscope; display-capture";

    // Append to wrapper
    const wrapper = section.querySelector('.iframe-container');
    if (wrapper) wrapper.appendChild(iframe);

    // Fullscreen Logic
    const btnFullscreen = section.querySelector('#btn-fullscreen');
    btnFullscreen.addEventListener('click', () => {
      if (iframe.requestFullscreen) {
        iframe.requestFullscreen();
      } else if (wrapper.requestFullscreen) {
        wrapper.requestFullscreen();
      }
    });

    container.appendChild(section);
  } catch (err) {
    console.error("Render Error:", err);
    container.innerHTML = `<div class="error-state">
          <h2>Error Loading Game</h2>
          <p>Please try refreshing the page.</p>
          <a href="#/" class="btn-back">Go Home</a>
      </div>`;
  }
}
