import requests

# Searching for Lunar Reconnaissance Orbiter (LRO) products
URL = "https://nasa.gov"
params = {
    "q": "target:Moon AND instrument:\"Lunar Reconnaissance Orbiter Camera\"",
    "wt": "json",
    "rows": 5
}

response = requests.get(URL, params=params)

if response.status_code == 200:
    results = response.json().get('response', {}).get('docs', [])
    print("Recent Lunar Data Products found:")
    for doc in results:
        title = doc.get('title', 'No Title')
        data_id = doc.get('identifier', 'N/A')
        print(f"- {title} (ID: {data_id})")
else:
    print("Failed to connect to PDS API.")
