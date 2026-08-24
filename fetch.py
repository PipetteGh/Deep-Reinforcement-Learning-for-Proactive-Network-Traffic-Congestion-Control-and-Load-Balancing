import json
import urllib.request

url = "https://api.openalex.org/works?search=deep+reinforcement+learning+routing+traffic+engineering&filter=publication_year:2022-2026&per-page=6"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
    for w in data.get('results', []):
        authors = w.get('authorships', [])
        author_name = authors[0]['author']['display_name'] if authors else 'Unknown'
        title = w.get('title')
        year = w.get('publication_year')
        source = w.get('primary_location', {}).get('source', {})
        source_name = source.get('display_name') if source else 'Unknown'
        print(f"{title} by {author_name} ({year}) - {source_name}")
except Exception as e:
    print(f"Error: {e}")
