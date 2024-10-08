import requests
from bs4 import BeautifulSoup
import sys

def scrape_article(url):
    # Send a GET request to the URL 
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve article. Status code: {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title
    title = soup.find('h1').get_text(strip=True)

    # Extract the article content
    paragraphs = soup.find_all('p')
    content = "\n".join([para.get_text(strip=True) for para in paragraphs])

    # Optionally extract other information like byline or updated date
    byline = soup.find('span', class_='css-1n7hynb').get_text(strip=True) if soup.find('span', class_='css-1n7hynb') else 'No byline found'
    updated_date = soup.find('time').get('datetime') if soup.find('time') else 'No updated date found'

    # Return the extracted information
    return {
        'title': title,
        'content': content,
        'byline': byline,
        'updated_date': updated_date
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_newyorktimes.py <article_url>")
        sys.exit(1)

    article_url = sys.argv[1]
    article_data = scrape_article(article_url)

    if article_data:
        print("Title:", article_data['title'])
        print("Byline:", article_data['byline'])
        print("Updated Date:", article_data['updated_date'])
        print("Content:", article_data['content'])
