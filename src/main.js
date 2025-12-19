import { fetchGames } from './store.js';
import { renderLayout } from './components/Layout.js';
import { initRouter } from './router.js';

// Initialize the application
async function init() {
  const app = document.getElementById('app');

  // ABORT if on a static policy page (privacy, terms, about, contact)
  // This prevents the SPA router from wiping the static content
  const path = window.location.pathname;
  if (path.includes('privacy') ||
    path.includes('terms') ||
    path.includes('about') ||
    path.includes('contact') ||
    path.includes('popular') ||
    path.includes('new') ||
    path.includes('/games/')) {
    console.log('Static page detected, skipping SPA init');
    return;
  }

  // Show loading state
  app.innerHTML = '<div style="display:flex;justify-content:center;align-items:center;width:100%;height:100vh;">Loading assets...</div>';

  // Show loading state
  app.innerHTML = '<div style="display:flex;justify-content:center;align-items:center;width:100%;height:100vh;">Loading assets...</div>';

  try {
    // 1. Fetch Data
    await fetchGames();

    // 2. Render Layout (Sidebar + Main Content Area)
    app.innerHTML = '';
    renderLayout(app);

    // 3. Initialize Router (Handles rendering the correct page into Main Content)
    initRouter();

  } catch (error) {
    console.error("Failed to init app:", error);
    app.innerHTML = `<div style="padding:2rem;color:red;">Error loading application: ${error.message}</div>`;
  }
}

init();
