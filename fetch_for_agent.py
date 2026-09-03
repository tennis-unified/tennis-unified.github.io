#!/usr/bin/env python3
"""
Hermes-Friendly Web Scraper
Fetches a target URL, strips HTML boilerplate, extracts core content,
and formats it cleanly for Hermes Agent consumption.
"""
import sys
import re
import json
import urllib.request
import urllib.error
from html.parser import HTMLParser
from datetime import datetime, timezone

class ContentExtractor(HTMLParser):
    """Extract clean text content from HTML, skipping junk elements."""
    
    def __init__(self):
        super().__init__()
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header', 'iframe', 'noscript'}
        self.current_skip = 0
        self.text_parts = []
        self.in_body = False
        self.title = ''
        self.in_title = False
        self.in_h1 = False
        self.h1_text = ''
        self.images = []
        self.links = []
        self.videos = []
        self.in_a = False
        self.current_link = None
        self.tag_stack = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.tag_stack.append(tag)
        
        if tag in self.skip_tags:
            self.current_skip += 1
            return
            
        if self.current_skip > 0:
            return
            
        if tag == 'body':
            self.in_body = True
            
        if tag == 'title':
            self.in_title = True
            
        if tag == 'h1':
            self.in_h1 = True
            
        if tag == 'img' and 'src' in attrs_dict:
            self.images.append({
                'src': attrs_dict['src'],
                'alt': attrs_dict.get('alt', '')
            })
            
        if tag == 'a' and 'href' in attrs_dict:
            self.in_a = True
            self.current_link = {'href': attrs_dict['href'], 'text': ''}
            
        if tag == 'iframe' and 'src' in attrs_dict:
            self.videos.append(attrs_dict['src'])
            
    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
            
        if tag in self.skip_tags:
            self.current_skip = max(0, self.current_skip - 1)
            return
            
        if self.current_skip > 0:
            return
            
        if tag == 'title':
            self.in_title = False
            
        if tag == 'h1':
            self.in_h1 = False
            
        if tag == 'a' and self.in_a:
            if self.current_link and self.current_link.get('text', '').strip():
                self.links.append(self.current_link)
            self.in_a = False
            self.current_link = None
            
        if tag in ['p', 'div', 'br', 'li', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.text_parts.append('\n')
            
    def handle_data(self, data):
        if self.current_skip > 0:
            return
            
        if self.in_title:
            self.title += data
            
        if self.in_h1:
            self.h1_text += data
            
        if self.in_a and self.current_link:
            self.current_link['text'] += data
            
        stripped = data.strip()
        if stripped:
            self.text_parts.append(stripped)
            
    def get_clean_text(self):
        """Return cleaned text content."""
        text = ' '.join(self.text_parts)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text)
        # Collapse multiple newlines
        text = text.replace('\n ', '\n').replace(' \n', '\n')
        return text.strip()
    
    def get_result(self):
        """Return structured result."""
        return {
            'status': 'success',
            'title': self.title or self.h1_text or 'No Title',
            'h1': self.h1_text,
            'body_text': self.get_clean_text(),
            'images': self.images[:20],  # Limit to save tokens
            'links': self.links[:30],
            'videos': self.videos,
            'content_length': len(self.get_clean_text())
        }


def fetch_for_agent(url, timeout=15):
    """
    Fetch a URL and extract clean content for Hermes Agent.
    
    Args:
        url: Target URL to scrape
        timeout: Request timeout in seconds
        
    Returns:
        dict: Structured content data
    """
    # Validate URL
    if not url or not url.startswith(('http://', 'https://')):
        return {'status': 'error', 'message': 'Invalid URL. Must start with http:// or https://'}
    
    # Stealth headers to avoid bot detection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            html = response.read().decode('utf-8', errors='replace')
            http_code = response.getcode()
            
        if http_code != 200:
            return {'status': 'error', 'message': f'HTTP {http_code}'}
            
    except urllib.error.HTTPError as e:
        return {'status': 'error', 'message': f'HTTP Error {e.code}: {e.reason}'}
    except urllib.error.URLError as e:
        return {'status': 'error', 'message': f'URL Error: {e.reason}'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error: {str(e)}'}
    
    # Parse HTML and extract content
    parser = ContentExtractor()
    try:
        parser.feed(html)
    except Exception as e:
        return {'status': 'error', 'message': f'Parse Error: {str(e)}'}
    
    result = parser.get_result()
    result['url'] = url
    result['extracted_at'] = datetime.now(timezone.utc).isoformat()
    result['http_code'] = http_code
    
    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python fetch_for_agent.py <URL>")
        print("Returns structured JSON content from the target URL.")
        sys.exit(1)
        
    url = sys.argv[1]
    result = fetch_for_agent(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
