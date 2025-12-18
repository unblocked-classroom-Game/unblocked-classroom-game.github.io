import { fetchGames } from './store.js';
import { renderLayout } from './components/Layout.js';
import { initRouter } from './router.js';

// Initialize the application
async function init() {
  const app = document.getElementById('app');

  // Check for static content - REMOVED to force router initialization for Dynamic SEO
  // if (app.children.length > 0) { ... }
  // We want the router to take over so we can handle SEO dynamically.

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
