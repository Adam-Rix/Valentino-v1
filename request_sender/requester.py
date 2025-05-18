# requester.py
# v1.0.0
import logging
import json
import os

# logger
logging.basicConfig(level=logging.INFO, format="%(message)s")

async def send_request(client, item):
    method = item.get("method", "GET").upper()
    url = item["url"]
    headers = item.get("headers", {}).copy()
    body = item.get("body")

    # always use https
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    # token if requested
    # if "Authorization" not in headers and item.get("auth", {}).get("type") == "bearer":
    #     token = os.getenv("TOKEN")
    #     headers["Authorization"] = f"Bearer {token}"

    # # default-headers if needed
    # headers.setdefault("Accept-Encoding",
    #                    os.getenv("ACCEPT_ENCODING"))
    # headers.setdefault("Connection",
    #                    os.getenv("CONNECTION"))

    # hard-coded cookies
    cookies = {
        "PHPSESSID": os.getenv("PHPSESSID"),
        "_csrf": os.getenv("_csrf"),
        "_identity-biz": os.getenv("_identity-biz"),
        "module_id": os.getenv("MODULE_ID")
    }

    try:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            cookies=cookies,
            json=body
        )

        # processing with request from API
        logging.info(f"[{method}] {url} -> {response.status_code}")
        try:
            parsed = response.json()
            logging.info(json.dumps(parsed, indent=2, ensure_ascii=False))
        except Exception:
            logging.warning("⚠️ Response isn't JSON")
            logging.info(response.text)

        return response

    except Exception as e:
        logging.error(f"[❌] Request failed for {url}: {e}")
        return None
