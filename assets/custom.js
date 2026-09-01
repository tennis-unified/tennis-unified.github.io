// Breadcrumbs generator for MkDocs
document.addEventListener('DOMContentLoaded', function() {
    // Get current path
    const path = window.location.pathname;
    const segments = path.split('/').filter(s => s && s !== 'tennisknowledgebase');
    
    // Create breadcrumbs container
    const container = document.createElement('div');
    container.id = 'breadcrumbs-container';
    
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'breadcrumb');
    
    const ol = document.createElement('ol');
    ol.className = 'tu-breadcrumbs';
    
    // Home link
    const homeLi = document.createElement('li');
    homeLi.className = 'tu-breadcrumbs__item';
    if (segments.length === 0) {
        // On home page - show as current
        const homeSpan = document.createElement('span');
        homeSpan.className = 'tu-breadcrumbs__current';
        homeSpan.textContent = '🏠 Home';
        homeLi.appendChild(homeSpan);
    } else {
        const homeLink = document.createElement('a');
        homeLink.href = '/';
        homeLink.className = 'tu-breadcrumbs__link';
        homeLink.textContent = '🏠 Home';
        homeLi.appendChild(homeLink);
    }
    ol.appendChild(homeLi);
    
    // Build breadcrumb trail from path segments
    if (segments.length > 0) {
        let buildPath = '';
        for (let i = 0; i < segments.length - 1; i++) {
            const segment = decodeURIComponent(segments[i]);
            buildPath += segment + '/';
            
            const li = document.createElement('li');
            li.className = 'tu-breadcrumbs__item';
            
            const separator = document.createElement('span');
            separator.className = 'tu-breadcrumbs__separator';
            separator.textContent = '›';
            li.appendChild(separator);
            
            const link = document.createElement('a');
            link.href = '/' + buildPath;
            link.className = 'tu-breadcrumbs__link';
            link.textContent = segment;
            li.appendChild(link);
            
            ol.appendChild(li);
        }
        
        // Current page (last segment, not a link)
        const currentPage = decodeURIComponent(segments[segments.length - 1]) || 'Home';
        const currentLi = document.createElement('li');
        currentLi.className = 'tu-breadcrumbs__item';
        
        const separator = document.createElement('span');
        separator.className = 'tu-breadcrumbs__separator';
        separator.textContent = '›';
        currentLi.appendChild(separator);
        
        const currentSpan = document.createElement('span');
        currentSpan.className = 'tu-breadcrumbs__current';
        currentSpan.textContent = currentPage;
        currentLi.appendChild(currentSpan);
        
        ol.appendChild(currentLi);
    }
    
    nav.appendChild(ol);
    container.appendChild(nav);
    
    // Insert before main content
    const mainContent = document.querySelector('main') || document.querySelector('[role="main"]');
    if (mainContent) {
        mainContent.parentElement.insertBefore(container, mainContent);
    }
});

// Footer Prev/Next navigation enhancement
document.addEventListener('DOMContentLoaded', function() {
    const footer = document.querySelector('.md-footer__inner.md-grid');
    if (!footer) return;
    
    // Check if we have both prev and next links
    const prevLink = document.querySelector('.md-footer__link--prev');
    const nextLink = document.querySelector('.md-footer__link--next');
    
    if (prevLink || nextLink) {
        // Create our own styled footer nav
        const navContainer = document.createElement('div');
        navContainer.className = 'tu-footer-nav';
        
        const navList = document.createElement('ul');
        navList.className = 'tu-footer-nav__list';
        
        if (prevLink) {
            const prevLi = document.createElement('li');
            prevLi.className = 'tu-footer-nav__item tu-footer-nav__item--prev';
            const prevLinkClone = prevLink.cloneNode(true);
            // Clean up classes
            prevLinkClone.className = 'tu-footer-nav__link';
            prevLi.appendChild(prevLinkClone);
            navList.appendChild(prevLi);
        }
        
        if (nextLink) {
            const nextLi = document.createElement('li');
            nextLi.className = 'tu-footer-nav__item tu-footer-nav__item--next';
            const nextLinkClone = nextLink.cloneNode(true);
            nextLinkClone.className = 'tu-footer-nav__link';
            nextLi.appendChild(nextLinkClone);
            navList.appendChild(nextLi);
        }
        
        navContainer.appendChild(navList);
        
        // Insert before the copyright section
        const footerMeta = document.querySelector('.md-footer-meta');
        if (footerMeta) {
            footerMeta.parentElement.insertBefore(navContainer, footerMeta);
        }
    }
});
