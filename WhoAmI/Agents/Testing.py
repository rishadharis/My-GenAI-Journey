import requests
from urllib.parse import urlparse

def is_valid_linkedin_profile(url):
    """
    Check if a LinkedIn profile URL is valid (returns 200) or invalid (returns 404).
    
    Args:
        url (str): LinkedIn profile URL to validate
        
    Returns:
        bool: True if profile exists, False if 404 or invalid URL
    """
    # Validate URL format first
    try:
        parsed = urlparse(url)
        if not parsed.netloc.endswith('linkedin.com'):
            return False
    except:
        return False
        
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        
        # Check if we got a successful response
        if response.status_code == 200:
            return True
        # Check specifically for 404
        elif response.status_code == 404:
            return False
        # Handle other status codes as invalid
        else:
            return False
            
    except requests.RequestException:
        # Handle any request errors (timeout, connection error, etc.)
        return False
    
print(is_valid_linkedin_profile("https://www.linkedin.com/in/anandadp"))