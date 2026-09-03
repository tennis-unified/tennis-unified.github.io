<?php
/**
 * Hermes-Friendly PHP Scraping API
 * 
 * Fetches a target URL, strips HTML boilerplate, extracts core content,
 * and formats it cleanly into JSON for Hermes Agent consumption.
 * 
 * Usage: fetch_for_agent.php?url=https://example.com
 */

header('Content-Type: application/json');

// Only allow requests with a URL payload
$targetUrl = $_GET['url'] ?? null;
if (!$targetUrl || !filter_var($targetUrl, FILTER_VALIDATE_URL)) {
    echo json_with_code(400, "Error: A valid 'url' query parameter is required.");
    exit;
}

// 1. Fetch HTML using a Stealth User-Agent to avoid early blocks
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $targetUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 15);
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language: en-US,en;q=0.5',
]);

$html = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200 || !$html) {
    echo json_with_code(500, "Error: Unable to fetch page content. HTTP Code: " . $httpCode);
    exit;
}

// 2. Parse HTML and clean up noise (scripts, navbars, footers)
$dom = new DOMDocument();
libxml_use_internal_errors(true);
$dom->loadHTML($html);
libxml_clear_errors();

$xpath = new DOMXPath($dom);

// Remove useless nodes to save LLM tokens
$junkElements = $xpath->query("//script | //style | //nav | //footer | //header | //iframe | //noscript");
foreach ($junkElements as $junk) {
    $junk->parentNode->removeChild($junk);
}

// 3. Isolate the main content body or specific structured text
$bodyNode = $dom->getElementsByTagName('body')->item(0);
$cleanText = $bodyNode ? trim(preg_replace('/\s+/', ' ', $bodyNode->nodeValue)) : '';

// Extract images
$images = [];
$imgNodes = $dom->getElementsByTagName('img');
foreach ($imgNodes as $img) {
    $src = $img->getAttribute('src');
    $alt = $img->getAttribute('alt');
    if ($src) {
        $images[] = ['src' => $src, 'alt' => $alt];
    }
}

// Extract links
$links = [];
$linkNodes = $dom->getElementsByTagName('a');
foreach ($linkNodes as $link) {
    $href = $link->getAttribute('href');
    $text = trim($link->nodeValue);
    if ($href && $text) {
        $links[] = ['href' => $href, 'text' => $text];
    }
}

// Extract videos (YouTube iframes)
$videos = [];
$iframeNodes = $dom->getElementsByTagName('iframe');
foreach ($iframeNodes as $iframe) {
    $src = $iframe->getAttribute('src');
    $src = $iframe->getAttribute('src');
    if ($src && (strpos($src, 'youtube') !== false || strpos($src, 'vimeo') !== false)) {
        $videos[] = $src;
    }
}

// 4. Return LLM-ready structured JSON data
echo json_encode([
    'status' => 'success',
    'url' => $targetUrl,
    'extracted_at' => date('c'),
    'http_code' => $httpCode,
    'content_length' => strlen($cleanText),
    'data' => [
        'title' => $dom->getElementsByTagName('title')->item(0)?->nodeValue ?? 'No Title',
        'h1' => $dom->getElementsByTagName('h1')->item(0)?->nodeValue ?? '',
        'body_text' => mb_strimwidth($cleanText, 0, 10000, "... [Truncated for Agent Token Limits]"),
        'images' => array_slice($images, 0, 20),
        'links' => array_slice($links, 0, 30),
        'videos' => $videos
    ]
], JSON_PRETTY_PRINT);

function json_with_code($code, $message) {
    http_response_code($code);
    return json_encode(['status' => 'error', 'message' => $message]);
}
