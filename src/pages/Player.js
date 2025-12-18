import { getGameBySlug } from '../store.js';
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
    section.className = 'player-page';

    section.innerHTML = `
      <div class="player-header">
        <a href="#/" class="btn-back">
          <span class="icon">arrow_back</span> Back
        </a>
        <h2>${game.name}</h2>
      </div>
      <div class="game-container">
        <div class="iframe-wrapper"></div>
      </div>
    `;

    // Create iframe programmatically
    const iframe = document.createElement('iframe');
    const gameUrl = `https://html5.gamedistribution.com/${game.id}/`;

    iframe.src = gameUrl;
    iframe.id = 'game-frame';
    iframe.frameBorder = '0';
    iframe.scrolling = 'no';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = "no-referrer"; // Hides the source domain
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.style.background = "white"; // Make it visible against black

    // Sandbox: IMPORTANT to prevent "block-and-redirect" scripts from navigating the top window
    // We allow 'allow-top-navigation-by-user-activation' to potentially fix the "not available" error
    // while still blocking auto-redirects.
    // Restored 'allow-same-origin' for game functionality (localStorage, etc.)
    iframe.sandbox = "allow-scripts allow-same-origin allow-popups allow-forms allow-pointer-lock allow-top-navigation-by-user-activation";
    iframe.allow = "autoplay; fullscreen; monetization; clipboard-write; web-share; accelerometer; magnetometer; gyroscope; display-capture";

    // Append to wrapper
    const wrapper = section.querySelector('.iframe-wrapper');
    if (!wrapper) throw new Error("Wrapper not found");

    wrapper.appendChild(iframe);

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
