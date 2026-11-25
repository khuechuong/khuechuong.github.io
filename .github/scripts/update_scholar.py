"""Get total Google Scholar citations via SerpAPI and save to assets/data/scholar.json.

Needs the SERPAPI_KEY repository secret. Exits with an error (red run in
GitHub Actions) if the lookup fails; the old value is kept.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

AUTHOR_ID = "D14wq88AAAAJ"
OUT = "assets/data/scholar.json"

key = os.environ.get("SERPAPI_KEY")
if not key:
    sys.exit("SERPAPI_KEY is not set. Add it under Settings > Secrets and variables > Actions.")

url = "https://serpapi.com/search.json?" + urllib.parse.urlencode({
    "engine": "google_scholar_author",
    "author_id": AUTHOR_ID,
    "hl": "en",
    "api_key": key,
})
data = json.load(urllib.request.urlopen(url, timeout=60))

if "error" in data:
    sys.exit(f"SerpAPI error: {data['error']}")

try:
    count = int(data["cited_by"]["table"][0]["citations"]["all"])
except (KeyError, IndexError, TypeError, ValueError):
    sys.exit(f"Unexpected SerpAPI response: {json.dumps(data)[:500]}")

with open(OUT, "w") as f:
    json.dump({"citations": count}, f)
    f.write("\n")
print("citations:", count)
