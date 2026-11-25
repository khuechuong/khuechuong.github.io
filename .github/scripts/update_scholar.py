import json, re, sys, urllib.request

URL = "https://scholar.google.com/citations?user=D14wq88AAAAJ&hl=en"
OUT = "assets/data/scholar.json"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
m = re.search(r'class="gsc_rsb_std">(\d+)<', html)  # first cell = total citations
if not m:
    sys.exit("Could not find citation count (Scholar may have blocked the request); keeping old value.")
count = int(m.group(1))
with open(OUT, "w") as f:
    json.dump({"citations": count}, f)
    f.write("\n")
print("citations:", count)
