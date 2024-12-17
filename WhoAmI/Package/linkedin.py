import os
import requests
from dotenv import load_dotenv

load_dotenv()

nubela_api_key = os.getenv('NUBELA_API_KEY')

def scrape_linkedin_profile(linkedin_profile_url: str = None, mock: bool = False):
    if mock:
        api_url = 'https://gist.githubusercontent.com/rishadharis/c3a481badecffac573c4f502395bf0a0/raw/6ab67ee207af4bf68125e29465a104009deebf05/rishad-harisdias-linkedin.json'
        response = requests.get(api_url, timeout=10)
    else:
        if linkedin_profile_url is None:
            raise ValueError('LinkedIn profile URL is required.')
        
        headers = {'Authorization': 'Bearer ' + nubela_api_key}
        api_url = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'linkedin_profile_url': linkedin_profile_url,
            'extra': 'include',
            'github_profile_id': 'include',
            'personal_contact_number': 'include',
            'personal_email': 'include',
            'inferred_salary': 'include',
            'skills': 'include',
            'use_cache': 'if-recent',
            'fallback_to_cache': 'on-error',
        }
        response = requests.get(api_url, params=params, headers=headers)
    
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None, "None")
        and k not in ["people_also_viewed","activities","inferred_salary","extra"]
    }
    return data
        
if __name__ == '__main__':
    print(scrape_linkedin_profile(mock=True))