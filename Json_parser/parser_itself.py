# parser_itself.py
# v1.1.1
import json
import os


def parse_collection(data):
    result = []

    for item in data.get("item", []):
        name = item.get("name")
        request = item.get("request", {})
        method = request.get("method", "GET")
        url = request.get("url", {}).get("raw", "").replace(os.getenv("OLD_DOMAIN"),
                                                            os.getenv("NEW_DOMAIN"))

        headers = {h["key"]: h["value"] for h in request.get("header", [])}
        body = request.get("body", {}).get("raw")

        body_json = None
        body_error = False

        if body:
            try:
                body_json = json.loads(body)
            except json.JSONDecodeError:
                body_error = True

        # Pars examples of responses from response board from json
        example_responses = []
        for resp in item.get("response", []):
            code = resp.get("code")
            body_raw = resp.get("body", "")
            try:
                json.loads(body_raw)  # Is that valid?
                example_responses.append({
                    "code": code,
                    "body": body_raw,
                    "originalRequest": resp.get("originalRequest", {})
                })
            except json.JSONDecodeError:
                continue
                #Debug
                # print(f"\n❌ ERROR parsing response body: {e}")
                # print(f"Body content:\n{body_raw} \n")

        # Structure of saved response from server
        result.append({
            "name": name,
            "method": method,
            "url": url,
            "headers": headers,
            "body": body_json,
            "example_responses": example_responses
        })

        summary = []
        if body:
            summary.append("✅ request has body")
        elif method.upper() in ["POST", "PUT", "PATCH"] and body is None:
            summary.append("❌ request body is None")
        else:
            summary.append("ℹ️ GET request has no body")


        if example_responses:
            summary.append(f"✅ {len(example_responses)} example(s) of response")
        else:
            summary.append(f"❌ {len(example_responses)} example of response")


        summary_text = " | ".join(summary)
        print(f"[🔍] Parsed item: {method} {url} — {summary_text}")

    return result