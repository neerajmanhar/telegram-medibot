import requests
from config import TAVILY_API_KEY, GOOGLE_PLACES_API_KEY

def search_web(query):
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    res = requests.post(url, json={"query": query, "search_depth": "basic"}, headers=headers)
    results = res.json()
    return results.get("answer", "No results found.")

def find_nearby_places(keyword, location="28.61,77.20"):
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}"
        f"&radius=5000&keyword={keyword}&key={GOOGLE_PLACES_API_KEY}"
    )
    res = requests.get(url)
    results = res.json().get("results", [])
    return [r["name"] for r in results[:3]]
