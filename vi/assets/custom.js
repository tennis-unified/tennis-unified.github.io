// Breadcrumbs generator for MkDocs
document.addEventListener('DOMContentLoaded', function() {
    // Get current path
    const path = window.location.pathname;
    const segments = path.split('/').filter(s => s && s !== 'tennisknowledgebase');
    
    if (segments.length === 0) return; // Home page, no breadcrumbs needed
    
    // Create breadcrumbs container
    const container = document.createElement('div');
    container.id = 'breadcrumbs-container';
    
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'breadcrumb');
    
    const ol = document.createElement('ol');
    ol.style.cssText = 'list-style: none; padding: 0.75rem 1rem; margin: 0; background: #f8f9fa; border-radius: 4px; border: 1px solid #e0e0e0; display: flex; flex-wrap: wrap; gap: 0.5rem;';
    
    // Home link
    const homeLi = document.createElement('li');
    homeLi.style.display = 'inline';
    homeLi.innerHTML = '<a href="/tennisknowledgebase/" style="color: #306998; text-decoration: none; font-weight: 500;">🏠 Home</a>';
    ol.appendChild(homeLi);
    
    // Build breadcrumb trail from path segments
    let buildPath = '';
    for (let i = 0; i < segments.length - 1; i++) {
        const segment = decodeURIComponent(segments[i]);
        buildPath += segment + '/';
        
        const li = document.createElement('li');
        li.style.display = 'inline';
        
        const separator = document.createElement('span');
        separator.style.cssText = 'color: #6c757d; margin: 0 0.25rem;';
        separator.textContent = '›';
        li.appendChild(separator);
        
        const link = document.createElement('a');
        link.href = '/tennisknowledgebase/' + buildPath;
        link.style.cssText = 'color: #306998; text-decoration: none; font-weight: 500;';
        link.textContent = segment;
        li.appendChild(link);
        
        ol.appendChild(li);
    }
    
    // Current page (last segment, not a link)
    const currentPage = decodeURIComponent(segments[segments.length - 1]) || 'Home';
    const currentLi = document.createElement('li');
    currentLi.style.display = 'inline';
    
    const separator = document.createElement('span');
    separator.style.cssText = 'color: #6c757d; margin: 0 0.25rem;';
    separator.textContent = '›';
    currentLi.appendChild(separator);
    
    const currentSpan = document.createElement('span');
    currentSpan.style.cssText = 'color: #6c757d;';
    currentSpan.textContent = currentPage;
    currentLi.appendChild(currentSpan);
    
    ol.appendChild(currentLi);
    nav.appendChild(ol);
    container.appendChild(nav);
    
    // Insert before main content
    const mainContent = document.querySelector('main') || document.querySelector('[role="main"]');
    if (mainContent) {
        mainContent.parentElement.insertBefore(container, mainContent);
    }
});