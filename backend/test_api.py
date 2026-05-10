
import requests

API_KEY = "YzL7GBd82cDwTT4GMNDEp997aycqLDyffXldLDcg"
# Curiosity on Sol 1000 (roughly May 31, 2015) - Guaranteed to have photos
url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={API_KEY}"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success! Found {len(data['photos'])} photos.")
else:
    print(f"❌ Failed with status code: {response.status_code}")
    print(response.text)