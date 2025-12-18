export function updateSEO({ title, description, image, url }) {
    // Update Title
    if (title) {
        document.title = title;
        setMetaTag('property', 'og:title', title);
        setMetaTag('property', 'twitter:title', title);
    }

    // Update Description
    if (description) {
        setMetaTag('name', 'description', description);
        setMetaTag('property', 'og:description', description);
        setMetaTag('property', 'twitter:description', description);
    }

    // Update Image
    if (image) {
        // Resolve relative paths if necessary, but ideally we pass absolute or full URLs
        // For this static setup, we might need to prepend base URL if not present.
        // Assuming 'image' is relative to root (./public/...) or absolute.
        const fullImageUrl = image.startsWith('http') ? image : new URL(image, window.location.origin + window.location.pathname).href;

        setMetaTag('property', 'og:image', fullImageUrl);
        setMetaTag('property', 'twitter:image', fullImageUrl);
    }

    // Update URL
    if (url) {
        setMetaTag('property', 'og:url', url);
        setMetaTag('property', 'twitter:url', url);
    }
}

function setMetaTag(attr, key, value) {
    let element = document.querySelector(`meta[${attr}="${key}"]`);
    if (!element) {
        element = document.createElement('meta');
        element.setAttribute(attr, key);
        document.head.appendChild(element);
    }
    element.setAttribute('content', value);
}
