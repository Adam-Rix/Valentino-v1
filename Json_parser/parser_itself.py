#v0.0.1
import json

def parse_collection(data):

    result = []

    for item in data.get("item", []):
        name = item.get("name")
        request = item.get("request", {})
        method = request.get("method", "GET")
        url = request.get("url", {}).get("raw", "")

        headers = {h["key"]: h["value"] for h in request.get("header", [])}
        body = request.get("body", {}).get("raw")

        body_json = None

        if body:
            try:
                body_json = json.loads(body)
            except json.JSONDecodeError:
                pass  # logging

        result.append({
            "name": name,
            "method": method,
            "url": url,
            "headers": headers,
            "body": body_json
        })

        print(f"[🔍] Parsed item: {method} {url}")

    return result