import json
try:
    with open('papers.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
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
