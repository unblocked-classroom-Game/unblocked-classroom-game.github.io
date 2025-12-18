import { getAllGames } from '../store.js';
import { renderGameCard } from '../components/GameCard.js';
import { updateSEO } from '../utils/seo.js';

export function renderHome(container) {
  updateSEO({
    title: 'Modern Game Portal - Play Best Free Online Games',
    description: 'Play the best free online games at Modern Game Portal. Discover arcade, puzzle, and action games in a premium, ad-free environment. Play now without downloads!',
    image: './public/cache/data/image/options/geometry_dash.png',
    url: 'https://pingwin-w.github.io/GameBLOCK.github.io/'
  });
  const games = getAllGames();
  console.log("RenderHome: Games to render:", games);

  const section = document.createElement('section');
  section.className = 'home-page';

  const header = document.createElement('header');
  header.className = 'page-header';
  header.innerHTML = `
    <h2>All Games</h2>
    <div class="search-bar">
      <input type="text" placeholder="Search games..." />
    </div>
  `;

  const grid = document.createElement('div');
  grid.className = 'games-grid';

  games.forEach(game => {
    const card = renderGameCard(game);
    grid.appendChild(card);
  });

  section.appendChild(header);
  section.appendChild(grid);

  /* Search Logic */
  const searchInput = section.querySelector('input');
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const cards = grid.querySelectorAll('.game-card');
    let hasResults = false;

    cards.forEach(card => {
      const name = card.querySelector('h3').textContent.toLowerCase();
      if (name.includes(query)) {
        card.style.display = 'block';
        card.style.animation = 'fadeIn 0.3s ease';
        hasResults = true;
      } else {
        card.style.display = 'none';
      }
    });

    const noResultsMsg = grid.querySelector('.no-results');
    if (!hasResults) {
      if (!noResultsMsg) {
        const msg = document.createElement('div');
        msg.className = 'no-results';
        msg.style.gridColumn = '1 / -1';
        msg.style.textAlign = 'center';
        msg.style.padding = '2rem';
        msg.style.color = 'var(--color-text-dim)';
        msg.innerHTML = `<h3>No games found matching "${e.target.value}"</h3>`;
        grid.appendChild(msg);
      } else {
        noResultsMsg.querySelector('h3').textContent = `No games found matching "${e.target.value}"`;
        noResultsMsg.style.display = 'block';
      }
    } else if (noResultsMsg) {
      noResultsMsg.style.display = 'none';
    }
  });

  container.appendChild(section);
}
