#v0.0.1
from Valentino_v1.Json_parser.parser_itself import parse_collection
from Valentino_v1.request_sender.requester import send_request

import asyncio
import json
import jsonschema
import logging
import httpx
import os

class JParser:
    def __init__(self, collection_path):
        self.collection_path = collection_path

    async def Gettig_Json(self):
        with open(self.collection_path, "r", encoding = "utf-8") as f:
            data = json.load(f)

        items = parse_collection(data)

        async with httpx.AsyncClient(timeout=15) as client:
            tasks = [send_request(client, item) for item in items]
            responses = await asyncio.gather(*tasks)
            for r in responses:
                if r is not None:
                    try:
                        print(f"\n[✅] Response from {r.request.url} ({r.status_code}):")
                        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
                    except Exception:
                        print(f"\n[⚠️] Non-JSON response from {r.request.url} ({r.status_code}):")
                        print(r.text)

