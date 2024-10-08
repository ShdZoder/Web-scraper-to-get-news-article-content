import requests
from bs4 import BeautifulSoup

def get_content(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting information with a helper function
        def extract_text(selector, class_name=None):
            if class_name:
                element = soup.find(selector, class_=class_name)
            else:
                element = soup.find(selector)
            return element.get_text(strip=True) if element else 'Not found'

        title = extract_text('h1')
        updated_date = extract_text('time')
        byline = extract_text('div', class_name='!text-brand.text-sm.font-normal')
        article_content = extract_text('div', class_name='ciam-article-pf1')

        return {
            'title': title,
            'updated_date': updated_date,
            'byline': byline,
            'content': article_content
        }

    except requests.RequestException as e:
        return {'error': f'Network error: {e}'}
    except Exception as e:
        return {'error': f'Error: {e}'}
    
if __name__ == '__main__':
    link = 'https://www.planetf1.com/news/michael-schumacher-accident-what-happened-condition'
    content = get_content(link)
    print(content)
