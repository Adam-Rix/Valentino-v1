#v0.0.1
import asyncio
import logging

async def send_request(client, item):
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    method = item.get("method", "GET").upper()
    url = item["url"]
    headers = item.get("headers", {})
    body = item.get("body", None)

    try:
        response = await client.request(method,
                                        url,
                                        headers=headers,
                                        json=body)
        logging.info(f"[{method}] {url} -> {response.status_code}\n{response.text}")
        return response

    except Exception as e:
        print(f"Error for {url}: {e}")