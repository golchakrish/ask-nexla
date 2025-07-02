import requests
import json

ENDPOINTS = {
    "posts": "https://nexla.com/wp-json/wp/v2/posts",
    "pages": "https://nexla.com/wp-json/wp/v2/pages",
    "landing-page": "https://nexla.com/wp-json/wp/v2/landing-page",
    "resources": "https://nexla.com/wp-json/wp/v2/resources"
}

def fetch_items(name, url):
    items = []
    page = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
    }
    while True:
        res = requests.get(url, params={"per_page": 20, "page": page}, headers=headers)
        print(f"Fetching: {url}?page={page}")
        print("Status code:", res.status_code)
        print("Response:", res.text[:300])  # Show only first 300 chars
        if res.status_code != 200:
            print(res.text)
            break
        data = res.json()
        if not data:
            break
        for item in data:
            items.append({
                "id": item.get("id"),
                "type": name,
                "title": item.get("title", {}).get("rendered", ""),
                "content": item.get("content", {}).get("rendered", "") or item.get("excerpt", {}).get("rendered", ""),
                "link": item.get("link", "")
            })
        page += 1
    return items

# Test just posts first
if __name__ == "__main__":
    # Test just posts first
    res = requests.get(
        "https://nexla.com/wp-json/wp/v2/posts",
        headers={"User-Agent": "Mozilla/5.0"},
        params={"per_page": 5}
    )
    print(res.status_code)
    print(res.json())
    # Fetch all content types at once
    all_content = []
    for name, url in ENDPOINTS.items():
        all_content.extend(fetch_items(name, url))
    with open("nexla_indexed_content.json", "w") as f:
        json.dump(all_content, f, indent=2)
    print("Indexing complete. Saved to 'nexla_indexed_content.json'")
