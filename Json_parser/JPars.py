# JPars.py
# v1.0.0

import asyncio
import json
import httpx
from Valentino_v1.Json_parser.parser_itself import parse_collection
from Valentino_v1.request_sender.requester import send_request

class JParser:
    def __init__(self, collection_path):
        self.collection_path = collection_path

    async def Gettig_Json(self):
        with open(self.collection_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Parse each request and example of response
        items = parse_collection(data)

        #  create async client
        async with httpx.AsyncClient(timeout=15) as client:
            # create coroutine (list of async tasks)
            tasks = [send_request(client, item) for item in items]
            responses = await asyncio.gather(*tasks) #wait while all will be ended

        # sorting through pairs
        for item, response in zip(items, responses):
            url = item.get("url")
            print(f"\n[🔍] Validating structure for: {url}")

            if response is None:
                print("[❌] No response received.")
                continue

            try:
                actual_json = response.json()
            except Exception:
                print(f"[⚠️] Non-JSON response from {url} ({response.status_code}):\n⚠️⚠️⚠️SKIPPED⚠️⚠️⚠️")
                continue

            # generator which searchs and returns examples with code == 200 or none if generator is empty
            expected_response = next(
                (r for r in item.get("example_responses", []) if r.get("code") == 200),
                None
            )

            if not expected_response:
                print("[ℹ️] No example response found for validation.")
                continue

            try:
                expected_json = json.loads(expected_response.get("body", "{}"))
                validate_structure(expected_json, actual_json)

                '''Debugging prints with expected and actual responses'''
                # print("Expected (parsed from collection):", json.dumps(expected_json, indent=2, ensure_ascii=False))
                # print("Actual (from response):", json.dumps(actual_json, indent=2, ensure_ascii=False))

            except json.JSONDecodeError:
                print("[⚠️] Example body in collection is not valid JSON.")

# matching dicts and lists in memory
def validate_structure(expected, actual, path=""):

    if isinstance(expected, dict):

        if not isinstance(actual, dict):
            print(f"❌ Type mismatch at {path or 'root'}: expected object")
            return False

        for key in expected:

            if key not in actual:
                print(f"❌ Missing key at {path or 'root'}: {key}")

            else:
                validate_structure(expected[key], actual[key], path + f".{key}")
                print(f"✅ Matched with Reference key at {path or 'root'}: {key}")

    elif isinstance(expected, list) and isinstance(actual, list):
        for i, (exp, act) in enumerate(zip(expected, actual)):
            validate_structure(exp, act, path + f"[{i}]")

