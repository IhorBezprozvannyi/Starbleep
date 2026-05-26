import requests
NASA_API_KEY = "DEMO_KEY"
print("Testing NASA Mars Rover API...")

url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
params = {"api_key": NASA_API_KEY, "sol": 100, "camera": "FHAZ"}

r = requests.get(url, params=params)
photos = r.json()["photos"][:3]

print(f" Found {len(photos)} Curiosity photos!")
for p in photos:
    print(f" {p['earth_date']} - {p['camera']['name']}")
    print(f"  {p['img_src'][:80]}...")
print(" SUCCESS!")
